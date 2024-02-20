#!/bin/bash

# Funktioniert nicht, nicht alle ISSN werden gefunden

for i in $(cat 2023-11-20-Article_list_dirty.tsv | grep -Po [0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9] | sort | uniq ); do
	echo -n "$i " && cat 2023-11-20-Article_list_dirty.tsv | grep -m 1 "$i" | sed -e "s/\r//g" | awk '{print $NF}'
done >results.tsv
