from django.urls import path
from goodsapp import views

#
urlpatterns = [
    path(r'^$', views.IndexView.as_view),
    path(r'^category/(?P<cid>\d+)$', views.IndexView.as_view()),
]
