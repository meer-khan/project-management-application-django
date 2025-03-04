# **Project Management API** 🛠️🚀

## **Overview**

This is a **Django REST Framework (DRF)**-based API for managing **projects, users, project members, and comments**. It supports:

✔ **User Registration & Authentication**  
✔ **Project Creation & Management**  
✔ **Role-Based Access Control (Owner, Editor, Reader)**  
✔ **Commenting on Projects**  
✔ **Admin Panel for Management**  
✔ **SMTPLib For email verification**    




---

## Note and Assumptions: 
- Used **pipenv** as packagemanager.
- Used SQLite as a  database (As it comes with Django by default).
- Added Email verification system by using Python's default SMTPLib.
- **.env.dist** has all the variables/secrets required to run the application.
- **python-version** file has Python version which is 3.11
- **IMPORTANT:** Attached the Postman collection *[visual-abstract-project-management.postman_collection.json](https://github.com/meer-khan/project-management-application-django/blob/main/visual-abstract-project-management.postman_collection.json)* in root directory. Just import this collection in Postman and use all the routes. 

---

## **📌 Tech Stack**

- **Backend**: Django, Django REST Framework
- **Database**: SQLite
- **Authentication**: Django Authentication
- **Email verification**: SMTPLib
- **Admin Panel**: Django Admin
- **Testing**: Django TestCase
- **Logging**: Python `logging` module

---

## **📌 Setup Instructions**

### **1️⃣ Clone the Repository**

```sh
git clone https://github.com/your-username/project-management-api.git
cd project-management-api
```

### **2️⃣ Install Pipenv and Dependencies**

Ensure **Pipenv** is installed. If not, install it first:

```
pip install pipenv
```


Then, install dependencies using Pipenv:

```pipenv install```


### **3️⃣ Activate the Virtual Environment** - Activate the environment after writing .env

```pipenv shell```


### **4️⃣ Set Up the Database** - Activate the environment after writing .env

Modify **`.env` file** (check .env.dist) to configure your env:


Then, run migrations:

```python manage.py migrate```


### **5️⃣ Create a Superuser for Admin Panel**

```python manage.py createsuperuser```

Follow the prompts to enter  **username, email, and password** .

### **6️⃣ Run the Development Server**

```python manage.py runserver```


Access the API at: **`http://127.0.0.1:8000/api/`**
Access the Django Admin at: **`http://127.0.0.1:8000/admin/`**

---

## **📌 API Endpoints**

### **🔹 Authentication**

| Method   | Endpoint                 | Description                     |
| -------- | ------------------------ | ------------------------------- |
| `POST` | `/api/users/register/` | Register a new user             |
| `POST` | `/api/users/login/`    | Log in a user                   |
| `POST` | `/api/users/logout/`   | Log out a user                  |
| `POST` | `/api/users/verify/`   | Verify email after registration |

---

### **🔹 Projects**

| Method     | Endpoint                | Description                                  |
| ---------- | ----------------------- | -------------------------------------------- |
| `GET`    | `/api/projects/`      | List all projects for the authenticated user |
| `POST`   | `/api/projects/`      | Create a new project                         |
| `GET`    | `/api/projects/{id}/` | Retrieve a project                           |
| `PUT`    | `/api/projects/{id}/` | Update a project (Owner, Editor)             |
| `DELETE` | `/api/projects/{id}/` | Delete a project (Owner only)                |

---

### **🔹 Project Members**

| Method   | Endpoint                        | Description                            |
| -------- | ------------------------------- | -------------------------------------- |
| `POST` | `/api/projects/{id}/members/` | Add a member to a project (Owner only) |

---

### **🔹 Comments**

| Method   | Endpoint                         | Description                                |
| -------- | -------------------------------- | ------------------------------------------ |
| `POST` | `/api/projects/{id}/comments/` | Add a comment to a project (Owner, Editor) |
| `GET`  | `/api/projects/{id}/comments/` | List all comments for a project            |


### **🔹 csrf token**

| Method   | Endpoint                         | Description                                |
| -------- | -------------------------------- | ------------------------------------------ |
| `POST` | `/api/csrf/`                   |To generate the CSRF token for request where CSRF Token error arises |


## **📌 Running Tests** 🧪


or

```python manage.py test```


---

## **📌 Admin Panel**

Access Django Admin at **[http://127.0.0.1:8000/admin/]()** using the superuser credentials.

---

## **📌 Logging**

✅ API requests  
✅ Authentication logs  
✅ Errors and warnings  

## **📌 License**

This project is  **MIT Licensed** .
