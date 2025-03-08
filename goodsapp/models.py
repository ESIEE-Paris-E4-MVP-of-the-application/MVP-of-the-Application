from django.db import models

# There is the table for the models.
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
    category = models.ForeignKey(Category)

    def __unicode__(self):
        return u'<Goods:%s>'%self.gname

class GoodsDetailName(models.Model):
    gdname = models.CharField(max_length=30)

class GoodDetail(models.Model):
    # This is the url of the image. And for now it comes from the media
    gdurl= models.ImageField(upload_to='')
    # A good could have a lot of information so there is a key to link the Detail
    goodsdname = models.ForeignKey(GoodsDetailName)
    goods = models.ForeignKey(Goods)

