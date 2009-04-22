#!/bin/bash
for i in `ps aux |grep "python plc.py" | head -n3 |awk '{print $2}'` ; do
        echo "killing $i"
        kill $i
done

echo "Start Registry"
python plc.py -r -d
echo "Start Aggregate Manager"
python plc.py -a -d
echo "Start Slice Manager"
python plc.py -s -d 
