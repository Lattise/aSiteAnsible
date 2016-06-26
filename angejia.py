#!/usr/bin/env python
import argparse
import os
import string
from builtins import input

from git import InvalidGitRepositoryError, NoSuchPathError, Repo


def parse_args():
    parser = argparse.ArgumentParser(
        description='deploy a new version')
    parser.add_argument('version', nargs='?',
                        help='which version to deploy')
    parser.add_argument('-F', '--fire', dest='fire', action='store_true',
                        help='only fire version')
    parser.add_argument('-D', '--deploy', dest='deploy', action='store_true',
                        help='only deploy version')
    parser.add_argument('-B', '--backend-only', dest='backend', action='store_true',
                        help='only update backend code')
    parser.add_argument('-E', '--env', dest='env', action='store_true',
                        help='only update env')
    args = parser.parse_args()
    if not args.deploy and not args.fire and not args.env:
        args.all = True

    return args


def playbook(args):
    tags = []
    if hasattr(args, 'all') and args.all:
        tags = ['all']
    else:
        if args.deploy:
            tags.append('deploy')
        if args.fire:
            tags.append('fire')
        if args.env:
            tags.append('env')

    cmd = 'ansible-playbook'
    cmd_args = [cmd,
                'angejia.yml',
                '--tags=%s' % (','.join(tags)),
                ]

    if args.version:
        cmd_args.append('--extra-vars=angejia_version=%s' % args.version)

    if args.backend:
        cmd_args.append('--extra-vars=backend=%s' % args.backend)

    os.execvp(cmd, cmd_args)


def pick_version():
    try:
        repo = Repo('./repos/angejia')
        repo.remotes.origin.pull()
    except (InvalidGitRepositoryError, NoSuchPathError):
        repo = Repo.clone_from('git@git.corp.angejia.com:service/angejia.git', './repos/angejia')

    tags = string.split(repo.git.tag('--sort=version:refname'), '\n')[-10:]
    default_tag = tags[-1]
    for tag in tags:
        print(' ' + tag)
    version = input('which version [%s]?' % default_tag).strip()
    if not version:
        version = default_tag
    return version


def main():
    args = parse_args()
    if not args.env and args.version is None:
        args.version = pick_version()
    playbook(args)


if __name__ == '__main__':
    main()
