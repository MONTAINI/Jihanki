import csv
import json
csvfile = open('Loading.csv', 'r')
jsonfile = open('/home/ServalChan/Jihanki/web_app/loading.json', 'w')
fieldnames = ("jihanki","stock","jan_code","xy","coordnate_X","coodnate_Y","earnings")
reader = csv.DictReader(csvfile, fieldnames)
for row in reader:
  jsonfile.write('[')
  json.dump(row, jsonfile)
  jsonfile.write(']')

