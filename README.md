# 🚀 Flask App Deployment Guide (RDS + S3 Integration)
## 📌 Overview
**This guide helps you deploy a Flask-based application on AWS EC2 that:**
- Stores user details in RDS PostgreSQL
- Uploads profile images to S3
- Uses AWS Access Key & Secret Key
- Sends signup confirmation and signin success/failure as image response
# Deploying Application
## 📁 Project Structure
```
flask-user-app/
├── app.py
├── config.py
├── .env
├── requirements.txt
├── templates/
│   ├── signup.html
│   ├── signin.html
│   └── success.html
├── confirmation_images/
│   ├── success.jpg
│   └── failed.jpg
```
## 🔧 AWS Components Required
**AWS Resource	Purpose**
- EC2 (Ubuntu 22.04)	Host Flask app
- RDS PostgreSQL	Store user data
- S3 Bucket	Store profile images
-  AWS IAM user with access key & secret key

## 🛠️ Deployment Steps
### 1. ✅ Launch EC2 Instance
- OS: Ubuntu 22.04
- Security Group: Allow ports 22, 5000, and/or 80
- Use a public key for SSH access

### 2. ✅ SSH into EC2
```
ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>
```
### 3. ✅ Install Dependencies
```
sudo apt update
sudo apt install python3-pip python3-venv git -y
```
### 4. ✅ Upload or Clone the Project
Option A: Clone from GitHub
```
ls
git clone https://github.com/muralialakuntla3/ec2-s3-rds.git
ls
cd ec2-s3-rds
ls -a
```
### 5. ✅ Create and Activate Virtual Environment
```
python3 -m venv venv
source venv/bin/activate
```
### 6. ✅ Install Python Dependencies
```
pip install -r requirements.txt
```
### 7. ✅ Create .env File
```
vi .env
```
**Add the following and replace with your actual values:**
```
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_KEY=your_aws_secret_key
S3_BUCKET_NAME=flask-user-images
S3_REGION=us-east-1

DB_HOST=your-db-endpoint.rds.amazonaws.com
DB_NAME=userdb
DB_USER=postgres
DB_PASS=YourSecurePassword
```
### 8. ✅ Run Flask App (for Testing)
```
python3 app.py
```
**Visit in browser:**
- http://<EC2_PUBLIC_IP>:5000/
<img width="658" height="465" alt="image" src="https://github.com/user-attachments/assets/38dafea0-aff6-4b7d-84e9-7a1c01464872" />

## Test the Features
**Sign-Up:**
- Go to /signup
- Fill the form, upload an image
- Check:
  - Image stored in S3
  - Data stored in RDS

**Sign-In:**
- Go to /signin
- Provide same email and password
- Check:
  - Success or failure image is shown
 
<img width="668" height="348" alt="image" src="https://github.com/user-attachments/assets/aa37cb16-f14c-4089-84a8-0fe9989c4629" />


## Connecting to Database and Checking the information
### Install Postgres Database Client:
```
sudo apt install curl ca-certificates
sudo install -d /usr/share/postgresql-common/pgdg
sudo curl -o /usr/share/postgresql-common/pgdg/apt.postgresql.org.asc --fail https://www.postgresql.org/media/keys/ACCC4CF8.asc
. /etc/os-release
sudo sh -c "echo 'deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc] https://apt.postgresql.org/pub/repos/apt $VERSION_CODENAME-pgdg main' > /etc/apt/sources.list.d/pgdg.list"
sudo apt update
sudo apt -y install postgresql-16
```
### Connect to the Database
```
psql -h <db-host-address> -p 5432 --username postgre
# Enter The password
<img width="1174" height="303" alt="image" src="https://github.com/user-attachments/assets/fd1d30f7-960b-4dbc-ad6e-476ed2bff343" />

# displays the tables
\dt
<img width="449" height="199" alt="image" src="https://github.com/user-attachments/assets/ea824806-1b14-4734-abb4-1f1c522b4915" />

# view the table data
SELECT * FROM "users;"
<img width="1662" height="126" alt="image" src="https://github.com/user-attachments/assets/7b3e8c3a-a374-407e-ab9a-d070714fcdec" />
# exit the databse
exit;

```
----------------------------------------------------------------------------------- 

## Optional: Use Gunicorn for Production
**Install Gunicorn:**
```
pip install gunicorn
# Run Gunicorn:
gunicorn app:app --bind 0.0.0.0:5000

# Or on port 80:
sudo gunicorn app:app --bind 0.0.0.0:80
```

## ✅ Final Checks
- Sign up → stores user in RDS + image in S3
- Sign in → shows confirmation image (success/fail)
- App accessible at: http://<EC2_PUBLIC_IP>:5000/ (or port 80 if using Gunicorn with sudo)

# Delete AWS Resources via AWS Console
## 🔐 1. Sign in to AWS Console
- Visit: https://console.aws.amazon.com/
- Make sure you're in the correct region where your resources are deployed (e.g., us-west-1).

## 🗑️ 2. Delete S3 Bucket and Contents
- Go to S3 Console: https://s3.console.aws.amazon.com/s3/
- Click on the bucket name (e.g., flask-user-images)
- Select All objects → Click Actions > Delete → Confirm
- After the bucket is empty, return to the bucket list
- Select the bucket → Click Delete → Type the bucket name → Confirm deletion

## 🗑️ 3. Delete RDS PostgreSQL Database
- Go to RDS Console: https://console.aws.amazon.com/rds/
- In the left menu, click Databases
- Find your DB instance (e.g., flask-user-db)
- Click the checkbox next to it → Click Actions > Delete
- On the confirmation page:
  - Uncheck "Create final snapshot" if you don’t need a backup
  - Check the acknowledgment box
- Click Delete

## 🗑️ 4. Terminate EC2 Instance
- Go to EC2 Console: https://console.aws.amazon.com/ec2/
- In the left menu, click Instances
- Find your instance (e.g., with name FlaskAppVM)
- Select the instance → Click Instance State > Terminate instance
- Confirm termination

## 🛡️ 5. Delete Security Group (Optional)
- In EC2 Console, click Security Groups in the left menu
- Find the group associated with your RDS or EC2 instance (used in VPC)
- Ensure no instances or resources are attached
- Select the group → Click Actions > Delete security group

## 🔑 6. Delete EC2 Key Pair (Optional)
- Go to EC2 Console
- In the left menu, click Key Pairs
- Find your key (e.g., flask-key)
- Select it → Click Actions > Delete → Confirm

## 🔐 7. Delete IAM User and Access Keys (Optional)
- Go to IAM Console: https://console.aws.amazon.com/iam/
- In the left menu, click Users
- Click the user you created (e.g., flask-user)
- In Security Credentials, delete access keys if present
- Return to Users list → Select user → Click Delete user

## ✅ Verify All Are Deleted
- **S3**: No buckets left
- **RDS**: No DB instances
- **EC2**: No running instances or key pairs
- **IAM**: No leftover access users or keys
