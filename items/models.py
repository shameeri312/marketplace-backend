from django.db import models


from django.db import models
from django.db.models import JSONField
from django.contrib.auth import get_user_model

User = get_user_model()


class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
    ad_title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    currency = models.CharField(max_length=10, default="PKR")

    # Category as an array (PostgreSQL required)
    category = models.CharField(max_length=255)

    # Address Fields
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)

    # Image fields
    image1 = models.ImageField(upload_to="items/", blank=True, null=True)
    image2 = models.ImageField(upload_to="items/", blank=True, null=True)
    image3 = models.ImageField(upload_to="items/", blank=True, null=True)

    # Specifications as JSON
    specifications = JSONField(blank=True, null=True)

    # Keywords as an array
    keywords = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ad_title
