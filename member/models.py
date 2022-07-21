from django.db import models
# member/models.py
# Create your models here.
#
# anaconda prompt 창
# python manage.py makemigrations => db에 model 적용
# python manage.py migrate
# db에 member_member 테이블 생성 확인

class Member(models.Model) :  #db에 테이블이 생성. db 연결완료
    id = models.CharField(max_length=20,primary_key=True) #기본키
    pass1 = models.CharField(max_length=20)    #varchar(20)
    name = models.CharField(max_length=20)
    gender= models.IntegerField(default=0)
    tel = models.CharField(max_length=20)    
    email = models.CharField(max_length=100)        
    picture = models.CharField(max_length=200)        
    
    def __str__(self) :
        return self.id + ":" + self.name + ":" + self.pass1