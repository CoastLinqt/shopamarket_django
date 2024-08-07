from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from catalog.models import Categories
from myauth.models import Profile

def product_image_directory_path(instanse: 'ProductImage', filename: str) -> str:
    return 'products/images/product_{pk}/{filename}'.format(
        pk=instanse.pk,
        filename=filename
    )


class Product(models.Model):
    """Модель Product представляет товар,
    который можно продавать в интернет магазине.

    Заказы тут: :model:`catalog.Order`
    """

    class Meta:
        ordering = ["title", "price"]

    title = models.CharField(max_length=150, null=False, blank=False)
    description = models.TextField(null=False, blank=True, db_index=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2,
                                validators=[MinValueValidator(1),
                                            MaxValueValidator(100000000)])
    count = models.IntegerField(default=0, null=False)
    date = models.DateTimeField(auto_now_add=True, null=False)
    freeDelivery = models.BooleanField(default=True)
    limited = models.BooleanField(default=False)
    rating = models.DecimalField(default=0, max_digits=3, decimal_places=2,
                                 auto_created=True, blank=True)
    active = models.BooleanField(default=False)

    category = models.ForeignKey(Categories, on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 related_name='products')

    tags = models.ManyToManyField('Tag', blank=True, related_name='products')


    def __str__(self) -> str:
        return f"Product(pk={self.pk}, name={self.title!r})"


class Sales(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                related_name='sales')

    salePrice = models.IntegerField(default=0, null=True)
    dateFrom = models.DateTimeField(default='')

    dateTo = models.DateTimeField(blank=True, null=True)
    images = models.ForeignKey('ProductImage', on_delete=models.CASCADE, related_name='sales')


class Tag(models.Model):
    name = models.CharField(max_length=150, null=False, blank=True)

    def __str__(self) -> str:
        return self.name


class ProductImage(models.Model):
    name = models.CharField(max_length=200, null=False, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='images')
    image = models.FileField(upload_to=product_image_directory_path)


class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                related_name='specifications')
    name = models.CharField(max_length=250, default='')
    value = models.CharField(max_length=250, default='')


class Review(models.Model):
    author = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    text = models.TextField(default='')
    rate = models.PositiveSmallIntegerField(blank=False, default=5)
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                related_name='reviews',)

    def __str__(self) -> str:
        return f"{self.author}: {self.product.title}"


class Order(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    fullName = models.CharField(max_length=200, null=False, blank=True)
    email = models.EmailField(max_length=100, null=False)
    phone = models.CharField(max_length=20, blank=True)
    deliveryType = models.BooleanField(default=False)
    paymentType = models.CharField(max_length=20, null=True, blank=True)
    totalCost = models.DecimalField(default=0, max_digits=8, decimal_places=2,
                                    validators=[MinValueValidator(1),
                                                MaxValueValidator(100000000)])
    status = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    product = models.ManyToManyField(Product, related_name="orders")
    profile = models.ForeignKey(Profile, models.CASCADE, related_name="orders_profile",)

