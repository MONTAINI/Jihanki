import json

from django.core.management.base import BaseCommand

from ...models import Loading, Jihanki


# BaseCommandを継承して作成
class Command(BaseCommand):
    # python manage.py help import_loadingで表示されるメッセージ
    help = 'Create Loading from json file'

    def remove_null(self, value, default):
        if value is None:
            return default
        return value

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):

        # ファイルのオープン
        with open('loading.json', 'r') as file:

            # JSONの読み込み
            data = json.load(file)
            count = 0

            # 取得したデータを1件づつ取り出す
            for loading_obj in data:

                if not loading_obj['jihanki']:
                    continue

                # loadingの保存処理
                loading = Loading()
                loading.jihanki_id = self.remove_null(loading_obj['jihanki'], '')
                loading.jan_code = self.remove_null(loading_obj['jan_code'], '')
                loading.stock = self.remove_null(loading_obj['stock'], 0)
                loading.earnings = self.remove_null(loading_obj['earnings'], 0)
                loading.xy = self.remove_null(loading_obj['xy'], '')
                loading.save()

                count += 1
                print('Create Loading: {0}: {1}'.format(loading.id, loading.jihanki))

            print('{} loadings have been created.'.format(count))
