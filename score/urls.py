from django.urls import path
from . import views
 
app_name = 'score'    #score 어플리케이션의 url 호출시 앞의 구분자 사용을 하시려면 작성합시다.
 
urlpatterns = [
    path('post/<int:pk>',views.post_detail,name='post_detail'),
    path('post_list',views.post_list,name='post_list'),
    path('new',views.post_new, name='post_new'),
    path('', views.score_view, name='score_view'),            #검색창 메인 화면
    path('search_result', views.search_result, name='search_result'),    #검색결과를 보여줄 화면
]