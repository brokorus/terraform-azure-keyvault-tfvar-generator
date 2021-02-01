#!/usr/bin/python3

import argparse
import sys, getopt
import hcl2
import json
import logging
import datetime
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def main(argv):
    logger = logging.getLogger('azure')
    logger.setLevel(logging.ERROR)
    tfVariables = {}
    missingVars = []
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--keyVault", help="name of the keyVault to access")
    parser.add_argument("-t", "--vaultType", help="type of vault, values can be vault or vaultcore", default='vault')
    parser.add_argument("-i", "--ifile", help="file to import, usually the variables.tf of the role module")
    parser.add_argument("-o", "--ofile", help="file to save, must end in .json")
    parser.add_argument("-g", "--globalKeyVault", help="endpoint that points to a shared keyvault to also try, in the future will allow a tuple instead")
    parser.add_argument("-a", "--apiEndpoint", help="use azure.net for azure public or usgovcloudapi.net for azure government", default='usgovcloudapi.net')
    args = parser.parse_args()
 
    credential = DefaultAzureCredential()
    keyVaultClient = SecretClient(vault_url="https://{}.{}.{}/".format(args.keyVault, args.vaultType, args.apiEndpoint), credential=credential)
    keyVaultGlobalClient = SecretClient(vault_url="https://{}.{}.{}/".format(args.globalKeyVault, args.vaultType, args.apiEndpoint), credential=credential)
    with open(args.ifile, 'r') as file:
        tfVariablesDictSimple = hcl2.load(file)
    for set in tfVariablesDictSimple['variable']:
        for k in set:
            tfVariables[k] = retrieveValue(keyVaultClient, k, set, keyVaultGlobalClient)
        pass
    pass
    with open(args.ofile, 'w') as out:
        out.write(json.dumps(tfVariables))
        out.close()

    for key in tfVariables:
        try:
            if tfVariables[key] == "NOVALUEFOUND":
                missingVars.append(key)
        except:
            error=0
    try:
        if len(missingVars) != 0:
            print("""

The following variables do not have default values, and have not been set in the appropriate keyvault

{}

Go to https://{}.{}.{}/ and configure the missing variables there

            """.format(missingVars, args.keyVault, args.vaultType, args.apiEndpoint))
            sys.exit()
        else:
            print('All variables found')
    except ValueError:
        error=1
    

def retrieveValue(keyVaultClient, key, set, keyVaultGlobalClient):
    try:
        secret = keyVaultClient.get_secret(key.replace("_", "-"))
        return secret.value
    except:
        try:
            secret = keyVaultGlobalClient.get_secret(key.replace("_", "-"))
            return secret.value
        except:
            try:
                return set[key]['default'][0]
            except:
                return 'NOVALUEFOUND'

if __name__ == "__main__":
   main(sys.argv[1:])
