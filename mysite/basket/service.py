from django.conf import settings


class Cart:
    def __init__(self, request):

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        print(cart)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

        if "False" in [key for key in self.cart.keys()]:
            del self.cart["False"]

    def add(self, product, count):

        product_id = product.pk
        product_count_limit = product.count

        if str(product_id) not in self.cart:

            if product_count_limit < count:
                self.cart["False"] = False
            else:

                self.cart[str(product_id)] = {
                    "count": count,
                }

                if self.cart[str(product_id)].get("count") == 0:
                    del self.cart[str(product_id)]

        else:

            count_product_basket = self.cart[str(product_id)].get("count")
            if product_count_limit < count_product_basket + count:
                self.cart["False"] = False

            else:

                self.cart[str(product_id)] = {
                    "count": count_product_basket + count,
                }

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product, count):

        product_id = product.pk

        if str(product_id) in self.cart:
            count_product = self.cart[str(product_id)].get("count")

            if count_product - count <= 0:
                del self.cart[str(product_id)]
            else:
                self.cart[str(product_id)] = {
                    "count": count_product - count,
                }

        self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
