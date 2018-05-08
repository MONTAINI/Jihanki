import csv
import json
csvfile = open('Purchase.csv', 'r')
jsonfile = open('/home/ServalChan/Jihanki/web_app/earnings.json', 'w')
fieldnames = ("jihanki","jan_code","coordinate_Y","coordinate_X","earnings","user_id","purchase_flag")

reader = csv.DictReader(csvfile, fieldnames)
for row in reader:
  jsonfile.write('[')
  json.dump(row, jsonfile)
  jsonfile.write(']')
