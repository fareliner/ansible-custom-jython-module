# Example Custom Ansible Module executed with Jython Interpreter

This is an example custom ansible module to manage WildFly/JBoss AS through jython cli.

## Run It

ensure requirements are met (see below) then run the example:

```sh
ansible-playbook -vvvv site.yml
```

or use the vagrant example

```sh
vagrant up
```

## Requirements

1. Target host will need to have jython installed (for this example jython needs to be present on local)

2. jython executable needs to be linked into `/usr/bin` to ensure the interpreter is found by `#! /usr/bin/env jython`

## Limitations

- Tested successfully with ansible 2.0.0.2 but not working on ansible 2.1 anymore

- To get logging working in a remote Linux host, one will need to also compile [syslog.java](https://gist.github.com/bertramn/3a57c6d513cd1e66f8606ceb392cba7b) and enable UDP rsyslog
