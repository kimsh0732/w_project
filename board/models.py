from django.db import models

# Create your models here.
# board/models.py
# python manage.py makemigrations
# python manage.py migrate
# mariadb : board_board  테이블 생성 확인

class Board(models.Model):
    #num 값이 없으면, 자동증가함(auto_increments). 
    num = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    pass1 = models.CharField(max_length=20)
    subject = models.CharField(max_length=100)
    content = models.CharField(max_length=4000)
    regdate = models.DateTimeField()
    readcnt = models.IntegerField(default=0)
    file1 = models.CharField(max_length=100)

    def __str__(self):
        return str(self.num)+':' + self.subject