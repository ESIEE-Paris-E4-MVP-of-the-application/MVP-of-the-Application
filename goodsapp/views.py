from __future__ import unicode_literals

from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from django.views import View

from goodsapp.models import Category, Goods


class IndexView(View):
    def get(self,request,cid=2,num = 1):
        num = int(num)
        cid = int(cid)
        categoryList = Category.objects.all()
        goodsList = Goods.objects.filter(category_id=cid)

        # 8 objects per page
        paginator_obj = Paginator(goodsList,8)

        #get the data of one page
        paginator_obj.page(num)
        return render(request,'index.html',{'categoryList':categoryList,'cid':cid,'goodsList':goodsList})