# Tasky API
> is a robust and flexible interface designed to interact seamlessly with the Tasky App. It provides a set of endpoints that allow you to manage tasks, users, and account settings programmatically, making it perfect for integrating Tasky’s task management functionality into your own applications or workflows.

## Key Features:
> Task Management: Create, read, update, and delete tasks with ease through a set of simple API calls.
QR Code Integration: Generate and scan QR codes to quickly access specific tasks within your system.
User Authentication & Management: Secure user login, profile updates, password resets, and more.
Account Management: Update personal data, manage account settings, and securely handle user information.
Flexible Data Handling: Return and manipulate task data in various formats for easy integration into your apps.
The Tasky API is built to be reliable, scalable, and easy to use, enabling developers to add powerful task management features to their own applications quickly and efficiently. Start integrating Tasky API into your project today and experience seamless task management!

## How to use the API
```
git clone https://github.com/Amr20533/TASK-API.git
```
```
git pull origin main
```
### To create a virtual environment (venv) in Python, follow these steps:
1. Navigate to your project folder (where you want to create the virtual environment):
```
cd /path/to/your/project
```
2. Create a virtual environment:
```
python -m venv venv
```
3. Activate the virtual environment:
* On Windows:
```
.\venv\Scripts\activate
```
* On macOS/Linux:
```
source venv/bin/activate
```
4. Deactivate the virtual environment (when you're done):
```
deactivate
```
### To migrate your database and run the server, follow these steps:

1. Make Migrations
 At first need to create migrations for your models.
```
python manage.py makemigrations
```
2. Apply Migrations
  After making migrations, you need to apply them to your database:
```
python manage.py migrate
```
3. Run the Development Server
  To start your development server:
```
python manage.py runserver
```


