#!/bin/sh

cd /home/ServalChan/Jihanki 

. /home/ServalChan/Jihanki/bin/activate

cd /home/ServalChan/Jihanki/web_app

./paa.sh earnings.json 'python3 /home/ServalChan/Jihanki/web_app/manage.py import_earnings'
