# project-management-application-djnago

# **Project Management API** 🛠️🚀

## **Overview**

This is a **Django REST Framework (DRF)**-based API for managing **projects, users, project members, and comments**. It supports:

✔ **User Registration & Authentication** (Token-Based)
✔ **Project Creation & Management**
✔ **Role-Based Access Control (Owner, Editor, Reader)**
✔ **Commenting on Projects**
✔ **Admin Panel for Management**

---

## **📌 Tech Stack**

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL (or SQLite for local development)
- **Authentication**: Django Authentication
- **Admin Panel**: Django Admin
- **Testing**: Pytest, Django TestCase
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


### **3️⃣ Activate the Virtual Environment**

```pipenv shell```


### **4️⃣ Set Up the Database**

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

Logs are stored in **logs/app.log** and include:
✅ API requests
✅ Authentication logs
✅ Errors and warnings

## **📌 License**

This project is  **MIT Licensed** .
