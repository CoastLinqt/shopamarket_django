from django.test import TestCase
from django.urls import reverse
from shopapp.models import Product
from .models import Categories


class CategoriesViewTestCase(TestCase):
    fixtures = [
        "categories_fixtures.json",
    ]

    def test_categories(self):

        response = self.client.get(reverse("catalog:categories"))
        categories = Categories.objects.filter(parent=None)
        expected_data = [
            {
                "id": cat.pk,
                "title": cat.title,
                "image": {"src": f"/media/{cat.image.name}", "alt": cat.image.name},
                "subcategories": [
                    {
                        "id": sub.pk,
                        "title": sub.title,
                        "image": {"src": f"/media/{sub.image.name}", "alt": sub.image},
                    }
                    for sub in cat.subcategories.all()
                ],
            }
            for cat in categories
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(expected_data, response.data)


class CatalogViewTestCase(TestCase):

    fixtures = ['categories_fixtures.json',
                'shopapp/fixtures/tag_fixtures.json',
                'shopapp/fixtures/product_fixtures.json',]

    def test_catalog(self):
        data = {'filter[name]': 'Iphone',
                'filter[minPrice]': 0,
                'filter[maxPrice]': 10000,
                'filter[freeDelivery]': True,
                'filter[available]': True,
                'sort': "date",
                'sortType': "dec",
                'limit': 20,
                }

        header = {"HTTP_REFERER": 'http://127.0.0.1:8000/catalog/1/'}

        response = self.client.get(reverse("catalog:catalog"), data=data, **header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.data['items'][0]['title']), 'Iphone')
        self.assertEqual(len(response.data['items']), 1)


class CatalogPopularViewTestCase(TestCase):
    fixtures = [
        "categories_fixtures.json",
        "shopapp/fixtures/review_fixtures.json",
        "shopapp/fixtures/tag_fixtures.json",
        "shopapp/fixtures/product_fixtures.json",
    ]

    def test_popular_catalog(self):
        response = self.client.get(reverse("catalog:catalog_popular"))

        product = Product.objects.all()[0]

        expected_data = product.pk

        product_data = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(product_data[0]["pk"], expected_data)


class CatalogLimitedViewTestCase(TestCase):
    fixtures = [
        "categories_fixtures.json",
        "shopapp/fixtures/review_fixtures.json",
        "shopapp/fixtures/tag_fixtures.json",
        "shopapp/fixtures/product_fixtures.json",
    ]

    def test_limit_view(self):
        response = self.client.get(reverse("catalog:catalog_limited"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)


class BannersViewTestCase(TestCase):
    fixtures = [
        "categories_fixtures.json",
        "shopapp/fixtures/review_fixtures.json",
        "shopapp/fixtures/tag_fixtures.json",
        "shopapp/fixtures/product_fixtures.json",
    ]

    def test_banners_view(self):
        response = self.client.get(reverse("catalog:banners"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)


class CatalogSalesTestCase(TestCase):
    fixtures = [
        "categories_fixtures.json",
        "shopapp/fixtures/review_fixtures.json",
        "shopapp/fixtures/tag_fixtures.json",
        "shopapp/fixtures/product_fixtures.json",
        "shopapp/fixtures/productimage_fixtures.json",
        "shopapp/fixtures/sales_fixtures.json",
    ]

    def test_banners_view(self):
        response = self.client.get(reverse("catalog:sales"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["items"]), 1)
