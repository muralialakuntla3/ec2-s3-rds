import boto3
import psycopg2
from flask import Flask, request, render_template, redirect, send_file
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from config import *

app = Flask(__name__)

# PostgreSQL Connection
conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
cursor = conn.cursor()

# Create users table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT,
    image_filename TEXT
)
""")
conn.commit()

# S3 Client
s3 = boto3.client('s3',
                  aws_access_key_id=AWS_ACCESS_KEY,
                  aws_secret_access_key=AWS_SECRET_KEY,
                  region_name=S3_REGION)

@app.route("/")
def home():
    return redirect("/signup")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    image = request.files["profile"]

    filename = secure_filename(image.filename)

    try:
        s3.upload_fileobj(image, S3_BUCKET, filename)
        hashed_pw = generate_password_hash(password)
        cursor.execute("INSERT INTO users (name, email, password, image_filename) VALUES (%s, %s, %s, %s)",
                       (name, email, hashed_pw, filename))
        conn.commit()
        return render_template("success.html")
    except Exception as e:
        conn.rollback()
        return f"Signup error: {str(e)}"

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")

    email = request.form["email"]
    password = request.form["password"]
    cursor.execute("SELECT password FROM users WHERE email=%s", (email,))
    result = cursor.fetchone()

    if result and check_password_hash(result[0], password):
        return send_file("confirmation_images/success.jpg", mimetype='image/jpeg')
    else:
        return send_file("confirmation_images/failed.jpg", mimetype='image/jpeg')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
