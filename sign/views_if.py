from django.http import  JsonResponse
from sign.models import Event,Guest
from  django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.db.utils import IntegrityError
from  django.views.decorators.csrf import csrf_exempt
import time
#add event interface
@csrf_exempt
def add_Event(request):
    e_id =request.POST.get('e_id','')
    e_title =request.POST.get('e_title','')
    e_limit =request.POST.get('e_limit','')
    e_status = request.POST.get('e_status','')
    e_address = request.POST.get('e_address','')
    e_start_time =request.POST.get('e_start_time','')
    e_end_time =request.POST.get('e_end_time','')
    if e_id == '' or e_title == ''or e_limit =='' or e_status =='' or e_address =='' or\
        e_start_time =='' or e_end_time =='':
        return  JsonResponse({'status':10021,'message':'parameter error'})
    result =Event.objects.filter(id=e_id)
    if result :
        return  JsonResponse({'status':10022,'message':'event id  is exists'})#返回json格式的response
    result =Event.objects.filter(title=e_title)
    if result:
        return  JsonResponse({'status':10023,'message':'event title  is exists'})
    if e_status =='':
        e_status =1
    #添加数据
    try:
        Event.objects.create(id=e_id, title=e_title, limit=e_limit, status=e_status, address=e_address,
                             start_time=e_start_time, end_time=e_end_time)
    except ValidationError as e:
        error = 'time format wrong '
        return JsonResponse({'status':10024,'message':error})
    return JsonResponse({'status':200,'message':'add event success'})

#add event search interface

def add_event_search(request):
    e_id =request.GET.get('e_id','')
    print(type(e_id))
    e_title = request.GET.get('e_title','')
    if e_id == '' and e_title == '':
        return  JsonResponse({'status':10021,'mesage':'parameter error'})
    if e_id !='':
        event ={}
        try:
            result =Event.objects.get(id=e_id)
        except ObjectDoesNotExist:
            return  JsonResponse({'status':10022,'message':'query is empty'})
        else:
            event['title']=result.title
            event['limit']=result.limit
            event['status']=result.status
            event['address']=result.address
            event['start_time']=result.start_time
            event['end_time']=result.end_time
            return  JsonResponse({'status':200,'message':'success','data':event})
    if e_title!='':
        datas=[]
        results=Event.objects.filter(title__contains=e_title)
        if results :
            for result in results:
                event={}
                event['title'] = result.title
                event['limit'] = result.limit
                event['status'] = result.status
                event['address'] = result.address
                event['start_time'] = result.start_time
                event['end_time'] = result.end_time
                datas.append(event)
            return JsonResponse({'status':200,'message':'success','data':datas})

        else:
            return JsonResponse({'status': 10022, 'message': 'query is empty'})



################# add Guest Interface
@csrf_exempt
def add_guest(request):
    e_id =request.POST.get('e_id','')
    print('e_id: ',e_id)
    p_name=request.POST.get('p_name','')
    p_phone =request.POST.get('p_phone','')
    p_e_mail =request.POST.get('p_e_mail','')
    if e_id ==''or p_name =='' or p_phone =='' or p_e_mail=='':
        return JsonResponse({'status':10021,'message':'parameter error'})
    result =Event.objects.filter(id=e_id)
    if not  result :
        return  JsonResponse({'status':10022,'message':'event id is not exist'})
    result =Event.objects.get(id=e_id).status #获取发布会的状态
    if not result :
        return  JsonResponse({'status':10023,'message':'event status is not available'})

    event_limit =Event.objects.get(id=e_id).limit #获取发布会签到的人数限制
    guest_limit =Guest.objects.filter(id=e_id,p_sign=True).count() #已经签到的嘉宾数
    if guest_limit>event_limit:
        return JsonResponse({'status':10024,'message':'member sign full'})
    event_time =Event.objects.get(id=e_id).start_time #发布会时间
    e_time =str(event_time).split('.')[0]
    time_arry = time.strptime(e_time,"%Y-%m-%d %H:%M:%S")
    e_time =int(time.mktime(time_arry))

    now_time =str(time.time())
    ntime =now_time.split('.')[0]
    n_time =int(ntime)
    if n_time >e_time:
        return  JsonResponse({'status':10025,'message':'time has started'})
    try:
        Guest.objects.create(event_id=int(e_id),p_name=p_name,p_phone=int(p_phone),p_e_mail=p_e_mail,p_sign=0)
    except IntegrityError:
        return JsonResponse({'status':10026,'message':'phone repeat'})
    return  JsonResponse({'status':200,'message':'add guess success'})

def add_guest_search(request):
    e_id =request.GET.get('e_id','')
    p_phone =request.GET.get('p_phone','')
    if e_id == '' :
        return JsonResponse({'status':10021,'message':'event id must not be empty'})
    if e_id !='' and p_phone =='':
        datas =[]
        results =Guest.objects.filter(event=e_id)
        if results:
            for result in results:
                guest={}
                guest['p_name']=result.p_name
                guest['p_phone']=result.p_phone
                guest['p_e_mail']=result.p_e_mail
                guest['p_sign']=result.p_sign
                datas.append(guest)
            return  JsonResponse({'status':200,'message':'query success','data':datas})
        else:
            return  JsonResponse({'status':10022, 'message':'query result is empty'})
    if e_id !='' and p_phone !='':
        guest ={}
        try:
            result =Guest.objects.get(event_id=e_id,p_phone=p_phone)
        except ObjectDoesNotExist:
            return  JsonResponse({'status':10023,'message':'query result empty'})
        else:
            guest['p_name'] = result.p_name
            guest['p_phone'] = result.p_phone
            guest['p_e_mail'] = result.p_e_mail
            guest['p_sign'] = result.p_sign
            return  JsonResponse({'status':200,'message':'query success','data':guest})
