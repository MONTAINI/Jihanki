from django.conf.urls import url

from . import views

# ルーティングの設定
urlpatterns = [

    # item
    url(r'^$', views.jihanki_index, name='jihanki_index'),

    # prpduct
    url(r'^product/$', views.product_index, name='product_index'),

    # jihankiproduct
    url(r'^jihankiproduct/(?P<jihanki_id>[A-Z0-9]+)/$', views.jihankiproduct_index, name='jihankiproduct_index'),

    # tokei
    url(r'^toukei/$', views.toukei_index, name='toukei_index'),
    url(r'^toukei/jihanki/$', views.toukei_jihanki_list, name='toukei_jihanki_list'),
    url(r'^toukei/jihanki/(?P<jihanki_id>[A-Z0-9]+)/index/$', views.toukei_jihanki_index, name='toukei_jihanki_index'),
    url(r'^toukei/jihanki/(?P<jihanki_id>[A-Z0-9]+)/index/age$', views.toukei_jihanki_age, name='toukei_jihanki_age'),
    url(r'^toukei/jihanki/(?P<jihanki_id>[A-Z0-9]+)/index/profession$', views.toukei_jihanki_profession, name='toukei_jihanki_profession'),
    url(r'^toukei/jihanki/(?P<jihanki_id>[A-Z0-9]+)/index/gen$', views.toukei_jihanki_gen, name='toukei_jihanki_gen'),
    url(r'^toukei/jihanki/(?P<jihanki_id>[A-Z0-9]+)/index/cate$', views.toukei_jihanki_cate, name='toukei_jihanki_cate'),
    url(r'^toukei/product/$', views.toukei_product_list, name='toukei_product_list'),
    url(r'^toukei/product/(?P<jan_code>[A-Z0-9]+)/index/$', views.toukei_product_index, name='toukei_product_index'),
    url(r'^toukei/product/(?P<jan_code>[A-Z0-9]+)/age/$', views.toukei_product_age, name='toukei_product_age'),
    url(r'^toukei/product/(?P<jan_code>[A-Z0-9]+)/profession/$', views.toukei_product_profession, name='toukei_product_profession'),
    url(r'^toukei/product/(?P<jan_code>[A-Z0-9]+)/gen/$', views.toukei_product_gen, name='toukei_product_gen'),
    url(r'^toukei/product/(?P<jan_code>[A-Z0-9]+)/area/$', views.toukei_product_area, name='toukei_product_area'),
    
]