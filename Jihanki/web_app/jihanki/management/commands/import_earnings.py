import json

from django.core.management.base import BaseCommand

from ...models import Earnings, Jihanki


# BaseCommandを継承して作成
class Command(BaseCommand):
    # python manage.py help import_earningsで表示されるメッセージ
    help = 'Create Earnings from json file'

    def remove_null(self, value, default):
        if value is None:
            return default
        return value

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):

        # ファイルのオープン
        with open('earnings.json', 'r') as file:

            # JSONの読み込み
            data = json.load(file)
            count = 0

            # 取得したデータを1件づつ取り出す
            for earnings_obj in data:

                if not earnings_obj['jihanki']:
                    continue

                # earningsの保存処理
                earnings = Earnings()
                earnings.jihanki_id = self.remove_null(earnings_obj['jihanki'], '')
                earnings.jan_code = self.remove_null(earnings_obj['jan_code'], '')
                earnings.coordinate_X = self.remove_null(earnings_obj['coordinate_X'], '')
                earnings.coordinate_Y = self.remove_null(earnings_obj['coordinate_Y'], '')
                earnings.earnings = self.remove_null(earnings_obj['earnings'], 0)
                earnings.user_id = self.remove_null(earnings_obj['user_id'], '')
                earnings.purchase_flag = self.remove_null(earnings_obj['purchase_flag'], '')
                earnings.save()

                count += 1
                print('Create Earnings: {0}: {1}'.format(earnings.id, earnings.jihanki))

            print('{} earningss have been created.'.format(count))
