# AVEX Digital Hub — Python E-commerce Starter

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment (recommended):
   - Windows: `py -m venv .venv` then `.venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
4. Install Flask: `pip install -r requirements.txt`
5. Start the website: `python app.py`
6. Open `http://127.0.0.1:5000` in your browser.

## Included
- Product catalogue and search
- Session-based shopping cart
- Quantity updates
- Customer checkout form and demo order confirmation
- Responsive layout for phones and computers

## Important before real customers use it
This is a starter/demo. Checkout does not collect payment and orders are not stored permanently. Before launch, add a database (e.g. SQLite/PostgreSQL), admin authentication, product management, secure production secret key, HTTPS, input validation, order notifications, delivery settings, and a payment provider such as Paystack or Flutterwave. Do not use Flask's development server for public production hosting.
