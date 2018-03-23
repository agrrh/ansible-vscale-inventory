#!/usr/bin/env python

import sys
import os
import requests
import json

vscale_api_url = 'https://api.vscale.io/v1'

def get_token():
    for key in ('VS_API_KEY', 'VSCALE_API_TOKEN'):
        if key in os.environ and len(os.environ[key]) == 64:
            return os.environ[key]
    return None

def api_call(path):
    token = get_token()
    resp = requests.get(vscale_api_url + path, headers={'X-Token': token})
    return resp.json()

def get_scalets():
    return api_call('/scalets')

if __name__ == '__main__':
    token = get_token()
    if not token:
        print('Could not find token in VS_API_KEY or VSCALE_API_TOKEN vars')
        sys.exit(1)

    scalets = get_scalets()

    result = {
        '_meta': {
            'hostvars': {
                s['hostname']: {
                    'ansible_host': s['public_address']['address'],
                    'vscale_location': s['location'],
                    'vscale_plan': s['rplan'],
                    'vscale_image': s['made_from'],
                    'vscale_id': s['ctid']
                } for s in scalets
            }
        },
        'vscale': {
            'hosts': [s['hostname'] for s in scalets]
        }
    }

    result = json.dumps(result, indent=2)
    print(result)
