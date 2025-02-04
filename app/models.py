from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=100, unique=True)
    password = fields.CharField(max_length=128)
    status = fields.CharField(max_length=20, default="user")

    class Meta:
        table = "users"

class Product(Model):
    id = fields.IntField(pk=True)
    seller = fields.ForeignKeyField("models.User", related_name="products")
    name = fields.CharField(max_length=100)
    price = fields.FloatField()
    city = fields.CharField(max_length=50)
    stock = fields.IntField()

    class Meta:
        table = "products"

class Order(Model):
    id = fields.IntField(pk=True)
    product = fields.ForeignKeyField("models.Product", related_name="orders")
    user = fields.ForeignKeyField("models.User", related_name="orders")
    quantity = fields.IntField()
    status = fields.CharField(max_length=20, default="pending")
    total_price = fields.FloatField()

    class Meta:
        table = "orders"

class Post(Model):
    id = fields.IntField(pk=True)
    product: fields.ForeignKeyRelation[Product] = fields.ForeignKeyField("models.Product", related_name="posts")
    link = fields.CharField(max_length=255)
    description = fields.TextField()
    type = fields.CharField(max_length=50)  # "image" ou "video"

