import chardet
from collections import namedtuple
import bibtexparser
import docx
from docx.enum.text import WD_BREAK
from glob import glob
from git import Repo
from itertools import takewhile
import json
import os
from ply import lex, yacc
from pprint import pprint
from subprocess import Popen

REPO_DIR = 'overleaf_repos'

def overleaf2word(url,files=[]) :
    
    repo_root = url.split('/')[-1]
    repo_dir = '{}/{}'.format(REPO_DIR,repo_root)
    
    if not os.path.exists(repo_dir) :
        repo = Repo.clone_from(url,repo_dir)
    else :
        repo = Repo(repo_dir)
        repo.remotes['origin'].pull()
        
    for fn in files :
        tex_to_word(os.path.join(repo_dir,fn))
        

##########################################################################################
# this is the ply tokenizer for latex
tokens = ('COMMAND','EQUATION','WORD','COMMENT','NEWLINE')

def t_COMMAND(t):
    r'\\([a-zA-Z]+)(?:\[([^]]+)\])?(?:{([^}]+)})?'
    t.command, t.opts, t.args = t.lexer.lexmatch.groups()[1:4]
    return t

t_COMMENT = r'%.*'
def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += len(t.value)
    return t
t_WORD = r'[^\ %\n]+'
def t_EQUATION(t) :
    r'[$][^$]+[$]'
    return t

t_ignore = ' '

def t_error(t) :
    print(t)
    return t

lexer = lex.lex()
##########################################################################################

Text = namedtuple('Text',['text','type','style','props'])

def add_run(par,words) :
    if words :
        # add a space at the end for funsies
        text = ' '.join(_.text for _ in words)
        text += ' '
        # text can come in different encodings, coerce it to utf-8
        text = unicode(text,errors='replace')
        r = par.add_run(text,words[-1].style)
        if words[-1].props :
            for k,v in words[-1].props.items() :
                setattr(r,k,v)
            
def add_paragraph(doc,words) :
    '''Add words to doc as paragraph. Words is a list of Text namedtuples. The
    *type* field is used to collapse the words into runs with the same formatting.'''
    # collapse the words into lists of identical type to be turned into a
    # formatted run
    if words :
        par = doc.add_paragraph()
        curr_type = [words.pop(0)]
        while words:
            curr_text = words.pop(0)
            # curr_text is a different type than what we've seen already
            if curr_text.type != curr_type[-1].type : # new run
                add_run(par,curr_type)
                curr_type = [curr_text]
            else :
                curr_type.append(curr_text)
        add_run(par,curr_type)
    
def tex_to_word(tex_fn,bib_fn=None) :
        
    with open(tex_fn) as f :
        tex = f.read()
    parsed = lexer.input(tex)
    
    bibdb = None
    if bib_fn :
        with open(bib_fn) as f:
            bibtex_str = f.read()
        
        bibdb = bibtexparser.loads(bibtex_str)
        bibdb = {_['ID']:_ for _ in bibdb.entries}
    
    def is_heading(args) :
        return 'section' in args
        
    def get_heading_level(args) :
        return args.count('sub')+1
        
    heading_level = 1
    in_doc = False
    prev_token = None
    
    doc = docx.Document()
    text_started = False
    words = []
    
    while True :
        tok = lexer.token()
        if not tok: break
        
        # handle commands, which control the structure of the document
        # and special elements like tables and figures (not yet implemented)
        if tok.type == 'COMMAND' :
            
            if tok.command == 'title' :
                doc.add_heading(tok.args,0)
            
            elif tok.command == 'begin' :
                
                # don't insert anything until we have seen a begin{document}
                if tok.args == 'document' :
                    in_doc = True
                    
                # other \begin's to be supported:
                # table
                # tabular
                # figure
                    
            # \section, \subsection, \subsubsection, etc
            elif is_heading(tok.command) :
                if words :
                    add_paragraph(doc,words)
                    words = []
                heading_level = get_heading_level(tok.command)
                doc.add_heading(tok.args,heading_level)
                
            # insert citation text
            elif tok.command == 'cite':
                ref_strs = tok.args
                if bibdb :
                    refids = tok.args.split(',')
                    refids = [_ for _ in refids if _]
                    ref_strs = []
                    for refid in refids :
                        entry = bibdb[refid] 
                        author = entry.get('author',entry.get('title','')).split(',')[0]           
                        year = entry.get('year','')
                        ref_strs.append(' '.join([author,year]))
                    ref_strs = ','.join(ref_strs)
                citation = Text(
                    text=''.join(['(',ref_strs,')']),
                    type='cite',
                    style=None,
                    props=None
                )
                words.append(citation)
                
            elif tok.command == 'textbf' :
                bold = Text(
                    text=tok.args,
                    type='textbf',
                    style=None,
                    props={'bold':True}
                )
                words.append(bold)
                
            elif tok.command == 'textit' :
                italic = Text(
                    text=tok.args,
                    type='textit',
                    style=None,
                    props={'italic':True}
                )               
                words.append(italic)
                
            elif tok.command == 'clearpage' :
                doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
            else :
                print('unrecognized command:',tok.command,tok.opts,tok.args)
        if tok.type == 'EQUATION' :
            print('found an equation',tok.value)
                    
        # regular text word
        if tok.type == 'WORD' :
            text_started = True
            text = Text(
                text=tok.value,
                type='word',
                style=None,
                props=None
            )
            words.append(text)
            
        # if we hit two newlines in a row, create a new paragraph
        if tok.type == 'NEWLINE' and \
           prev_token and prev_token.type == 'NEWLINE' and \
           text_started :
               add_paragraph(doc,words)
               words = []
            
        prev_token = tok
            
    # write out the doc
    basedir = os.path.dirname(tex_fn)
    basename, ext = os.path.splitext(os.path.basename(tex_fn))
    doc_fn = os.path.join(basedir,'{}.docx'.format(basename))
    doc.save(doc_fn)
        