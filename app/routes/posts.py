# app/routers/posts.py
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from app.models import Like, Post as PostModel, Product
from app.schemas import PostCreate, PostResponse
from app.auth import get_current_seller, get_current_user

router = APIRouter()

#Creer un post
@router.post("/posts/", response_model=PostResponse)
async def create_post(post: PostCreate, current_user=Depends(get_current_user)):
    product = await Product.filter(id=post.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    new_post = await PostModel.create(**post.dict())
    return new_post

#supprimer un post 
@router.delete("/posts/{post_id}", dependencies=[Depends(get_current_user)])
async def delete_post(post_id: int, current_user=Depends(get_current_user)):
    post = await PostModel.filter(id=post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    await post.delete()
    return {"msg": "Post deleted successfully"}

#lister les posts d'un vendeurs precis 
@router.get("/user-posts/", response_model=list[PostResponse])
async def get_posts(current_user=Depends(get_current_user)):
    posts = await PostModel.filter(product__seller=current_user).order_by('-date').prefetch_related("product")
    return posts


# lister tous les postes
@router.get("/posts/", response_model=list[PostResponse])
async def get_posts(current_user=Depends(get_current_user)):
    posts = await PostModel.all().order_by('-date')
    return posts

#lister les posts avec pagination

"""@router.get("/posts/paginated/?skip={skip}&limit={limit}", response_model=list[PostResponse])
async def get_paginated_posts(skip: int = 0, limit: int = 1, current_user=Depends(get_current_user)):
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


#Methode qui gere le like et le delike pour un post précis
@router.post("/likes/{post_id}/")
async def toggle_like(post_id: int, current_user=Depends(get_current_user)):
    # Vérifiez si l'utilisateur a déjà liké ce post
    existing_like = await Like.filter(user_id=current_user.id, material_id=post_id).first()
    post = await PostModel.filter(id=post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if existing_like:
        # Inverser l'état du like
        existing_like.is_liked = not existing_like.is_liked
        await existing_like.save()
        
        # Mettre à jour le compteur de likes
        if existing_like.is_liked:
            post.likes_count += 1
        else:
            post.likes_count -= 1
    else:
        # Créer un nouveau like
        new_like = await Like.create(user_id=current_user.id, material_id=post_id, is_liked=True)
        post.likes_count += 1

    await post.save()
    
    return {
        "post_id": post_id,
        "is_liked": existing_like.is_liked if existing_like else True,
        "likes_count": post.likes_count
    }


#methode qui retourne la liste des personnes ayant liké un post précis
@router.get("/likes/{post_id}/users/")
async def get_likers(post_id: int):
    # Récupérer tous les likes pour le post donné
    likes = await Like.filter(post_id=post_id, is_liked=True).prefetch_related("user_id").all()

    if not likes:
        return {"post_id": post_id, "likers": []}

    # Récupérer les utilisateurs qui ont liké
    likers = [like.user_id for like in likes]

    return {"post_id": post_id, "likers": likers}

#methode qui indique si l'utilisateur actuel a deja like un post
@router.get("/likes/{post_id}/user/liked")
async def get_liker(post_id: int, current_user=Depends(get_current_user)):
    # Vérifiez si l'utilisateur a déjà liké ce post
    existing_like = await Like.filter(user_id=current_user.id, material_id=post_id).first()
    post = await PostModel.filter(id=post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return {
        "post_id": post_id,
        "is_liked": existing_like.is_liked if existing_like else True
    }