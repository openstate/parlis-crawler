#!/bin/bash

YESTERDAY=`date -d 'yesterday' '+%Y-%m-%d'`

# first run the crawler
./crawler.py -f $YESTERDAY -t $YESTERDAY

# the zaken subtree
# ./zaken_subtree.py $YESTERDAY
