from django.db import models


def categories_preview_directory_path(instance: "Categories", filename: str) -> str:

    return "catalog/categories_{id}/{filename}".format(
        id=instance.pk,
        filename=filename,
    )


class Categories(models.Model):
    title = models.CharField(max_length=100, db_index=True, null=False)
    image = models.ImageField(null=True, blank=True, upload_to=categories_preview_directory_path)

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="subcategories")


