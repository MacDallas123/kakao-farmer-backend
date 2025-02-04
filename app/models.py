from tortoise import fields, Model
from enum import Enum

class UserType(str, Enum):
    CLIENT = "client"
    CACAOCULTEUR = "cacaoculteur"
    ADMIN = "admin"

class User(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    type = fields.CharEnumField(UserType)
    notifications = fields.ReverseRelation["Notification"]  # Defines a reverse relation to Notification model
    transactions = fields.ReverseRelation["Transaction"]  # Defines a reverse relation to Transaction model
    products = fields.ReverseRelation["Product"]  # Defines a reverse relation to Product model
    posts_likes = fields.ManyToManyField("models.Post", related_name="likes", through="like")

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

