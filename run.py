import json
from overleaf2word import overleaf2word

if __name__ == '__main__':
    with open('sources.json') as f :
        overleaf_repos = json.load(f)
    for repo in overleaf_repos :
        overleaf2word(repo['git_clone_url'],repo.get('latex_paths',[]))