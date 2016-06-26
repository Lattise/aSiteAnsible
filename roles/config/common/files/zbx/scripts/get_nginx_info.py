#!/usr/bin/env python3

import argparse
from urllib.request import urlopen
import re


def main():
    parser = argparse.ArgumentParser(description='parse nginx server status')
    parser.add_argument('key', choices=[
        'active_connections',
        'accepted_connections',
        'handled_connections',
        'handled_requests',
        'reading',
        'writing',
        'waiting',
    ])
    parser.add_argument('url', default='http://localhost/server-status')
    args = parser.parse_args()

    content = urlopen(args.url)
    content = content.read().decode().splitlines()
    if args.key == 'active_connections':
        print(re.match(r'Active connections:\s*(\d+)', content[0]).group(1))
    elif args.key in ('accepted_connections', 'handled_connections', 'handled_requests'):
        match_obj = re.match(r'\s+(\d+)\s+(\d+)\s+(\d+)', content[2])
        if args.key == 'accepted_connections':
            print(match_obj.group(1))
        elif args.key == 'handled_connections':
            print(match_obj.group(2))
        elif args.key == 'handled_requests':
            print(match_obj.group(3))
    elif args.key in ('reading', 'writing', 'waiting'):
        match_obj = re.match(r'Reading:\s*(\d+)\s*Writing:\s*(\d+)\s*Waiting:\s*(\d+)', content[3])
        if args.key == 'reading':
            print(match_obj.group(1))
        elif args.key == 'writing':
            print(match_obj.group(2))
        elif args.key == 'waiting':
            print(match_obj.group(3))


if __name__ == "__main__":
    main()
