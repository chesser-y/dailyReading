"""Commit archive changes and push the current branch, without force or resets."""
import argparse,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
def git(*args,check=True):return subprocess.run(['git',*args],cwd=ROOT,text=True,capture_output=True,check=check)
def main():
    p=argparse.ArgumentParser();p.add_argument('--message',required=True);p.add_argument('--commit-only',action='store_true');args=p.parse_args()
    subprocess.run([sys.executable,str(ROOT/'scripts/validate.py')],check=True)
    if git('rev-parse','--show-toplevel').stdout.strip()!=str(ROOT):raise SystemExit('Unexpected repository root')
    branch=git('symbolic-ref','--short','HEAD').stdout.strip()
    if not args.commit_only:
        remote=git('remote','get-url','origin',check=False)
        if remote.returncode:raise SystemExit('origin is not configured; archive remains local, no push attempted')
        git('fetch','origin')
        remote_ref=git('show-ref','--verify','--quiet',f'refs/remotes/origin/{branch}',check=False)
        if remote_ref.returncode==0:git('merge','--ff-only',f'origin/{branch}')
    # Only these archive paths belong to the recurring publishing scope.
    allowed=['README.md','AGENTS.md','.gitignore','requirements.txt','papers','reports','data','docs','templates','scripts']
    existing=[name for name in allowed if (ROOT/name).exists()]
    for name in existing:
        path=ROOT/name
        for candidate in ([path] if path.is_file() else path.rglob('*')):
            if candidate.is_symlink():raise SystemExit(f'Refusing symlink: {candidate.relative_to(ROOT)}')
    git('add','--',*existing)
    changes=git('diff','--cached','--name-only','-z').stdout.split('\0')
    for name in filter(None,changes):
        if pathlib.Path(name).parts[0] not in allowed:raise SystemExit(f'Unexpected staged path: {name}')
        if pathlib.Path(name).suffix not in {'.md','.json','.png','.py','.txt',''} and name!='.gitignore':raise SystemExit(f'Unexpected staged file: {name}')
    if git('diff','--cached','--quiet',check=False).returncode!=0:git('commit','-m',args.message)
    sha=git('rev-parse','HEAD').stdout.strip();print('Commit:',sha)
    if not args.commit_only:
        git('push','--set-upstream','origin',branch)
        remote_sha=git('ls-remote','origin',f'refs/heads/{branch}').stdout.split()[0]
        if remote_sha!=sha:raise SystemExit('Remote verification failed')
        print('Push verified:',sha)
    else:print('Local commit only; no push')

if __name__=='__main__':
    try:main()
    except subprocess.CalledProcessError as e:
        print(e.stderr or str(e),file=sys.stderr);sys.exit(e.returncode)
