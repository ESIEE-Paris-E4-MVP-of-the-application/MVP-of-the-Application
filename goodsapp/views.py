from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.views import View

from goodsapp.models import Category, Goods


class IndexView(View):
    def get(self,request,cid=2):

        cid = int(cid)
        categoryList = Category.objects.all()
        goodsList = Goods.objects.filter(category_id=cid)
        return render(request,'index.html',{'categoryList':categoryList,'cid':cid,'goodsList':goodsList})