#!/usr/bin/env bash

# scrape new news items every hour
(crontab -l ; echo "0 * * * * python /path/to/script/cronUpdateNewsFeeds.py") | crontab -

