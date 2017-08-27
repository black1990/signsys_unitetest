from django.test import TestCase
from .models import Guest,Event
from  django.contrib.auth.models import  User
from django.test import Client
# Create your tests here.
#model测试
class ModelTest(TestCase):
    def setUp(self):
        Event.objects.create(
            id=1,title='发布model单元测试',limit=2000,status=True,address='自己',
            start_time='2017-08-16 08:00',
            end_time='2017-08-16 12:00'
        )
        Guest.objects.create(
            id=1,event_id=1,p_name='测试',p_phone='110120',p_e_mail='ces@qq.com',
            p_sign='False'
                             )
    def test_event(self):
        result = Event.objects.get(title='发布model单元测试')
        self.assertEqual(result.address,'自己')
        self.assertTrue(result.status)
    def test_guest(self):
        result =Guest.objects.get(p_phone='110120')
        self.assertEqual(result.p_name,'测试')
        self.assertFalse(result.p_sign)
##########测试index登录页面
class IndexPageTest(TestCase):
    def test_index_page_render_template(self):
        '''测试视图'''
        response = self.client.get('/')
        #是否响应为200
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'sign/index.html')
#登录测试
class Login_Test(TestCase):

        def setUp(self):
            #创建登录用户
            User.objects.create_user(
                username='evan',email='evan@qq.com',password='sx564312974'
            )
            #创建Client ，提供get /post 请求
            self.c = Client()
         #用户名密码为空测试
        def test_username_password_null(self):
            test_data={'username':'','password':''}
            response = self.c.post('/login_action/',test_data)
            self.assertEqual(response.status_code,200)
            self.assertIn(b'wrong',response.content)

        def test_username_password_wrong(self):
            test_data={'username':'abc','password':123}
            response = self.c.post('/login_action/',test_data)
            self.assertEqual(response.status_code,200)
            self.assertIn(b'wrong',response.content)

        def test_username_password_success(self):
            test_data ={'username':'evan','password':'sx564312974'}
            response =self.c.post('/login_action/',data=test_data)
            self.assertEqual(response.status_code,302)

#Event_manage发布会管理测试

class EventManageTest(TestCase):
     '''必须注销@login_required方法'''
     def setUp(self):
         Event.objects.create(
             id=1, title='event_test', limit=200, status=True, address='local',
             start_time='2017-08-19 08:00',
             end_time='2017-08-19 12:00'
         )
         self.c=Client()
     def test_event_manage_success(self):
              '''测试发布会：fabuhui1'''
              response= self.c.post('/event_manage/')
              self.assertEqual(response.status_code,200)
              self.assertIn(b'event_test',response.content)
              self.assertIn(b'local',response.content)
              result =Event.objects.get(title='event')
              self.assertTrue(result.status)
     def test_event_search_success(self):
             '''测试发布会搜索'''
             response = self.c.post('/event_search/',{'title':'event_test'})
             self.assertEqual(response.status_code,200)
             self.assertIn(b'event_test',response.content)
             self.assertIn(b'local', response.content)

#嘉宾管理
class GuestManageTest(TestCase):
    def setUp(self):
        Event.objects.create(id=1, title='test', limit=200, status=True, address='test',
             start_time='2017-08-19 08:00',
             end_time='2017-08-19 12:00'
                             )
        Guest.objects.create(
            event_id=1,p_name='guest_test',p_phone='110120',p_e_mail='test@qq.com',
            p_sign=False
        )
        self.c =Client()
        #嘉宾信息测试
    def test_guest_manage_success(self):
         response= self.c.post('/guest_manage/')
         self.assertEqual(response.status_code,200)
         self.assertIn(b'guest_test',response.content)
         self.assertIn(b'110120',response.content)
    def test_guest_search_success(self):
         response=self.c.post('/guest_search/',{'p_name':'guest_test'})
         self.assertEqual(response.status_code,200)
         self.assertIn(b'guest_test',response.content)
         self.assertIn(b'110120',response.content)

#签到测试
class SignTest(TestCase):
    '''发布会签到'''
    def setUp(self):
        Event.objects.create(id=3, title='sign_test', limit=200, status=True, address='sign_test',
                             start_time='2017-08-20 11:00',end_time='2017-08-20 12:00')
        Event.objects.create(id=4, title='sign_test1', limit=200, status=True, address='sign_test1',
                             start_time='2017-08-20 13:00',
                             end_time='2017-08-20 17:00'
                             )

        Guest.objects.create(
            event_id=3,p_name='guest1',p_phone='1234',p_e_mail='guest1@qq.com',
            p_sign=0
        )
        Guest.objects.create(
            event_id=4,p_name='guest2',p_phone='5678',p_e_mail='guest2@qq.com',
            p_sign=1
        )
        self.c=Client()
    def test_sign_phone_null(self):
        '''手机号为空'''
        response =self.c.post('/event_sign/3',{'p_phone':''})
        self.assertEqual(response.status_code,200)
        self.assertIn(b'phone not exist',response.content)
    def test_sign_phone_or_id_wrong(self):
        '''phone or id wrong'''
        response=self.c.post('/event_sign_action/4/',{'p_phone':'1234'})
        self.assertEqual(response.status_code,200)
        self.assertIn(b'phone or id wrong',response.content)
    def test_sign_phone_already_sign(self):
        '''user is already sign'''
        response =self.c.post('/event_sign_action/4/',{'p_phone':'5678'})
        self.assertEqual(response.status_code,200)
        self.assertIn(b'user is already sign',response.content)

    def test_sign_phone_success(self):
        '''sign access'''
        response =self.c.post('/event_sign_action/3/',{'p_phone':'1234'})
        self.assertEqual(response.status_code,200)
        self.assertIn(b'sign access',response.content)



#python manage.py test （测试整个项目）
#指定模块  python manage.py  test sign  (运行sign 目录 下的所有测试)
#python manage.py test sign.tests (运行sign目录tests.py)
#python manage.py test sign.tests.ModelTest
#python manage.py test sign.tests.ModelTest.test_event

#python manage.py test -p test*.py (模糊匹配以test开头.py结尾的)

