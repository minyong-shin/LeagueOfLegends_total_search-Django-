from django.db import models
from django.utils import timezone
# Create your models here.
#리그오브레전드 전적검색
#모델의속성을 정의하는 것에 대해서 써준다.즉,속성을 정의하기
#위해서 필드마다 어떤 종류의 데이터 타입을 가지는지 정해야 함
#dtype에는 text, num, date, user등의 객체 참조가 있음

#아래의 모델 정의는 blog의 객체 정의를 하기 위한 과정이다.
#class는 객체를 정의해주는 것
class Post(models.Model): #models는 post가 장고 모델임을 의미
    #따라서 models라는 코드 때문에 장고는 post가 db에 저장되어야 한다고 알게 됨
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    #위와 같이 모델을 객체 정의한 이후에 db에 모델을 위해서
    #테이블을 만들어야 한다. 즉, post모델을 추가 해야한다.

