from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Product(models.Model):
    CATEGORY_CHOICES = (
        (u'お茶', u'お茶'),(u'水', u'水'),(u'炭酸・エナジードリンク', u'炭酸・エナジードリンク'),
        (u'コーヒー・乳製品', u'コーヒー・乳製品'),(u'果汁・野菜', u'果汁・野菜'),(u'その他', u'その他')
    )
    # product_id = models.CharField('商品ID', max_length=10, primary_key=True)
    jan_code = models.CharField('JANコード', max_length=255, primary_key=True)
    name = models.CharField('商品名', max_length=255)
    maker = models.CharField('メーカー', max_length=255)
    maker_price = models.IntegerField('メーカー価格', default=0)
    category = models.CharField('カテゴリ', max_length=255, null=True, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

    # カテゴリ：
        # お茶
        # 水
        # 炭酸・エナジードリンク
        # コーヒー・乳製品
        # 果汁・野菜
        # その他

class Jihanki(models.Model):
    jihanki_id = models.CharField('自動販売機ID', max_length=255, primary_key=True)
    address = models.CharField('住所', max_length=255)
    coordinate_X = models.CharField('座標X', max_length=255)
    coordinate_Y = models.CharField('座標Y', max_length=255)
    change = models.IntegerField('お釣り', default=0)

    def __str__(self):
        return self.address

class JihankiProduct(models.Model):
    XY_CHOICES = (
        (u'a1', u'a1'),(u'a2', u'a2'),(u'a3', u'a3'),(u'a4', u'a4'),(u'a5', u'a5'),(u'a6', u'a6'),(u'a7', u'a7'),(u'a8', u'a8'),
        (u'b1', u'b1'),(u'b2', u'b2'),(u'b3', u'b3'),(u'b4', u'b4'),(u'b5', u'b5'),(u'b6', u'b6'),(u'b7', u'b7'),(u'b8', u'b8'),
        (u'c1', u'c1'),(u'c2', u'c2'),(u'c3', u'c3'),(u'c4', u'c4'),(u'c5', u'c5'),(u'c6', u'c6'),(u'c7', u'c7'),(u'c8', u'c8')
    )
    jihanki = models.ForeignKey(Jihanki, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.IntegerField('在庫', default=0)
    price = models.IntegerField('価格', default=0)
    xy = models.CharField('補充位置', max_length=10, null=True, choices=XY_CHOICES)

    def encode(self):
         return {
             'product': self.product,
             }

    def __str__(self):
        return ('%s %s' % (self.product, self.jihanki))

class Earnings(models.Model):
    jihanki = models.ForeignKey(Jihanki, on_delete=models.CASCADE)
    stock_L = models.IntegerField('左在庫', default=0, null=True)
    stock_R = models.IntegerField('右在庫', default=0, null=True)
    jan_code =models.CharField('JANコード', max_length=255, null=True)
    jan_code_L = models.CharField('左JANコード', max_length=255, null=True)
    jan_code_R = models.CharField('右JANコード', max_length=255, null=True)
    coordinate_X = models.CharField('座標X', max_length=255)
    coordinate_Y = models.CharField('座標Y', max_length=255)
    earnings = models.IntegerField('売上', default=0)
    user_id = models.CharField('ユーザID', max_length=255)
    purchase_flag = models.CharField('購入フラグ', max_length=255)
    created_time = models.DateTimeField('created time', auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return ('%s %s' % (self.purchase_flag, self.jihanki))

class Loading(models.Model):
    jihanki = models.ForeignKey(Jihanki, on_delete=models.CASCADE)
    jan_code = models.CharField('JANコード', max_length=255)
    stock = models.IntegerField('在庫', default=0, null=True)
    earnings = models.IntegerField('売上', default=0, null=True)
    xy = models.CharField('補充位置', max_length=10, null=True)
    created_time = models.DateTimeField('created time', auto_now_add=True, blank=True, null=True)

class User_info(models.Model):
    GEN_CHOICES = (
        (u'男性', u'男性'),(u'女性', u'女性')
    )
    PRO_CHOICES = (
        (u'公務員', u'公務員'),(u'経営者・役員', u'経営者・役員'),(u'会社員', u'会社員'),
        (u'自営業', u'自営業'),(u'専業主婦', u'専業主婦'),(u'パート・アルバイト', u'パート・アルバイト'),
        (u'学生', u'学生'),(u'その他', u'その他')
    )
    user_id = models.CharField('ユーザID', max_length=255)
    age = models.CharField('年齢', max_length=100)
    gen = models.CharField('性別',  max_length=30, choices=GEN_CHOICES)
    pro = models.CharField('職業', max_length=30, choices=PRO_CHOICES)
    area = models.CharField('都道府県', max_length=50)


