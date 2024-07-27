from django.db import models
from django.core.validators import MinValueValidator


def product_preview_directory_path(instance: "Product", filename: str) -> str:

    return "products/product_{id}/preview/{filename}".format(
        id=instance.pk,
        filename=filename,
    )


class Product(models.Model):
    """Модель Product представляет товар,
    который можно продавать в интернет магазине.

    Заказы тут: :model:`shopapp.Order`
    """

    class Meta:
        ordering = ["name", "price"]

    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=False, blank=True, db_index=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2,
                                validators=[MinValueValidator(1)])

    created_at = models.DateTimeField(auto_now_add=True)

    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path,
                                )

    def __str__(self) -> str:
        return f"Product(pk={self.pk}, name={self.name!r})"