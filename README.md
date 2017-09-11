# overleaf2word

Convert [LaTeX](https://www.latex-project.org/) documents hosted on
[overleaf.com](https://overleaf.com) to Microsoft Word documents. The module
parses a TeX formatted file and knows how to convert the following tags/
environments into approximate Word equivalents:

- LaTeX paragraphs (i.e. blocks of text separated by one or more blank lines)
  are formatted as Word paragraphs.
- `\title`
- `\section`, `\subsection`, `\subsubsection`, etc.
- Formatting:
  - `\textbf`
  - `\textit`
  - `\clearpage`
- `\cite` and, if a [BibTex](http://www.bibtex.org/) file is provided,
  `\bibliography`

# Installation

First, `git clone` this repo.

```
git clone https://github.com/adamlabadorf/overleaf2word.git
cd overleaf2word
```

I suggest you use [anaconda](https://www.anaconda.com/downloads) or
[miniconda3](https://conda.io/miniconda.html) to create an environment:

```
conda create -n overleaf2word python=3.5
source activate overleaf2word
```

You can install all the prerequisite software packages with `pip`:

```python
pip install -f requirements.txt
```

# Run

Run without arguments, the `run.py` script looks for a file named
`sources.json` that has the info for overleaf projects:

```
[
  {
    "git_clone_url":"<git clone url from overleaf>",
    "latex_paths": [
      "main.tex",
      "<other .tex files in the project you want to convert>"
    ]
  },
  {
     "git_clone_url":"<another overleaf git clone url>" ,
     "latex_paths": [ ... ]
  },
  ...
]
``` 

Run it with or without a path to a sources file:

```
python run.py # looks for sources.json
python run.py some_other_overleaf_sources.json
```

Every time `run.py` is executed, each of the repos in the sources file is cloned
locally and the `latex_paths` are converted to correspondingly named Word docs.

If you don't want to use this with overleaf, the function `tex_to_word` can be
called independently, signature:

```python
def tex_to_word(tex_fn,bib_fn=None) :
    r"""Convert a LaTeX formatted file to docx format
    
    Parses ``tex_fn`` and converts text and some markup tags and environments
    into Word constructs. Creates a file with the same basename as ``tex_fn``
    but with ``.docx`` extension, e.g. ``main.tex -> main.docx``.
    
    If ``bib_fn`` is not provided, all ``\cite`` tags are replaced by parentheses,
    leaving keys as is. If ``bib_fn`` is provided, all ``\cite`` tags are replaced
    by <Author> <Year> formatted references, and if a ``\bibliography`` tag is
    present, a Reference section is formatted at the end of the document.
    
    :param tex_fn: path to LaTeX formatted file
    :param bib_fn: optional path to BibTeX formatted file containing citation
        information
    :return: nothing
    """
```
