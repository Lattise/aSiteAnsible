#!/usr/bin/env python3

import redis
import argparse
import json


def get_specific_key(key, data):
    for node in key.split('.'):
        data = data[node]
    return data


def get_db_list(client):
    data = []
    for db_name in client.info('keyspace').keys():
        data.append({'{#DBNAME}': db_name})
    return json.dumps({'data': data})


def get_redis_info(key, client):
    if key != 'discovery':
        section, key = key.split('.', maxsplit=1)
        res = client.info(section)
        return get_specific_key(key, res)
    else:
        return get_db_list(client)


def main():
    parser = argparse.ArgumentParser(description='Zabbix Redis status script')
    parser.add_argument('key')
    parser.add_argument('hostname', default='localhost', nargs='?')
    args = parser.parse_args()
    if not args.hostname:
        args.hostname = 'localhost'

    client = redis.StrictRedis(args.hostname)

    print(get_redis_info(args.key, client))


if __name__ == "__main__":
    main()
