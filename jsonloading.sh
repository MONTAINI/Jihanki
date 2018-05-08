#!/bin/sh

cd /home/ServalChan/Jihanki

. /home/ServalChan/Jihanki/bin/activate

cd


./jihanki.sh Loading.csv 'python3 /home/ServalChan/Jihanki/web_app/manage.py earnings && python3 /home/ServalChan/Jihanki/web_app/manage.py jihankiproduct && python3 /home/ServalChan/Jihanki/web_app/manage.py product'

