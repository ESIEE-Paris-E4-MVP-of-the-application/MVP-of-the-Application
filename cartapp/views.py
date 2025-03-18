# coding=utf-8

from collections import OrderedDict
from models import *
from django.db.models import F
import jsonpickle


class CartManager(object):
    def add(self, goodsid, conditionid, weightid, count, *args, **kwargs):
        '''Add an item to the cart. If the item already exists, update its quantity (self.update()), otherwise add it to the cart.'''
        pass

    def delete(self, goodsid, conditionid, weightid, *args, **kwargs):
        '''Delete an item from the cart.'''
        pass

    def update(self, goodsid, conditionid, weightid, count, step, *args, **kwargs):
        '''Update an item's quantity, increasing or decreasing it.'''
        pass

    def queryAll(self, *args, **kwargs):
        ''':return CartItem List of cart items.'''
        pass


# User not logged in
class SessionCartManager(CartManager):
    cart_name = 'cart'

    def __init__(self, session):
        self.session = session
        # Create a cart {cart:{key1:cartitem, key2:cartitem}}
        if self.cart_name not in self.session:
            self.session[self.cart_name] = OrderedDict()

    def __get_key(self, goodsid, conditionid, weightid):
        return goodsid + ',' + conditionid + ',' + weightid

    def add(self, goodsid, conditionid, weightid, count, *args, **kwargs):
        # Get the unique identifier for the cart item
        key = self.__get_key(goodsid, conditionid, weightid)

        # If the item is already in the session cart, update it; otherwise, add it
        if key in self.session[self.cart_name]:
            self.update(goodsid, conditionid, weightid, count, *args, **kwargs)
        else:
            self.session[self.cart_name][key] = jsonpickle.dumps(
                CartItem(goodsid=goodsid, conditionid=conditionid, weightid=weightid, count=count))

    def delete(self, goodsid, conditionid, weightid, *args, **kwargs):
        key = self.__get_key(goodsid, conditionid, weightid)
        if key in self.session[self.cart_name]:
            del self.session[self.cart_name][key]

    def update(self, goodsid, conditionid, weightid, step, *args, **kwargs):
        key = self.__get_key(goodsid, conditionid, weightid)
        if key in self.session[self.cart_name]:
            cartitem = jsonpickle.loads(self.session[self.cart_name][key])
            cartitem.count = int(str(cartitem.count)) + int(step)
        else:
            raise Exception('Error in update method of SessionCartManager')

    def queryAll(self, *args, **kwargs):
        cart_items_serialized = self.session[self.cart_name].values()
        return [jsonpickle.loads(item) for item in cart_items_serialized]

    def migrateSession2DB(self):
        if 'user' in self.session:
            user = jsonpickle.loads(self.session.get('user'))
            for cartitem in self.queryAll():
                if CartItem.objects.filter(goodsid=cartitem.goodsid, conditionid=cartitem.conditionid,
                                           weightid=cartitem.weightid).count() == 0:
                    cartitem.user = user
                    cartitem.save()
                else:
                    item = CartItem.objects.get(goodsid=cartitem.goodsid, conditionid=cartitem.conditionid,
                                                weightid=cartitem.weightid)
                    item.count = int(item.count) + int(cartitem.count)
                    item.save()
            del self.session[self.cart_name]


# User logged in
class DBCartManager(CartManager):
    def __init__(self, user):
        self.user = user

    def add(self, goodsid, conditionid, weightid, count, *args, **kwargs):
        if self.user.cartitem_set.filter(goodsid=goodsid, conditionid=conditionid, weightid=weightid).count() == 1:
            self.update(goodsid, conditionid, weightid, count, *args, **kwargs)
        else:
            CartItem.objects.create(goodsid=goodsid, conditionid=conditionid, weightid=weightid, count=count, user=self.user)

    def delete(self, goodsid, conditionid, weightid, *args, **kwargs):
        self.user.cartitem_set.filter(goodsid=goodsid, conditionid=conditionid, weightid=weightid).update(count=0, isdelete=True)

    def update(self, goodsid, conditionid, weightid, step, *args, **kwargs):
        self.user.cartitem_set.filter(goodsid=goodsid, conditionid=conditionid, weightid=weightid).update(
            count=F('count') + int(step), isdelete=False)

    def queryAll(self, *args, **kwargs):
        return self.user.cartitem_set.order_by('id').filter(isdelete=False).all()

    # Retrieve a CartItem object based on goodsid, weightid, and conditionid
    def get_cartitems(self, goodsid, weightid, conditionid, *args, **kwargs):
        return self.user.cartitem_set.get(goodsid=goodsid, weightid=weightid, conditionid=conditionid)


# Factory method
# Returns the appropriate CartManager object based on the user's login status
def getCartManager(request):
    if request.session.get('user'):
        # User is logged in
        return DBCartManager(jsonpickle.loads(request.session.get('user')))
    return SessionCartManager(request.session)
