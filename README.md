📋 Project Description
LIB POS App is a lightweight, user-friendly Point of Sale (POS) system designed to
streamline the process of managing sales, 
inventory, and customer records in retail or small business environments. 
It features a secure admin dashboard where users can:

Manage product listings

Process and track customer orders

Automatically calculate taxes and total amounts

Email professional receipts to customers

Monitor low stock and view sales history

Allow superusers to manage other admin accounts

The system supports role-based access where Super Admins have 
full control over the app (including user management), while Regular Admins focus
on product and sales operations.

💻 Technologies Used
Category	Technology Used
Backend	Python 3, Django Framework
Frontend	HTML5, CSS3, Bootstrap 5, Tailwind CSS (optional)
Database	SQLite3 (default), Django ORM
Email Service	Gmail SMTP with Google App Password
PDF-like Receipts	HTML template styled to resemble a printed receipt
Authentication	Django's built-in auth system
Hosting (Local)	Python server via manage.py runserver
Optional Timezone	Africa/Kigali (TIME_ZONE = 'Africa/Kigali')

🛠️ Setup Guide
Follow these steps to get the system up and running locally on your machine:

1. 📁 Clone or Download the Project
bash
Copy
Edit
git clone https://github.com/your-username/lib-pos-app.git
cd lib-pos-app
2. 🐍 Create and Activate Virtual Environment (Optional but Recommended)
bash
Copy
Edit
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
3. 📦 Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
Make sure your requirements.txt includes:

txt
Copy
Edit
Django>=3.2
4. ⚙️ Configure Your Settings
Open settings.py

Set your email configuration to use Google App Password:

python
Copy
Edit
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'hyallison5050@gmail.com'
EMAIL_HOST_PASSWORD = 'xhgm lhbq colk gyds'  # Use your Google App password
Optional: Set your timezone

python
Copy
Edit
TIME_ZONE = 'Africa/Kigali'
USE_TZ = True
5. 🔧 Migrate Database
bash
Copy
Edit
python manage.py makemigrations
python manage.py migrate
6. 👤 Create Superuser
bash
Copy
Edit
python manage.py createsuperuser
Follow the prompts to create a login account.

7. 🚀 Run the Server
bash
Copy
Edit
python manage.py runserver
Visit http://127.0.0.1:8000 to access the application.

8. 📨 Test Email Receipt Feature
Add a customer with a valid email.

Process a sale.

Use the "Send Receipt" button to test email delivery.

✅ If configured correctly, the customer will receive a beautifully formatted receipt via email!

