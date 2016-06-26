#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import configparser
from os import path

from qiniu import Auth, put_data

ext_map = {
    'android': 'apk',
    'ios': 'ipa',
}


def checkout(args):
    config_path = path.join(path.dirname(__file__), 'config.ini')
    config = configparser.ConfigParser()
    config.read(config_path)
    access_key = config.get('default', 'AccessKey')
    secret_key = config.get('default', 'SecretKey')
    bucket_name = config.get('default', 'BucketName')

    # 暂时只能上传broker包
    assert args.type[0] == 'broker'

    version_key = '/app/{type}/{version}/{type}.{ext}'.format(type=args.type[0], version=args.version[0],
                                                              ext=ext_map[args.platform[0]])

    current_key = 'app/{type}/{type}.{ext}'.format(type=args.type[0], ext=ext_map[args.platform[0]])

    q = Auth(access_key, secret_key)
    token = q.upload_token(bucket_name, current_key, 3600)
    ret, info = put_data(token, current_key, data=version_key, mime_type='application/redirect302')

    assert ret['key'] == current_key
    return ret['key']


def main():
    parser = argparse.ArgumentParser(description='upload local file to qiniu.')

    parser.add_argument('type', nargs=1, help='which type of app to upload')
    parser.add_argument('platform', nargs=1, help='which platform app to upload')
    parser.add_argument('version', nargs=1, help='version to upload')
    args = parser.parse_args()
    key = checkout(args)
    print(key)


if __name__ == '__main__':
    main()
