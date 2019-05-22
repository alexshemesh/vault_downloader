#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Requires 3 env vars to be set
VAULT_ADDR - url of vault server
VAULT_ROLE_ID - your app role id
VAULT_ROLE_SECRET - secret id that authenticates your role
"""

import hvac
import os
import yaml
import sys
import click

env = os.environ
vault_addr = env.get('VAULT_ADDR','localhost:8200')
vault_role_id = env.get('VAULT_ROLE_ID','undefined')
vault_role_secret = env.get('VAULT_ROLE_SECRET','undefined')

@click.group()
def cli():
    pass

def get_vault_client():
    client = hvac.Client(url=vault_addr)
    try:
        client.token = env['VAULT_TOKEN']
        if client.is_authenticated():
            print("vault auth: ok")
    except Exception as e:
        print(e)
    return client

@cli.command(help='Get Vault Token')
def get_vault_token():
    client = hvac.Client(url=vault_addr)
    try:
        auth_obj = client.auth_approle(vault_role_id, vault_role_secret)
        client.token = auth_obj['auth']['client_token']
        if client.is_authenticated():
            print('Vault auth is ok. Run following:' )
            print('\texport VAULT_TOKEN=' + client.token)
    except Exception as e:
        print(e)

def _load_yaml(filename):
    """
    Loads YAML content from filename
    :param filename: path to YAML file
    :return: dict with YAML content
    """

    with open(filename, 'r') as stream:
        try:
            data = yaml.safe_load(stream)

        except yaml.YAMLError as e:
            if hasattr(e, 'problem_mark'):
                mark = e.problem_mark
                print("YAML error at position: (%s:%s) in %s: %s" %
                      (mark.line + 1, mark.column + 1, filename, e))
            else:
                print('Error while loading YAML file: %s' % e)
            sys.exit(1)
    return data


@cli.command(help='Write helm secrets from file to vault.')
@click.argument('filename', type=click.Path(exists=True))
def upload(filename):
    vault_client = get_vault_client()
    data = _load_yaml(filename)
    vault_client.write('secret/data/sphera/some_secrets',data=data)


@cli.command(help='Read helm secrets from vault ans saves it to file.')
@click.argument('filename')
def download(filename):
    vault_client = get_vault_client()

    vault_data = vault_client.read('secret/data/sphera/some_secrets')
    d = {}
    for key, value in vault_data['data']['data'].items():
        d[key] = value

    print(yaml.dump(d, default_flow_style=False))
    with open(filename, 'w+') as f:
        f.write(yaml.dump(d, default_flow_style=False))

if __name__ == '__main__':
    cli()