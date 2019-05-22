# vault_downloader
Helper to upload/download your secrets from vault to local file

## Requirements 
Vault Server - [How to run vault server](https://hub.docker.com/_/vault/)

Python 3.6 or higher - [Installation Guide](https://www.python.org/downloads/)

## Create your vitual environment
```
python -m venv ~/.venvs/vault
source ~/.venvs/vault/bin/activate
```
## Install dependencies
```
pip install -r requirements.txt
```

## Configure
Requires 3 env vars to be set.

VAULT_ADDR - url of vault server.

VAULT_ROLE_ID - your app role id.

VAULT_ROLE_SECRET - secret id that authenticates your role

## Get token
```
./vault_helper.py get_vault_token
```
Follow instructions to export your token

## Use it
From your local machine
```
./vault_helper.py upload your_file.yaml
```
From your production server
```
./vault_helper.py download your_local_version.yaml
```