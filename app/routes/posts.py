# app/routers/posts.py
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from app.models import Post as PostModel, Product
from app.schemas import PostCreate, PostResponse
from app.auth import get_current_seller

router = APIRouter()

#Creer un post
@router.post("/posts/", response_model=PostResponse)
async def create_post(post: PostCreate, current_user=Depends(get_current_seller)):
    product = await Product.filter(id=post.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    new_post = await PostModel.create(**post.dict())
    return new_post

#supprimer un post 
@router.delete("/posts/{post_id}", dependencies=[Depends(get_current_seller)])
async def delete_post(post_id: int, current_user=Depends(get_current_seller)):
    post = await PostModel.filter(id=post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    await post.delete()
    return {"msg": "Post deleted successfully"}

#lister les posts d'un vendeurs precis 
@router.get("/user-posts/", response_model=list[PostResponse])
async def get_posts(current_user=Depends(get_current_seller)):
    posts = await PostModel.filter(product__seller=current_user).prefetch_related("product")
    return posts


# lister tous les postes
@router.get("/posts/", response_model=list[PostResponse])
async def get_posts(current_user=Depends(get_current_seller)):
    posts = await PostModel.all()
    return posts

#lister les posts avec pagination

"""@router.get("/posts/paginated/?skip={skip}&limit={limit}", response_model=list[PostResponse])
async def get_paginated_posts(skip: int = 0, limit: int = 1, current_user=Depends(get_current_seller)):
    posts = await PostModel.all().offset(skip).limit(limit).prefetch_related("product")
    return posts"""

#rechercher un post (videos images) en entrant le nom(cacao ou semence) ou le type (type de cacao ou type de semence )
@router.get("/posts/search/", response_model=list[PostResponse])
async def search_posts(product_name: Optional[str] = None, post_type: Optional[str] = None):
    query = PostModel.all().prefetch_related("product")

    if product_name:
        query = query.filter(product__name__icontains=product_name)
    if post_type:
        query = query.filter(type=post_type)

    posts = await query
    return posts