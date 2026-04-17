from flask import Flask, jsonify, request
from models import User, Base, Product, Sale, Payment
from sqlalchemy import create_engine
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
import psycopg2
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from mpesa import make_stk_push

load_dotenv()


app = Flask(__name__)
CORS(app, origins="http://localhost:5000")  # Enable CORS for all routes

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app = Flask(__name__)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# ✅ ADD THEM HERE
@jwt.unauthorized_loader
def unauthorized_callback(error):
    return jsonify({"error": "Missing token"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"error": "Invalid token"}), 422

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Token has expired"}), 401

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Token has been revoked"}), 401

@jwt.needs_fresh_token_loader
def needs_fresh_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Fresh token required"}), 401


app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("db_url")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("jwt_secret_key")

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
sessionLocal = sessionmaker(bind=engine)
# db_session = sessionLocal()

def get_db():
    return sessionLocal()

Base.metadata.create_all(engine)    

@app.route("/")
def home():
    return "Welcome to the Flask API!"

@app.route("/register", methods=["POST"])
def register():
    with get_db() as db:
        # if request.method != "POST":
        #     return jsonify({"error": "Method not allowed"}), 405
    
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        full_name = data.get("full_name")
        email = data.get("email")
        password = data.get("password")

        if not full_name or not email or not password:
            return jsonify({"error": "All fields are required"}), 400

        existing_user = db.query(User).filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "User already exists"}), 400
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')  

        try:
            new_user = User(full_name=full_name, email=email, password=hashed_password)
            db.add(new_user)
            db.commit()
            
            access_token = create_access_token(identity=email)
            
            if access_token:
                return jsonify({"message": "Registration Successful", "access_token": access_token}), 201
            else:
                return jsonify({"error": ""}), 500

        except Exception as e:
            db.rollback()
            return jsonify({"error": "Error occurred while registering user"}), 500

@app.route("/login", methods=["POST"])
def login():
        with get_db() as db:
            # Process login logic here
            data = request.get_json()

            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return jsonify({"error": "Email and password are required"}), 400
            
            user = db.query(User).filter_by(email=email).first()

            if user and bcrypt.check_password_hash(user.password, password):
                
                access_token = create_access_token(identity=user.email)

                return jsonify({"message": "Login Successful", "access_token": access_token}), 200

@app.route("/products", methods=["GET", "POST"])
@jwt_required()
def products():
    with get_db() as db:
        if request.method != "POST":
            return jsonify({"error": "Method not allowed"}), 405
        
        if request.method == "POST":
            data = request.get_json()

            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            product_name = data.get("product_name")
            price = data.get("price")

            if not price or not product_name:
                return jsonify({"error": "Product name and price are required"}), 400
            
            # ✅ Get logged-in user from JWT
            current_user_email = get_jwt_identity()
            user = db.query(User).filter_by(email=current_user_email).first()

            if not user:
                return jsonify({"error": "User not found"}), 404

            # ✅ Use authenticated user's ID
            new_product = Product(
                user_id=user.id,
                price=price,
                product_name=product_name
            )

            db.add(new_product)
            db.commit()
            db.refresh(new_product)

            return jsonify({"message": "Product created successfully"}), 201

        else:
            products = db.query(Product).all()

            products_list = [
                {
                    "id": product.id,
                    "user_id": product.user_id,
                    "product_name": product.product_name,
                    "price": product.price,
                    "created_at": product.created_at
                }
                for product in products
            ]

            return jsonify(products_list), 200
        
@app.route("/sales", methods=["GET", "POST"])
def sales():
    db = get_db()
    if request.method == "POST":
        # Process sales creation logic here
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        product_id = data.get("product_id")

        if not product_id:
            return jsonify({"error": "Product ID is required"}), 400

        existing_product = db.query(Product).filter_by(id=product_id).first()

        if not existing_product:
            return jsonify({"error": "Product not found"}), 404

        new_sale = Sale(product_id=product_id)
        try:
            db.add(new_sale)
            db.commit()
            db.refresh(new_sale)
            db.close()
        except Exception as e:
            db.rollback()
            return jsonify({"error": "Error occurred while creating sale"}), 500

        return jsonify({"message": "Sale created successfully"}), 201
    else:
            # Process sales retrieval logic here
            sales = db.query(Sale).all()

            sales_list = [
                {
                    "id": sale.id,
                    "product_id": sale.product_id,
                    "created_at": sale.created_at
                }
                for sale in sales
            ]
            return jsonify(sales_list), 200

@app.route('/stk-push', methods=['POST'])
def stk_push():
    data = request.get_json()
    
    stk_response = make_stk_push(data)
    
    #create a payment with id, sale_id, mrid, crid, created_at
    print(stk_response)
    return jsonify(stk_response)


@app.route('/stk-call-back', methods=['POST'])
def call_back():
    data = request.get_json()
    print("STK Callback Data:--------", data)
    
    #fetch the payment record using mrid and crid
    #update payment record with transaction code, status and trans_amount.
    return jsonify({"message": "Callback received"}), 200

#add a route for mpesa-payments its a get request it should fetch payments from payments table in db
#

if __name__ == "__main__":
    app.run()