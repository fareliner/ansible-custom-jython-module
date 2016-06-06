# Jython Ansible Role #

Installs jython and configures it to work with syslog.

#### TODO

[] install pip modules
[x] install jna native (need to add jar to search path somehow due to native listing in the MANIFEST.MF file)
[x] install syslog

#### Notes

Logging to syslog using jna on unix

```py
from org.productivity.java.syslog4j import SyslogConstants, Syslog
syslog = Syslog.getInstance("unix_syslog")
syslog.info("This is an INFO level log entry.")

```
