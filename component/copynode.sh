#!/bin/bash
echo connecting to node: $1
export FILES="component.py ../util/cert.py ../util/credential.py ../util/excep.py ../util/geniserver.py ../util/gid.py ../util/misc.py ../util/record.py ../util/rights.py ../util/report.py ../util/trustedroot.py ../registry/trusted_roots install"
echo $FILES
scp -i root_ssh_key.rsa -r $FILES root@$1:/usr/share/NodeManager
