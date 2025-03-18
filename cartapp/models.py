from django.db import models

# Create your models here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from goodsapp.models import Condition,Goods, Weight
from userapp.models import UserInfo
import math


class CartItem(models.Model):
    goodsid=models.PositiveIntegerField()
    conditionid=models.PositiveIntegerField()
    weightid=models.PositiveIntegerField()
    count=models.PositiveIntegerField()
    isdelete=models.BooleanField(default=False)
    user=models.ForeignKey(UserInfo)

    def getColor(self):
        return Condition.objects.get(id=self.conditionid)

    def getGoods(self):
        return Goods.objects.get(id=self.goodsid)

    def getweight(self):
        return Weight.objects.get(id=self.weightid)

    def getTotalPrice(self):
        return math.ceil(int(self.count) * self.getGoods().price)




