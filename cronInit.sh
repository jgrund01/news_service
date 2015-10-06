#!/usr/bin/env bash

SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
(crontab -l ; echo "0 * * * * python $SCRIPTPATH/manage.py update_news_items") | crontab -

