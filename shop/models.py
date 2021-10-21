from django.db import models
from django.db.models.fields.json import JSONField

# Create your models here.

class Product(models.Model):
    product_id = models.AutoField
    product_name =  models.CharField(max_length=50)
    short_desc=models.CharField(max_length=50, default='')
    long_desc=models.CharField(max_length=600, default='')
    pub_date = models.DateField()
    category = models.CharField(max_length=50, default='')
    sub_category = models.CharField(max_length=50, default='')
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to="shop/images", default="")
    colour = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="")
    e_mail = models.CharField(max_length=50, default="")
    message = models.CharField(max_length=300, default="")

    def __str__(self):
        return self.e_mail

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    array = models.JSONField(default=dict)
    price = models.IntegerField(default=0)
    name = models.CharField(max_length=300, default='')
    address = models.CharField(max_length=600, default='')
    e_mail = models.CharField(max_length=400, default='')
    city = models.CharField(max_length=70, default='')
    state = models.CharField(max_length=70, default='')
    zip = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.e_mail

class OtherUserDetails(models.Model):
    email = models.CharField(primary_key=True, unique=True, max_length=60)
    mobile = models.CharField(max_length=11)
    age = models.IntegerField(default=13)
