#! /usr/bin/env jython

DOCUMENTATION = '''
---
module: wildfly
short_description: Manage wildfly container via jboss-cli
'''

import traceback
import time
from datetime import datetime
from java.lang import IllegalStateException

def retry(exceptions=None, tries=None):
    if exceptions:
        exceptions = tuple(exceptions)

    def wrapper(fun):
        def retry_calls(*args, **kwargs):
            if tries:
                for _ in xrange(tries):
                    try:
                        fun(*args, **kwargs)
                    except exceptions:
                        pass
                    else:
                        break
            else:
                while True:
                    try:
                        fun(*args, **kwargs)
                    except exceptions:
                        pass
                    else:
                        break

        return retry_calls

    return wrapper

# need to deal with: Already connected to server

@retry([IllegalStateException], 10)
def connect(cli, controller_host=None, controller_port=None, admin_username=None, admin_password=None):
    try:
        module.log("trying to connect")
        if controller_host is None or controller_port is None or admin_username is None or admin_password is None:
            cli.connect()
        else:
            cli.connect(controller_host, controller_port, admin_username, admin_password)
    except IllegalStateException as e:
        if e.getMessage().startswith('Already connected to server'):
            module.log("already connected to server")
        else:
            module.log("connecting to server failed, retry in 2 seconds: %s" % e)
            # cleanup and try again
            try:
                cli.disconnect()
            except:
                pass
            time.sleep( 2 )
            raise e

def _normalize_dirpath(dirpath):
    return dirpath[:-1] if dirpath[-1] == '/' else dirpath

def _prepare_cli_classpath(wildfly_home):
    '''
    jboss CLI does something dodgy and can't just append the cli.jar to the system path
    sys.path.append(wildfly_home + "/bin/client/jboss-cli-client.jar")
    instead we are going to add a URL classloader into the loader hierarchy of
    the current thread context
    '''
    from java.lang import ClassLoader, Thread
    from java.net import URL, URLClassLoader
    from java.io import File
    from jarray import array
    cli_jar_path = '%s/%s' % (wildfly_home, 'bin/client/jboss-cli-client.jar')
    module.log("load wildfly cli from %s" % cli_jar_path)
    cliJar = File(cli_jar_path).toURL()
    currentThreadClassLoader = Thread.currentThread().getContextClassLoader()
    urlClassLoader = URLClassLoader(array([cliJar], URL), currentThreadClassLoader)
    Thread.currentThread().setContextClassLoader(urlClassLoader)

def _normalize_dirpath(dirpath):
    return dirpath[:-1] if dirpath[-1] == '/' else dirpath

def main():
    global module
    module = AnsibleModule(
        argument_spec = dict(
            wildfly_home = dict(required=True, type='str')
        )
    )
    wildfly_home = _normalize_dirpath(module.params['wildfly_home'])

    _prepare_cli_classpath(wildfly_home)

    changed = False

    # create a cli session
    from org.jboss.as.cli.scriptsupport import CLI
    cli = CLI.newInstance()
    try:
        connect(cli)
        module.log('after connect one')
        cli.cmd('cd /')
        connect(cli)
        module.log('after connect two')

        # got a connection
        result = {
            "changed": False,
            "msg": "connected to wildfly cli"
        }
        module.exit_json(**result)
    except IllegalStateException as e:
        result = {
            "msg": "failed connecting to wildfly: %s" % (e.getMessage()),
            "traceback": traceback.format_exc()
        }
        module.fail_json(**result)
    finally:
        try:
            cli.disconnect()
        except:
            pass

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
