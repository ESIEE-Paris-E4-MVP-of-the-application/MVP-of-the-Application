from __future__ import unicode_literals
from django.db import models

# The Django ORM will create those form base on the code.
class Category(models.Model):
    cname =  models.CharField(max_length=10)


    def __unicode__(self):
        return u'<Category:%s>' % self.cname

class Goods(models.Model):
    gname = models.CharField(max_length=100,unique=True)
    # Description of goods.
    gdesc = models.CharField(max_length=100)
    oldprice = models.DecimalField(max_digits=5,decimal_places=2)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __unicode__(self):
        return u'<Goods:%s>'%self.gname

class GoodsDetailName(models.Model):
    gdname = models.CharField(max_length=30)

class GoodDetail(models.Model):
    # This is the url of the image. And for now it comes from the media
    gdurl= models.ImageField(upload_to='')
    # A good could have a lot of information so there is a key to link the Detail
    goodsdname = models.ForeignKey(GoodsDetailName,on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE)

class Weight(models.Model):
    wname = models.CharField(max_length=10)


class Condition(models.Model):
    conditionname = models.CharField(max_length=10)
    conditionurl = models.ImageField(upload_to='conditions/')

class Inventory(models.Model):
    count = models.PositiveIntegerField(default=100)
    condition = models.ForeignKey(Condition,on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE)
    # Not sure that we want this or not
    weight = models.ForeignKey(Weight,on_delete=models.CASCADE)
