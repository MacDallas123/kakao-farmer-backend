# app/routers/orders.py
from fastapi import APIRouter, Depends, HTTPException
from app.models import Product, Order
from app.schemas import OrderCreate, OrderResponse
from app.auth import get_current_user, get_current_seller
from app.routes.notifications import send_email_notification
from fpdf import FPDF  # Pour générer le PDF

router = APIRouter()

# Passer une commande
@router.post("/orders/", response_model=OrderResponse)
async def create_order(order: OrderCreate, current_user=Depends(get_current_user)):
    product = await Product.filter(id=order.product_id).prefetch_related("seller").first()
    # product = await Product.filter(id=order.product_id).first()
    
    if not product or product.stock < order.quantity:
        raise HTTPException(status_code=400, detail="Product not available or insufficient stock")

    total_price = product.price * order.quantity
    new_order = await Order.create(product=product, user=current_user, quantity=order.quantity, total_price=total_price)

    # Envoyer l'email au vendeur
    send_email_notification(product.seller.email, "New Order Received", "You have a new order.")

    # Envoyer un email de confirmation au client
    send_email_notification(current_user.email, "Order Confirmation", f"Your order has been placed. Order ID: {new_order.id}")

    return new_order


# Liste des commandes passées par un utilisateur
@router.get("/orders/", response_model=list[OrderResponse])
async def get_user_orders(current_user=Depends(get_current_user)):
    orders = await Order.filter(user=current_user).order_by("-id").all()
    print(orders)
    return orders

# Liste des commandes passées par un utilisateur
@router.get("/orders/all", response_model=list[OrderResponse])
async def get_user_orders(current_user=Depends(get_current_user)):
    orders = await Order.filter(product__seller=current_user).exclude(user=current_user).order_by("-id").all()
    print(orders)
    return orders

# Annuler une commande
@router.patch("/orders/{order_id}", dependencies=[Depends(get_current_user)])
async def cancel_order(order_id: int, current_user=Depends(get_current_user)):
    order = await Order.filter(id=order_id, user=current_user, status="pending").prefetch_related("product__seller").first()
    #order = await Order.filter(id=order_id, user=current_user, status="pending").prefetch_related("product").first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found or cannot be canceled")

    order.status = "canceled"
    await order.save()

    # Envoyer un email de notification au vendeur
    send_email_notification(order.product.seller.email, "Order Canceled", "An order has been canceled.")

    return {"msg": "Order canceled successfully"}

# Valid money transaction
@router.patch("/orders/{order_id}/pay", dependencies=[Depends(get_current_user)])
async def pay_order(order_id: int, current_user=Depends(get_current_user)):
    order = await Order.filter(id=order_id, user=current_user).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.payed = True
    await order.save()

    return {"msg": "Order payed successfully"}


# Liste des commandes en attente pour les produits d'un vendeur
@router.get("/orders/pending/", response_model=list[OrderResponse])
async def get_pending_orders(current_user=Depends(get_current_seller)):
    orders = await Order.filter(product__seller=current_user, status="pending").prefetch_related("product").all()
    return orders


# Refuser une commande (c'est le vendeur qui peut refuser)
@router.patch("/orders/{order_id}/reject", dependencies=[Depends(get_current_seller)])
async def reject_order(order_id: int, current_user=Depends(get_current_seller)):
    order = await Order.filter(id=order_id, product__seller=current_user).prefetch_related("product", "user").first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found or not owned by you")
    
    order.status = "rejected"
    await order.save()
    return {"msg": "Order rejected successfully"}



# Validation d'une commande
@router.patch("/orders/{order_id}/validate", dependencies=[Depends(get_current_seller)])
async def validate_order(order_id: int, current_user=Depends(get_current_seller)):
    order = await Order.filter(id=order_id, product__seller=current_user).prefetch_related("product", "user").first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found or not owned by you")
    
    # Décrémenter le stock du produit
    product = await Product.filter(id=order.product.id).first()
    product.stock -= order.quantity
    await product.save()

    order.status = "validated"
    await order.save()

    # Générer le PDF de la commande
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Buyer Name: {order.user.username}", ln=True)
    pdf.cell(200, 10, f"Product Name: {product.name}", ln=True)
    pdf.cell(200, 10, f"Quantity: {order.quantity}", ln=True)
    pdf.cell(200, 10, f"Total Price: {order.total_price}", ln=True)
    pdf.cell(200, 10, f"Seller Name: {product.seller.username}", ln=True)
    pdf.cell(200, 10, f"Seller Email: {product.seller.email}", ln=True)

    # Enregistrer le PDF
    pdf_file_path = f"orders/{order.id}_invoice.pdf"
    pdf.output(pdf_file_path)

    # Envoyer le PDF par email au client
    send_email_notification(order.user.email, "Order Confirmation", f"Your order has been validated. Invoice: {pdf_file_path}")

    return {"msg": "Order validated successfully"}