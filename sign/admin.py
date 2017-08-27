from django.contrib import admin
from  sign.models import  Event,Guest
# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ['title','status','start_time','end_time','id']
    search_fields = ['title']#搜索栏
    list_filter = ['status']#过滤

class GuestAdmin(admin.ModelAdmin):
    list_display = ['p_name','p_phone','p_e_mail','p_sign','p_sign_time']
    search_fields = ['p_name','p_phone']
    list_filter = ['p_sign']
admin.site.register(Event,EventAdmin)
admin.site.register(Guest,GuestAdmin)