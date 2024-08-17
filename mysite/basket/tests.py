from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from .service import Cart
from shopapp.models import Product


class BasketViewTestCaseWithoutLogin(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.first_product = Product(pk=1, title="Phone", count=4)

        cls.second_product = Product(pk=2, title="Ipad", count=3)

    @classmethod
    def tearDownClass(cls):
        cls.first_product.delete()
        cls.second_product.delete()

    def setUp(self):
        self.request = RequestFactory().get("/")
        middleware = SessionMiddleware(lambda x: x)
        middleware.process_request(self.request)
        self.request.session["cart"] = {"1": {"count": 2}}
        self.request.session.save()

    def test_basket_view_post(self):
        cart = Cart(self.request)

        cart.add(product=self.first_product, count=2)
        cart.add(product=self.second_product, count=3)

        self.assertEqual(cart.cart, {"1": {"count": 4}, "2": {"count": 3}})

    def test_basket_view_get(self):
        cart = Cart(self.request)

        self.assertEqual(
            cart.cart,
            {
                "1": {"count": 2},
            },
        )

    def test_basket_view_delete(self):
        cart = Cart(self.request)

        cart.remove(product=self.first_product, count=1)

        self.assertEqual(cart.cart, {"1": {"count": 1}})
