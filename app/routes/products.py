# app/routers/products.py
from fastapi import APIRouter, Depends, HTTPException
from app.models import Product, Order
from app.schemas import ProductCreate, ProductResponse, OrderResponse
from app.auth import get_current_seller, get_current_user

router = APIRouter()

# Création d'un produit
@router.post("/products/", response_model=ProductResponse)
async def create_product(product: ProductCreate, current_user=Depends(get_current_user)):
    new_product = await Product.create(seller=current_user, **product.dict())
    return new_product

# Suppression d'un produit
@router.delete("/products/{product_id}", dependencies=[Depends(get_current_user)])
async def delete_product(product_id: int, current_user=Depends(get_current_user)):
    product = await Product.filter(id=product_id, seller=current_user).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found or not owned by you")
    
    await product.delete()
    return {"msg": "Product deleted successfully"}

# Liste des produits d'un vendeur
@router.get("/products/", response_model=list[ProductResponse])
async def get_products(current_user=Depends(get_current_user)):
    products = await Product.filter(seller=current_user).all()
    return products

# Obtenir un produit specifique
@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_products(product_id : int, current_user=Depends(get_current_user)):
    product = await Product.filter(id=product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product

# Mise à jour d'un produit
@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product: ProductCreate, current_user=Depends(get_current_user)):
    existing_product = await Product.filter(id=product_id, seller=current_user).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found or not owned by you")
    
    existing_product.price = product.price
    existing_product.stock = product.stock
    await existing_product.save()
    return existing_product
