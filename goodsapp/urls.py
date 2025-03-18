from django.urls import path
from goodsapp import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),  # 主页
    path('category/<int:cid>/', views.IndexView.as_view(), name='category'),  # 分类
]

