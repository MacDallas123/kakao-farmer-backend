from tortoise import fields, Model


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=255, unique=True)
    username = fields.CharField(max_length=50, unique=True, null=True)
    password = fields.CharField(max_length=255)
    status = fields.CharField(max_length=20, default="user") # admin, farmer, user
    
    notifications = fields.ReverseRelation["Notification"]  # Defines a reverse relation to Notification model
    products = fields.ReverseRelation["Product"]   # Defines a reverse relation to Product model
    orders = fields.ReverseRelation["Order"]  # Defines a reverse relation to Order model
    formations = fields.ReverseRelation["Formation"]  # Defines a reverse relation to Formation model

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
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "orders"

class Post(Model):
    id = fields.IntField(pk=True)
    product = fields.ForeignKeyField("models.Product", related_name="posts")
    link = fields.CharField(max_length=255)
    description = fields.TextField()
    type = fields.CharField(max_length=50)  # "image" ou "video"
    likes_count = fields.IntField(default=0)
    date = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "posts"

class Notification(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    user = fields.ForeignKeyField("models.User", related_name="notifications")
    date = fields.DatetimeField(auto_now_add=True)
    read_at = fields.DatetimeField(null=True)

    class Meta:
        table = "notifications"

class TrainingMaterial(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100)
    video_url = fields.CharField(max_length=255)  # URL de la vidéo
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "training_materials"

class Like(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()  # ID de l'utilisateur
    material_id = fields.IntField()  # ID de l'élément
    is_liked = fields.BooleanField(default=False)  # État du like
