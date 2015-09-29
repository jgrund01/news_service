#!/usr/bin/env bash

# scrape new news items every hour
SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
(crontab -l ; echo "0 * * * * python $SCRIPTPATH/api/cronUpdateNewsFeeds.py") | crontab -

