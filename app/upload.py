#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import configparser
from os import path

from qiniu import Auth, put_file

ext_map = {
    'android': 'apk',
    'ios': 'ipa',
}

mime_map = {
    'android': 'application/vnd.android.package-archive',
    'ios': 'application/octet-stream',
}


def upload(args):
    config_path = path.join(path.dirname(__file__), 'config.ini')
    config = configparser.ConfigParser()
    config.read(config_path)
    access_key = config.get('default', 'AccessKey')
    secret_key = config.get('default', 'SecretKey')
    bucket_name = config.get('default', 'BucketName')

    # 暂时只能上传broker包
    assert args.type[0] == 'broker'

    key = 'app/{type}/{version}/{type}.{ext}'.format(type=args.type[0], version=args.version[0],
                                                     ext=ext_map[args.platform[0]])

    q = Auth(access_key, secret_key)
    token = q.upload_token(bucket_name, key, 3600)
    ret, info = put_file(token, key, args.package[0], mime_type=mime_map[args.platform[0]])
    assert ret['key'] == key
    return ret['key']


def main():
    parser = argparse.ArgumentParser(description='upload local file to qiniu.')

    parser.add_argument('type', nargs=1, help='which type of app to upload')
    parser.add_argument('platform', nargs=1, help='which platform app to upload')
    parser.add_argument('version', nargs=1, help='version to upload')
    parser.add_argument('package', nargs=1, help='package to upload')
    args = parser.parse_args()
    key = upload(args)
    print(key)


if __name__ == '__main__':
    main()
