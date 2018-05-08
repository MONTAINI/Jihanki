import json
from django.core.management.base import BaseCommand
from django.core import serializers
import collections as cl
from ...models import Product

# BaseCommandを継承して作成
class Command(BaseCommand):
	# python manage.py help import_earningsで表示されるメッセージ
	help = 'Create product from json file'

	# コマンドが実行された際に呼ばれるメソッド
	def handle(self, *args, **options):
		jsonfile = open('/home/ServalChan/product.json', 'w')
		fieldnames = ("jan_code","name","maker","maker_price","category")
		product = Product.objects.all()
		json_serializer = serializers.get_serializer('json')()
		jsonfile.write('[')
		for p in product:
			data = cl.OrderedDict()
			data = [
				[fieldnames[0], p.jan_code],
				[fieldnames[1], p.name],
				[fieldnames[2], p.maker],
				[fieldnames[3], p.maker_price],
				[fieldnames[4], p.category]
			]
			jsonfile.write(',')
			json.dump(dict(data), jsonfile, ensure_ascii=False)
		jsonfile.write(']')

		for p in product:
			pname = p.name
			print(pname)
