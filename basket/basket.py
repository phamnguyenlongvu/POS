from store.models import Product
from decimal import Decimal


class Basket:
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product, product_qty):
        product_id = str(product.id)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = product_qty
        else:
            self.basket[product_id] = {'price': float(product.price), 'qty': int(product_qty)}

        self.session.modified = True

    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        '''
        count thr qty item
        '''
        return sum(item['qty'] for item in self.basket.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    def delete(self, product):
        """
        Delete item form session data
        """
        product_id = str(product)
        if product_id in self.basket:
            del self.basket[product_id]
        self.session.modified = True

    def update(self, product, qty):
        product_id = str(product)
        qty = qty
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        self.session.modified = True



