#!/bin/bash

source component_slice_config.sh

echo connecting to node: $1
export FILES="component.py ../util/cert.py ../util/credential.py ../util/excep.py ../util/server.py ../util/sfaticket.py ../util/gid.py ../util/misc.py ../util/record.py ../util/rights.py ../util/report.py ../util/trustedroot.py ../plc/trusted_roots install"
echo $FILES
scp -i $KEY_FILE -r $FILES $USER@$1:$DEST_DIR
