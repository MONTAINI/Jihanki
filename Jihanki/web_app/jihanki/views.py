import json
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.db.models import Q
from django.core import serializers
from django.db import models as django_models

from .models import Jihanki, Product, JihankiProduct, Earnings, User_info, Loading

# jihanki
@login_required
def jihanki_index(request):
    jihankis = Jihanki.objects.all()
    loading = Loading.objects.all()
    # 検索
    q_name = request.GET.get('jihanki_name')
    if q_name is not None:
        jihankis = Jihanki.objects.filter(address__contains=q_name)
    # お釣り更新(補充)
    ntime = 0
    for j in jihankis:
        jid = j.jihanki_id
        if loading.filter(jihanki=jid).last() is not None:
            lastlo = loading.filter(jihanki=jid).last()
            j.change = lastlo.earnings
            ntime = lastlo.created_time
            j.save()
    #　お釣り更新(購入)
    for j in jihankis:
        if Earnings.objects.filter(jihanki=j.jihanki_id).last() is not None:
            ea = Earnings.objects.filter(jihanki=j.jihanki_id).last()
            if ea.created_time > ntime:
                j.change = ea.earnings
                j.save()
    context = {'jihankis': jihankis, 'jid': jid}
    return TemplateResponse(request, 'jihanki/jihanki_index.html', context=context)

# product
@login_required
def product_index(request):
    products = Product.objects.all()
    q_name = request.GET.get('product_name')
    if q_name is not None:
        products = Product.objects.filter(name__contains=q_name)
    context = {'products': products}
    return TemplateResponse(request, 'product/product_index.html', context=context)

# jihankiproduct
@login_required
def jihankiproduct_index(request, jihanki_id):
    jihankiproducts = JihankiProduct.objects.filter(jihanki=jihanki_id)
    loading = Loading.objects.filter(jihanki=jihanki_id)
    earning = Earnings.objects.filter(jihanki=jihanki_id)
    # 在庫更新(補充)
    for jp in jihankiproducts:
        jan = jp.product.jan_code
        if loading.filter(jan_code=jan).last() is not None:
            lastlo = loading.filter(jan_code=jan).last()
            jp.stock = lastlo.stock
            jp.save()
    # 在庫更新(購入)
    ntime = 0
    if loading.all().last() is not None:
        lastlo = loading.all().last()
        ntime = lastlo.created_time
        for jp in jihankiproducts:
            cont = 0
            jan = jp.product.jan_code
            if earning.filter(jan_code=jan).last() is not None:
                janea = earning.filter(jan_code=jan)
                for je in janea:
                    if ntime <= je.created_time:
                        cont += 1
                jp.stock = jp.stock - cont
                jp.save()
    context = {'jihankiproducts': jihankiproducts}
    return TemplateResponse(request, 'jihankiproduct/jihankiproduct_index.html', context=context)

# toukei
@login_required
def toukei_index(request):
    return TemplateResponse(request, 'toukei/toukei_index.html')

@login_required
def toukei_jihanki_list(request):
    jihankis = Jihanki.objects.all()
    q_name = request.GET.get('jihanki_name')
    if q_name is not None:
        jihankis = Jihanki.objects.filter(address__contains=q_name)
    context = {'jihankis': jihankis}
    return TemplateResponse(request, 'toukei/toukei_jihanki_list.html', context=context)

@login_required
def toukei_jihanki_index(request, jihanki_id):
    data_str = []
    dd_str = []
    jp = JihankiProduct.objects.filter(jihanki=jihanki_id)
    data_str = [jihankiproduct['product'] for jihankiproduct in jp.values('product')]
    for proname in data_str:
        pro_str = Product.objects.filter(jan_code=proname)
        dd_str.extend([product['name'] for product in pro_str.values('name')])
    xy_list = [
        'a1','a2','a3','a4','a5','a6','a7','a8',
        'b1','b2','b3','b4','b5','b6','b7','b8',
        'c1','c2','c3','c4','c5','c6','c7','c8'
        ]
    xy_cont = [
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0
        ]
    for xy_c in range(len(xy_list)):
        xy_cont[xy_c] = xy_cont[xy_c] + Earnings.objects.filter(Q(jihanki=jihanki_id), Q(purchase_flag=xy_list[xy_c])).count()
    # jiha_earL = Earnings.objects.filter(Q(jihanki=jihanki_id), Q(purchase_flag="L")).count()
    # jiha_earR = Earnings.objects.filter(Q(jihanki=jihanki_id), Q(purchase_flag="R")).count()
    context = {
        'jihanki_id': jihanki_id,
        'jihankis': Jihanki.objects.all(),
        'jihankiproducts': JihankiProduct.objects.filter(jihanki=jihanki_id),
        'earnings': Earnings.objects.filter(jihanki=jihanki_id),
        'earningsV': xy_cont,
        'str': dd_str,
        'label': "売上（本）",
        'text': "の売上（本数）"
    }
    return TemplateResponse(request, 'toukei/toukei_jihanki_index.html', context=context)

