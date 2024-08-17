from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import Product, Order, Payment
from django.contrib.auth.models import User
from myauth.models import Profile
from basket.service import Cart
from django.contrib.sessions.middleware import SessionMiddleware


class ProductDetailViewTestCase(TestCase):
    fixtures = [
        "catalog/fixtures/categories_fixtures.json",
        "review_fixtures.json",
        "tag_fixtures.json",
        "product_fixtures.json",
        "product_fixtures.json",
    ]

    def test_product_view(self):
        response = self.client.get(reverse("shopapp:product", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Iphone")

    def test_product_view_reviews(self):
        data = {"author": "George", "email": "dv@inbox.ru", "text": "Hie ", "rate": 5}
        response = self.client.post(
            reverse("shopapp:product_review", args=[1]), data=data
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["author"], response.data["author"])


class TagsViewTestCase(TestCase):
    fixtures = [
        "tag_fixtures.json",
    ]

    def test_tags_view(self):
        response = self.client.get(reverse("shopapp:tags"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)


class OrderPostViewTestCase(TestCase):
    fixtures = [
        "payment_fixtures.json",
    ]

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username="test11", password="1")
        cls.product = Product.objects.create(
            title="Iphone",
            price=1500,
            count=40,
        )

        cls.profile = Profile.objects.create(
            email="dvl@inbox.ru", fullName="Gigs", phone="86579875645", user_id=1
        )
        cls.order = Order.objects.create(
            id=1,
            fullName="order",
            email="ddsa@inbox.ru",
            phone="89356576543",
            deliveryType=True,
            paymentType=True,
            totalCost="200",
            status="processing",
            city="",
            profile_id=1,
        )

        cls.order.product.add(cls.product)
        cls.order.save()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.profile.delete()
        cls.order.delete()

    def setUp(self):
        self.client.force_login(self.user)
        self.request = RequestFactory().get("/")
        middleware = SessionMiddleware(lambda x: x)
        middleware.process_request(self.request)
        self.request.session["cart"] = {1: {"count": 4}}
        self.request.session.save()

    def test_order_view_get(self):
        response = self.client.get(reverse("shopapp:orders"))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data[0]["fullName"], self.order.fullName)

    def test_order_view_post(self):
        response = self.client.post(reverse("shopapp:orders"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"order_id": 2})

    def test_order_details_post(self):
        data = {
            "paymentType": True,
            "deliveryType": True,
            "city": "Moscow",
            "address": "Lenina",
        }
        response = self.client.post(
            reverse("shopapp:orders_details", args=[1]), data=data
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data[0]["fullName"], self.order.fullName)

    def test_order_details_get(self):
        response = self.client.post(reverse("shopapp:orders_details", args=[1]))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data[0]["fullName"], self.order.fullName)

    # def test_payments_post(self):
    #     cart = Cart(self.request)
    #
    #     data = {
    #         'number': '324214124124124',
    #         'name': "George",
    #         "month": '06',
    #         "year": '2021',
    #         "code": '123',
    #
    #
    #     }
    #
    #     response = self.client.post(reverse("shopapp:payment", args=[1]), data=data)
    #
    #
    #     self.assertEqual(response.status_code, 200)
