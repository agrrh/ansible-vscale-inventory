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

def scalet_dump(scalet):
    return {
        'ansible_host': scalet['public_address']['address'],
        'vscale_location': scalet['location'],
        'vscale_hostname': scalet['hostname'],
        'vscale_name': scalet['name'],
        'vscale_plan': scalet['rplan'],
        'vscale_image': scalet['made_from'],
        'vscale_id': scalet['ctid']
    }

if __name__ == '__main__':
    token = get_token()
    if not token:
        print('Could not find token in VS_API_KEY or VSCALE_API_TOKEN vars')
        sys.exit(1)

    scalets = get_scalets()

    tags = [[t['name'] for t in s['tags']] for s in scalets]
    tags = [t for sub in tags for t in sub]  # [[a],[b]] -> [a, b]

    locations = [s['location'] for s in scalets]

    result = {
        '_meta': {
            'hostvars': {
                s['hostname']: scalet_dump(s) for s in scalets
            }
        },
        'vscale': {
            'hosts': [s['hostname'] for s in scalets]
        }
    }

    for location in locations:
        result['vscale_location_' + location] = {
            'hosts': [s['hostname'] for s in scalets if location == s['location']]
        }

    for tag in tags:
        result['vscale_tag_' + tag] = {
            'hosts': [s['hostname'] for s in scalets if tag in [t['name'] for t in s['tags']]]
        }

    result = json.dumps(result, indent=2)
    print(result)
