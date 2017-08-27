from django.db import models

# Create your models here.
class  Event(models.Model):
    title = models.CharField(max_length=100,verbose_name='发布会标题')
    limit = models.IntegerField(verbose_name='限制人数')
    status = models.BooleanField(verbose_name='状态')
    address = models.CharField(max_length=200,verbose_name='地址')
    start_time = models.DateTimeField(verbose_name='发布会时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    def __str__(self):
        return  self.title
    class Meta:
        verbose_name='发布会信息'
        verbose_name_plural=verbose_name

class Guest(models.Model):
    event =models.ForeignKey(Event)
    p_name = models.CharField(max_length=50,verbose_name='姓名')
    p_phone =models.CharField(max_length=16,verbose_name='手机号')
    p_e_mail= models.EmailField(verbose_name='邮箱')
    p_sign = models.BooleanField(verbose_name='签到状态')
    p_sign_time = models.DateTimeField(auto_now=True,verbose_name='自动获取签到时间')

    def __str__(self):
        return  self.p_name

    class Meta:
        # phone event 唯一
        unique_together =['event','p_phone']
        verbose_name='嘉宾'
        verbose_name_plural=verbose_name
