#!/usr/bin/python3

import argparse
import sys, getopt
import hcl2
import json
import datetime
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def main(argv):
    tfVariables = {}
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--keyVault", help="name of the keyVault to access")
    parser.add_argument("-t", "--vaultType", help="type of vault, values can be vault or vaultcore", default='vault')
    parser.add_argument("-i", "--ifile", help="file to import, usually the variables.tf of the role module")
    parser.add_argument("-o", "--ofile", help="file to save, must end in .json")
    args = parser.parse_args()
 
    credential = DefaultAzureCredential()
    keyVaultClient = SecretClient(vault_url="https://{}.{}.azure.net/".format(args.keyVault, args.vaultType), credential=credential)
    with open(args.ifile, 'r') as file:
        tfVariablesDictSimple = hcl2.load(file)
    for set in tfVariablesDictSimple['variable']:
        for k in set:
            tfVariables[k] = retrieveValue(keyVaultClient, k, set)
        pass
    pass
    with open(args.ofile, 'w') as out:
        out.write(json.dumps(tfVariables))
        out.close()
      
    

def retrieveValue(keyVaultClient, key, set):
    try:
        secret = keyVaultClient.get_secret(key)
        return secret.value
    except:
        try:
            return set[key]['default'][0]
        except:
            return 'NOVALUEFOUND'

if __name__ == "__main__":
   main(sys.argv[1:])
