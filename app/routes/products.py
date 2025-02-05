# app/routers/products.py
from fastapi import APIRouter, Depends, HTTPException
from app.models import Product, Order
from app.schemas import ProductCreate, ProductResponse, OrderResponse
from app.auth import get_current_seller
from app.routes.notifications import send_email_notification  # Import de la fonction d'envoi d'email

router = APIRouter()

# Création d'un produit
@router.post("/products/", response_model=ProductResponse)
async def create_product(product: ProductCreate, current_user=Depends(get_current_seller)):
    new_product = await Product.create(seller=current_user, **product.dict())
    return new_product

# Suppression d'un produit
@router.delete("/products/{product_id}", dependencies=[Depends(get_current_seller)])
async def delete_product(product_id: int, current_user=Depends(get_current_seller)):
    product = await Product.filter(id=product_id, seller=current_user).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found or not owned by you")
    
    await product.delete()
    return {"msg": "Product deleted successfully"}

# Liste des produits d'un vendeur
@router.get("/products/", response_model=list[ProductResponse])
async def get_products(current_user=Depends(get_current_seller)):
    products = await Product.filter(seller=current_user).all()
    return products

# Obtenir un produit specifique
@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_products(product_id : int, current_user=Depends(get_current_seller)):
    product = await Product.filter(id=product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product

# Mise à jour d'un produit
@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product: ProductCreate, current_user=Depends(get_current_seller)):
    existing_product = await Product.filter(id=product_id, seller=current_user).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found or not owned by you")
    
    existing_product.price = product.price
    existing_product.stock = product.stock
    await existing_product.save()
    return existing_product
