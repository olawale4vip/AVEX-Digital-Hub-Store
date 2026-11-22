from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

PRODUCTS = [
    {"id": 1, "name": "Black Chunky Sneakers", "price": 20000, "category": "Sneakers", "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=900", "description": "Comfortable everyday sneakers with a bold look."},
    {"id": 2, "name": "White High-Top Sneakers", "price": 30000, "category": "Sneakers", "image": "https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?w=900", "description": "Clean high-top style for casual outfits."},
    {"id": 3, "name": "Black Platform Shoes", "price": 35000, "category": "Shoes", "image": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=900", "description": "A stylish platform design for a confident look."},
    {"id": 4, "name": "Navy Blue & White Sneakers", "price": 20000, "category": "Sneakers", "image": "https://images.unsplash.com/photo-1552346154-21d32810aba3?w=900", "description": "Sport-inspired comfort for everyday wear."},
]

def cart_items():
    cart = session.get("cart", {})
    items, total = [], 0
    for product in PRODUCTS:
        qty = int(cart.get(str(product["id"]), 0))
        if qty:
            subtotal = qty * product["price"]
            items.append({"product": product, "qty": qty, "subtotal": subtotal})
            total += subtotal
    return items, total

@app.route("/")
def home():
    q = request.args.get("q", "").strip().lower()
    products = [p for p in PRODUCTS if q in p["name"].lower() or q in p["category"].lower()] if q else PRODUCTS
    items, total = cart_items()
    return render_template("index.html", products=products, q=q, cart_count=sum(i["qty"] for i in items))

@app.post("/add/<int:product_id>")
def add_to_cart(product_id):
    if not any(p["id"] == product_id for p in PRODUCTS):
        flash("Product not found.")
        return redirect(url_for("home"))
    cart = session.get("cart", {})
    key = str(product_id)
    cart[key] = int(cart.get(key, 0)) + 1
    session["cart"] = cart
    flash("Added to your cart.")
    return redirect(request.referrer or url_for("home"))

@app.route("/cart")
def cart():
    items, total = cart_items()
    return render_template("cart.html", items=items, total=total)

@app.post("/update-cart")
def update_cart():
    cart = session.get("cart", {})
    for product in PRODUCTS:
        qty = request.form.get(str(product["id"]))
        if qty is not None:
            try:
                qty = max(0, min(99, int(qty)))
            except ValueError:
                qty = 0
            if qty:
                cart[str(product["id"])] = qty
            else:
                cart.pop(str(product["id"]), None)
    session["cart"] = cart
    return redirect(url_for("cart"))

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    items, total = cart_items()
    if not items:
        flash("Your cart is empty.")
        return redirect(url_for("home"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        if not name or not phone or not address:
            flash("Please complete all checkout fields.")
            return render_template("checkout.html", items=items, total=total)
        # Demo order capture. Connect a database and payment provider before production.
        order_ref = "AVX" + datetime.now().strftime("%y%m%d%H%M%S")
        session["cart"] = {}
        return render_template("success.html", name=name, order_ref=order_ref, total=total)
    return render_template("checkout.html", items=items, total=total)

if __name__ == "__main__":
    app.run(debug=True)
