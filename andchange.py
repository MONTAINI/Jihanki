import csv
import json
csvfile = open('android.csv', 'r')
jsonfile = open('andch.json', 'a')
fieldnames = ("id","user_id","pass","age","prof","from","gen","nfc")

reader = csv.DictReader(csvfile, fieldnames)
for row in reader:
  jsonfile.write('[')
  json.dump(row, jsonfile, ensure_ascii=False)
  jsonfile.write(']')
