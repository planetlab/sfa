#!/bin/bash
for l in $(awk '{split($2, spl, "/"); print $4"\/"spl[length(spl)]}' python_install.log)
do 
		rm $l 2> /dev/null
done

exit 0