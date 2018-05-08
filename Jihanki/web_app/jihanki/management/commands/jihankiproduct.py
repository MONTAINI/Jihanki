import json
from django.core.management.base import BaseCommand
from django.core import serializers
import collections as cl
from ...models import Product, Jihanki, JihankiProduct

# BaseCommandを継承して作成
class Command(BaseCommand):
	# python manage.py help import_earningsで表示されるメッセージ
	help = 'Create jihankiproduct from json file'

	# コマンドが実行された際に呼ばれるメソッド
	def handle(self, *args, **options):
		jsonfile = open('/home/ServalChan/jihankiproduct.json', 'w')
		fieldnames = ("jihanki","product","stock","price","xy")
		jproduct = JihankiProduct.objects.all()
		json_serializer = serializers.get_serializer('json')()
		jsonfile.write('[')
		for jp in jproduct:
			data = cl.OrderedDict()
			data = [
				[fieldnames[0], jp.jihanki.jihanki_id],
				[fieldnames[1], jp.product.jan_code],
				[fieldnames[2], jp.stock],
				[fieldnames[3], jp.price],
				[fieldnames[4], jp.xy]
			]
			jsonfile.write(',')
			json.dump(dict(data), jsonfile, ensure_ascii=False)
		jsonfile.write(']')

		for jp in jproduct:
			jid = jp.jihanki.jihanki_id
			print(jid)
