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

class Notification(Model):
    id = fields.IntField(pk=True)
    titre = fields.CharField(max_length=255)
    contenu = fields.TextField()
    user = fields.ForeignKeyField("models.User", related_name="notifications")

    class Meta:
        table = "notifications"

class Transaction(Model):
    id = fields.IntField(pk=True)
    montant = fields.FloatField()
    motif = fields.CharField(max_length=255)
    date = fields.CharField(max_length=255)
    quantite = fields.CharField(max_length=255)
    user = fields.ForeignKeyField("models.User", related_name="transactions")
    produit = fields.ForeignKeyField("models.Produit", related_name="transactions")

    class Meta:
        table = "transactions"

class Produit(Model):
    id = fields.IntField(pk=True)
    nom = fields.CharField(max_length=255)
    pix = fields.CharField(max_length=255)
    description = fields.TextField()
    quantite = fields.CharField(max_length=255)
    user = fields.ForeignKeyField("models.User", related_name="produits")
    transactions = fields.ReverseRelation["Transaction"]  # Defines a reverse relation to Transaction model

    class Meta:
        table = "produit"

class Poste(Model):
    id = fields.IntField(pk=True)
    type = fields.CharField(max_length=50, null=True)  # 'video' ou 'texte'
    likes = fields.ManyToManyField("models.User", related_name="liked_posts", through="like")
    video = fields.ReverseRelation["Video"]
    texte = fields.ReverseRelation["Texte"]

    class Meta:
        table = "poste"

class Video(Model):
    id = fields.IntField(pk=True)
    idVideo = fields.CharField(max_length=255)
    poste = fields.OneToOneField("models.Poste", related_name="video")

    class Meta:
        table = "video"

class Texte(Model):
    id = fields.IntField(pk=True)
    contenu = fields.TextField()
    poste = fields.OneToOneField("models.Poste", related_name="texte")

    class Meta:
        table = "texte"

class Formation(Model):
    id = fields.IntField(pk=True)
    videos = fields.ManyToManyRelation["Video"]
    textes = fields.ManyToManyRelation["Texte"]

    class Meta:
        table = "formation"