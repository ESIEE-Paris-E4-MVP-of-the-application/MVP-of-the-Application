#coding=utf-8 !!! if there are any problems of the URL.
# please check the coding for now it's should be utf-8
# before you run the mocking code please make sure your database setting is correct
# to run this test code in Terminal Django Console :
# from utils.loaddata import *
# test_model()
from goodsapp.models import *
from django.db.transaction import atomic
@atomic
def test_model():
    with open('utils/mockinggoods.json') as fr:
        import json
        datas = json.loads(fr.read())
        for data in datas:

            # A object category
            cate = Category.objects.create(cname=data['category'])

            _goods = data['goods']

            # Create the entity for goods
            for goods in _goods:
                good = Goods.objects.create(gname=goods['goodsname'], gdesc=goods['goods_desc'],
                                            price=goods['goods_price'], oldprice=goods['goods_oldprice'],
                                            category=cate)
                weights = []
                for _weight in goods['weights']:
                    if Weight.objects.filter(wname=_weight[0]).count() == 1:
                        weight = Weight.objects.get(wname=_weight[0])
                    else:
                        weight = Weight.objects.create(wname=_weight[0])
                        weights.append(weight)

                conditions = []
                for _condition in goods['conditions']:
                    condition = Condition.objects.create(conditionname=_condition[0], conditionurl=_condition[1])
                    conditions.append(condition)

                for _spec in goods['specs']:
                    goodsdetails = GoodsDetailName.objects.create(gdname=_spec[0])
                    for img in _spec[1]:
                        GoodDetail.objects.create(goods=good,goodsdname=goodsdetails,gdurl=img)
                for c in conditions:
                    for w in weights:
                        Inventory.objects.create(count=100,goods=good, condition=c, weight=w)

def deleteall():
    Category.objects.filter().delete()
    Condition.objects.filter().delete()
    Weight.objects.filter().delete()

