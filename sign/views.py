from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from  django.urls import reverse
from  django.contrib import  auth
from sign.models import  Guest,Event
from  django.db.models import  Q
from  django.core.paginator import  Page,PageNotAnInteger,Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.
#首页
def index(request):
    return render(request,'sign/index.html')

#登录
def login_action(request):
    if request.method =='POST':
        #取出用户名密码
        uname = request.POST.get('username','')
        pwd  = request.POST.get('password','')
        print('uname : %s -- pwd :%s' %(uname, pwd))
        '''
        使用 authenticate()函数认证给出的用户名和密码。它接受两个参数，用户名 username 和密码 password，
        并在用户名密码正确的情况下返回一个 user 对象。如果用户名密码不正确，则 authenticate()返回 None。

        '''
        user=auth.authenticate(username=uname,password=pwd)
        if user is not  None:
            auth.login(request,user)
            #print('path  :%s'%(reverse('sign:event_manage')))
            #return  HttpResponseRedirect('/event_manage/')
            response =redirect(reverse('sign:event_manage'))
            '''
             #添加浏览器cookie，将cookie 保存到硬盘上  key  value  过期时间  路径和域
            #response.set_cookie('user',uname,3600)
            '''
            #给浏览器添加session
            request.session['user']=uname  #将用户名保存在session里

            return  response
        else:
            return  render(request,'sign/index.html',context={'error':'wrong'})
    else:
        return render(request, 'sign/index.html', context={'error': 'wrong'})
#退出
@login_required()
def logout(request):
    auth.logout(request)
    #return HttpResponseRedirect('/index/')
    return redirect(reverse('sign:index'))




####################################################################发布会
@login_required()#必须登录才能访问
def event_manage(request):

      #读取浏览器的cookies
      #cookie_usrname=request.COOKIES.get('user','')

     event_list = Event.objects.all()

     session_usrname=request.session.get('user','')#从session用户名中取出用户名

     #创建分页器（每两条）
     paginator =  Paginator(event_list,2)
     #paginator.count 总共多少数据
     #paginator.page_range 总共分多少页 range(1,3)分2页
     get_page=request.GET.get('page') #取出传过来的页
     #获取请求列表
     try:
          event_pages=paginator.page(get_page) #获取第几页数据
     except PageNotAnInteger: #如果请求的页数不是数字返回第一页
          event_pages=paginator.page(1)
     context={
          'uname': session_usrname,
          'event_list': event_list,
          'event_pages':event_pages,
            }
     return render(request,'sign/event_manage.html',context=context)

#search
@login_required()
def event_search(request):
    uname=request.session.get('user','')#从session 取出登录名
    keyword=request.GET.get('keyword','')#取出get过来的内容
    event_list=Event.objects.filter(Q(title__contains=keyword))
    return render(request,'sign/event_manage.html',{'uname':uname,'event_list':event_list})

########################################嘉宾
@login_required()
def guest_manage(request):
    guest_list=Guest.objects.all()
    session_uname=request.session.get('user','')
    return render(request,'sign/guest_manage.html',{'uname':session_uname,'guest_list':guest_list})
@login_required()
def guest_search(request):
    uname=request.session.get('user','')
    keyword=request.GET.get('keyword','')
    guest_list=Guest.objects.filter(Q(p_name__contains=keyword)|
                                    Q(p_phone__contains=keyword)
                                    )
    return render(request,'sign/guest_manage.html',{'uname':uname,'guest_list':guest_list})

#进入签到
@login_required()
def event_sign(request,event_id):
    event=get_object_or_404(Event,pk=event_id)
    guest_count=Guest.objects.filter(event_id=event_id).count()
    sign_count = Guest.objects.filter(event_id=event_id,p_sign=True).count()
    context={'event':event,'guest_count':guest_count,'sign_count':sign_count}
    return render(request,'sign/sign.html',context=context)



#######################################签到 138888888888
@login_required()
def event_sign_action(request,event_id):
    #通过id获取发布会名
    event= get_object_or_404(Event,pk=event_id)
    #获取手机号
    phone=request.POST.get('phone','')
    result=Guest.objects.filter(p_phone=phone)
    if not result :
        return render(request,'sign/sign.html',{'event':event,'status':'phone not exist'})
    #2次过滤，判断手机号和id来判断，如果未空，则表示手机号没有注册发布会
    result_filter=Guest.objects.filter(p_phone=phone,event_id=event_id)
    if not result_filter:
        return render(request,'sign/sign.html',{'event':event,'status':'phone or id wrong'})

    result_filter =Guest.objects.get(p_phone=phone,event_id=event_id)
    if result_filter.p_sign:
        return  render(request,'sign/sign.html',{'event':event,'status':'user is already sign'})
    else:
        result= Guest.objects.filter(p_phone=phone,event_id=event_id).update(p_sign='1')
        # 嘉宾、签到
        guest_count = Guest.objects.filter(event_id=event_id).count()
        sign_count = Guest.objects.filter(event_id=event_id, p_sign=True).count()
        context={
        'event':event,
        'guest':result_filter,
        'status':'sign access',
        'guest_count':guest_count,
        'sign_count':sign_count
                 }
        return render(request,'sign/sign.html',context=context)


