import json
from django.core.management.base import BaseCommand
from django.core import serializers
import collections as cl
from ...models import Jihanki

# BaseCommandを継承して作成
class Command(BaseCommand):
	# python manage.py help import_earningsで表示されるメッセージ
	help = 'Create jihanki from json file'

	# コマンドが実行された際に呼ばれるメソッド
	def handle(self, *args, **options):
		jsonfile = open('/home/ServalChan/jihanki.json', 'w')
		fieldnames = ("jihanki_id","address","coordinate_X","coordinate_Y","change")
		jihanki = Jihanki.objects.all()
		json_serializer = serializers.get_serializer('json')()
		jsonfile.write('[')
		for j in jihanki:
			data = cl.OrderedDict()
			data = [
				[fieldnames[0], j.jihanki_id],
				[fieldnames[1], j.address],
				[fieldnames[2], j.coordinate_X],
				[fieldnames[3], j.coordinate_Y],
				[fieldnames[4], j.change]
			]
			jsonfile.write(',')
			json.dump(dict(data), jsonfile, ensure_ascii=False)
		jsonfile.write(']')

		for j in jihanki:
			jadd = j.address
			print(jadd)
