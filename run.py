#!/usr/bin/env python
import argparse
import json
from overleaf2word import overleaf2word

parser = argparse.ArgumentParser(description='Convert overleaf latex sources to word docs')
parser.add_argument('sources', help='path to JSON file containing overleaf sources',
  nargs='?',default='sources.json'
)

if __name__ == '__main__':
    args = parser.parse_args()
    with open(args.sources) as f :
        overleaf_repos = json.load(f)
    for repo in overleaf_repos :
        overleaf2word(repo['git_clone_url'],repo.get('latex_paths',[]))
