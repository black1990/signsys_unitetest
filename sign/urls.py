from  django.conf.urls import  url
from  . import views ,views_if
urlpatterns=[
    url(r'^$',views.index),
    url(r'^index/$',views.index,name='index'),#首页
    url(r'^login_action/$',views.login_action,name='login_action'),#登录
    url(r'^logout/$',views.logout,name='logout'),#退出
    url(r'^event_manage/',views.event_manage,name='event_manage'),#发布会管理
    url(r'^event_search/',views.event_search,name='event_search'),#发布会搜索
    url(r'^guest_manage/',views.guest_manage,name='guest_manage'),#嘉宾管理
    url(r'^guest_search/',views.guest_search,name='guest_search'), #嘉宾搜索
    url(r'^accounts/login/$', views.index) , # 其他页面默认跳转到首页登录
    url(r'^event_sign/(?P<event_id>[0-9]+)/$',views.event_sign,name='event_sign'), #进入签到
    url(r'^event_sign_action/(?P<event_id>[0-9]+)/$',views.event_sign_action,name='event_sign_action'),#签到
    #接口配置
    url(r'^api/add_event/', views_if.add_Event, name='add_event'),
    url(r'^api/add_event_search/', views_if.add_event_search, name='add_event_search'),
    url(r'^api/add_guest/', views_if.add_guest, name='add_guest'),
    url(r'^api/add_guest_search/',views_if.add_guest_search, name='add_guest_search')

]