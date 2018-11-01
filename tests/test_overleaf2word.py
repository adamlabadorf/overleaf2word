from tex2word import tex_to_word, Text, Command, Comment
from pprint import pprint

def test_cmds() :
    assert tex_to_word(r'\cmd') == [Command(r'\cmd',None,None,None)]
    assert tex_to_word(r'\cmd[opt]') == None # this isn't valid, ignored
    assert tex_to_word(r'\cmd[opt]{arg}') == [Command(r'\cmd',[Text('arg')],None,[Text('opt')])]
    assert tex_to_word(r'\cmd{arg1}{arg2}') == [Command(r'\cmd',[Text('arg1')],[Text('arg2')],None)]
    assert tex_to_word(r'\cmd{arg1}[opt]{arg2}') == [Command(r'\cmd',[Text('arg1')],[Text('arg2')],[Text('opt')])]

def test_comment() :
    tex = r'a \% c % comment'
    assert tex_to_word(tex) == [Text('a'),Text(r'\%'),Text('c'),Comment('% comment')]

def test_tabular() :
    tex = r'''
    \begin{tabular}{l|l|l}
    a & \textbf{b} & c \\ \hline
    1 & 2 & 3 \\ \hline
    \end{tabular}
    '''
    res = tex_to_word(tex)
    pprint(res)
    assert False

