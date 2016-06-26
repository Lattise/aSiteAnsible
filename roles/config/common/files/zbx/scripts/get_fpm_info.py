#!/usr/bin/env python3

import argparse
from urllib.request import urlopen
import json


def main():
    parser = argparse.ArgumentParser(description='parse php-fpm status')
    parser.add_argument('key', choices=[
        'accepted conn',
        'listen queue',
        'listen queue len',
        'idle processes',
        'active processes',
        'total processes',
        'slow requests',
    ])
    parser.add_argument('url', default='http://localhost/fpm-status')
    args = parser.parse_args()
    args.url += '?json'

    content = urlopen(args.url)
    content = json.loads(content.read().decode())
    print(content[args.key])


if __name__ == "__main__":
    main()