@login_required
def toukei_jihanki_age(request, jihanki_id):
    age_str = ['～10代','20代','30代','40代','50代','60代','70代','80代','90代～']
    age_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    earning = Earnings.objects.filter(jihanki=jihanki_id)
    user_info = User_info.objects.all()
    for e in earning:
        for u in user_info:
            if e.user_id == u.user_id:
                uage = u.age
                for a in range(len(age_str)):
                    if uage == age_str[a]:
                        age_list[a] = age_list[a] + 1
    context = {
        'jihanki_id': jihanki_id,
        'jihankis': Jihanki.objects.all(),
        'jihankiproducts': JihankiProduct.objects.filter(jihanki=jihanki_id),
        'earningsV': age_list,
        'str': age_str,
        'label': "売上（本）",
        'text': "：年齢ごとの売上（本数）"
    }
    return TemplateResponse(request, 'toukei/toukei_jihanki_index.html', context=context)

@login_required
def toukei_jihanki_profession(request, jihanki_id):
    prof_str = ['公務員','経営者・役員','会社員','自営業','専業主婦','パート・アルバイト','学生','その他']
    prof_list = [0, 0, 0, 0, 0, 0, 0, 0]
    earning = Earnings.objects.filter(jihanki=jihanki_id)
    user_info = User_info.objects.all()
    for e in earning:
        for u in user_info:
            if e.user_id == u.user_id:
                upro = u.pro
                for a in range(len(prof_str)):
                    if upro == prof_str[a]:
                        prof_list[a] = prof_list[a] + 1
    context = {
        'jihanki_id': jihanki_id,
        'jihankis': Jihanki.objects.all(),
        'jihankiproducts': JihankiProduct.objects.filter(jihanki=jihanki_id),
        'earningsV': prof_list,
        'str': prof_str,
        'label': "売上（本）",
        'text': "：職業ごとの売上（本数）"
    }
    return TemplateResponse(request, 'toukei/toukei_jihanki_index.html', context=context)

@login_required
def toukei_jihanki_gen(request, jihanki_id):
    gen_str = ['男性','女性']
    gen_list = [0, 0]
    earning = Earnings.objects.filter(jihanki=jihanki_id)
    user_info = User_info.objects.all()
    for e in earning:
        for u in user_info:
            if e.user_id == u.user_id:
                ugen = u.gen
                for a in range(len(gen_str)):
                    if ugen == gen_str[a]:
                        gen_list[a] = gen_list[a] + 1
    context = {
        'jihanki_id': jihanki_id,
        'jihankis': Jihanki.objects.all(),
        'jihankiproducts': JihankiProduct.objects.filter(jihanki=jihanki_id),
        'earningsV': gen_list,
        'str': gen_str,
        'label': "売上（本）",
        'text': "：性別ごとの売上（本数）"
    }
    return TemplateResponse(request, 'toukei/toukei_jihanki_index.html', context=context)

@login_required
def toukei_jihanki_cate(request, jihanki_id):
    cate_str = ['お茶','水','炭酸・エナジードリンク','コーヒー・乳製品','果汁・野菜','その他']
    cate_list = [0, 0, 0, 0, 0, 0]
    earning = Earnings.objects.filter(jihanki=jihanki_id)
    jihankiproduct = JihankiProduct.objects.filter(jihanki=jihanki_id)
    for e in earning:
        for jp in jihankiproduct:
            if e.jan_code == jp.product.jan_code:
                pcate = jp.product.category
                for a in range(len(cate_str)):
                    if pcate == cate_str[a]:
                        cate_list[a] = cate_list[a] + 1
    context = {
        'jihanki_id': jihanki_id,
        'jihankis': Jihanki.objects.all(),
        'jihankiproducts': JihankiProduct.objects.filter(jihanki=jihanki_id),
        'earningsV': cate_list,
        'str': cate_str,
        'label': "売上（本）",
        'text': "：カテゴリごとの売上（本数）"
    }
    return TemplateResponse(request, 'toukei/toukei_jihanki_index.html', context=context)

