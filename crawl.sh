#!/bin/sh

YESTERDAY=`date -j -v-1d '+%Y-%m-%d'`

# first run the crawler
./crawler.py -f $YESTERDAY -t $YESTERDAY

# the zaken subtree
./zaken_subtree.py $YESTERDAY