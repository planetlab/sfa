source component_slice_config.sh

echo connecting to node: $1
ssh -i $KEY_FILE $USER@$1