@login_required
def toukei_product_list(request):
    products = Product.objects.all()
    q_name = request.GET.get('product_name')
    if q_name is not None:
        products = Product.objects.filter(name__contains=q_name)
    context = {'products': products}
    return TemplateResponse(request, 'toukei/toukei_product_list.html', context=context)

@login_required
def toukei_product_index(request, jan_code):
    month = ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月']
    data = [0,0,0,0,0,0,0,0,0,0,0,0]
    earning = Earnings.objects.filter(jan_code=jan_code)
    for e in earning:
        date = e.created_time
        emonth = date.month
        strmonth = str(emonth)
        remonth = strmonth + '月'
        for a in range(len(month)):
            if remonth == month[a]:
                data[a] = data[a] + 1
    context = {
        'jan_code': jan_code,
        'product': Product.objects.filter(jan_code=jan_code),
        'str': month,
        'earningsV': data,
        'label': "売上（本）",
        'text': "：月ごとの売上（本数）",
        'month': remonth
    }
    return TemplateResponse(request, 'toukei/toukei_product_index.html', context=context)

@login_required
def toukei_product_age(request, jan_code):
    age_str = ['～10代','20代','30代','40代','50代','60代','70代','80代','90代～']
    age_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    earning = Earnings.objects.filter(jan_code=jan_code)
    user_info = User_info.objects.all()
    for e in earning:
        for u in user_info:
            if e.user_id == u.user_id:
                uage = u.age
                for a in range(len(age_str)):
                    if uage == age_str[a]:
                        age_list[a] = age_list[a] + 1
    context = {
        'jan_code': jan_code,
        'product': Product.objects.filter(jan_code=jan_code),
        'earningsV': age_list,
        'str': age_str,
        'label': "売上（本）",
        'text': "：年齢ごとの売上（本数）"
    }
    return TemplateResponse(request, 'toukei/toukei_product_index.html', context=context)

@login_required
def toukei_product_profession(request, jan_code):
    prof_str = ['公務員','経営者・役員','会社員','自営業','専業主婦','パート・アルバイト','学生','その他']
    prof_list = [0, 0, 0, 0, 0, 0, 0, 0]
    earning = Earnings.objects.filter(jan_code=jan_code)
    user_info = User_info.objects.all()
    for e in earning:
        for u in user_info:
            if e.user_id == u.user_id:
                upro = u.pro
                for a in range(len(prof_str)):
                    if upro == prof_str[a]:
                        prof_list[a] = prof_list[a] + 1
    context = {
        'jan_code': jan_code,
        'product': Product.objects.filter(jan_code=jan_code),
        'earningsV': prof_list,
        'str': prof_str,
        'label': "売上（本）",
        'text': "：職業ごとの売上（本数）"
    }
    return TemplateResponse(request, 'toukei/toukei_product_index.html', context=context)

@login_required
def toukei_product_gen(request, jan_code):
    gen_str = ['男性','女性']
    gen_list = [0, 0]
    earning = Earnings.objects.filter(jan_code=jan_code)
    user_info = User_info.objects.all()
    for e in earning:
        for u in user_info:
            if e.user_id == u.user_id:
                ugen = u.gen
                for a in range(len(gen_str)):
                    if ugen == gen_str[a]:
                        gen_list[a] = gen_list[a] + 1
    context = {
        'jan_code': jan_code,
        'product': Product.objects.filter(jan_code=jan_code),
        'earningsV': gen_list,
        'str': gen_str,
        'label': "売上（本）",
        'text': "：性別ごとの売上（本数）"
    }
    return TemplateResponse(request, 'toukei/toukei_product_index.html', context=context)

@login_required
def toukei_product_area(request, jan_code):
    gen_str = ['北海道・東北','関東甲信越','中部','近畿','中国・四国','九州・沖縄']
    context = {
        'jan_code': jan_code,
        'product': Product.objects.filter(jan_code=jan_code),
        'earningsV': [12, 34, 27, 30, 18, 20],
        'str': gen_str,
        'label': "売上（本）",
        'text': "：地域ごとの売上（本数）"
    }
    return TemplateResponse(request, 'toukei/toukei_product_index.html', context=context)

def encode_myway(obj):
    if isinstance(obj, django_models.Model):
        return obj.encode()
    elif isinstance(obj, QuerySet):
        return list(obj)
    else:
        raise TypeError(repr(obj) + " is not JSON serializable")
# Create your views here.
