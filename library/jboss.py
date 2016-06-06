#! /usr/bin/jython
# WANT_JSON

# Note: If you need to use env to discover where json is, in your inventory
# file set the ansible_jython_interpreter variable for the hosts you're
# running this module on ex:
#
# myhost ansible_jython_interpreter="/usr/bin/env jython"
DOCUMENTATION = '''
---
module: wildfly
short_description: Manage wildfly container via jboss-cli
'''

import json
import os, sys
import traceback
import time
import shutil
from datetime import datetime

from jyboss import *


def main():

    # TODO parse ansible module
    facts = dict()

    with open(sys.argv[1]) as mod_args_file:
        args = json.load(mod_args_file)

    shutil.copy2(sys.argv[0], "/tmp/jboss_mod.py")
    shutil.copy2(sys.argv[1], "/tmp/jboss_args.json")

    ctx = JyBossCLI.context()
    ctx.jboss_home = args['jboss_home']
    ctx.noninteractive()
    connect()
    facts['jboss_ls'] = ls()['response']

    result = {
                "changed" : False,
                "ansible_facts": facts,
                "msg" : "result from jython module",
                "executable": sys.executable,
             }

    print json.dumps(result)

if __name__ == '__main__':
    main()
