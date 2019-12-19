from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Theme(models.Model):
    theme_title = models.CharField(max_length=50)
    TYPE_CHOICES = (('ST', 'Sub_theme'),('MT', 'Main_theme'))
    theme_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_CHOICES[0]) #0이면 sub_theme, 1이면 main_theme

    def __str__(self):
        return str(str(self.theme_title) + " /  "+str(self.theme_type))

class Post(models.Model):
    #post된 news들

    title = models.CharField(max_length=200)
    text = models.TextField()
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, null=True, blank=True)
    temp_theme = models.CharField(max_length=50, null=True, blank=True)
    author = models.CharField(max_length=200)

    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    prating = models.ManyToManyField(User, through='Rating', default=None)
    #없는 값을 default 0하는게 맞나?

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.title)



#필요 없다.
class Recommand(models.Model):
    #추천하는 기사들
    recomm_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    recomm_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(str(self.recomm_user) + " / "+str(self.recomm_post))

class Rating(models.Model):
    rating_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating_users', null=True) # 현재 사용자
    rating_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    # on_delete = models.CASADE 는 foreign key 가 삭제되면 이걸 들고 있는 데이터가 싹 사라짐

    GRADE_CHOICES = ((1, '1'), (2, '2'), (3,'3'), (4,'4'), (5,'5'))
    rating_grade = models.IntegerField(choices=GRADE_CHOICES, default=GRADE_CHOICES[4]) #get_rating_grade_disply로 html에서 볼 수 있음
    rating_direct = models.BooleanField(default=False)
    rating_date = models.DateTimeField(default=timezone.now)
    rating_grade_expect = models.FloatField(default=None, null=True, blank=True)
    
    #필요 없을듯
    def rating_save(self):
        self.save()

    def __str__(self):
        return str(str(self.rating_user) + " / " +str(self.rating_post) +" : "+ str(self.rating_grade))