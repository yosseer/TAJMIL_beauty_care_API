# TAJMIL Tunisia – Beauty Care RESTful API

A culturally inspired beauty care API built with **Flask**, integrating modern technology with Tunisian beauty traditions.

---

## 📌 Overview

**TAJMIL Tunisia** is a RESTful API designed to modernize how Tunisian users access beauty services and products.  
It blends technological innovation with Tunisia’s cultural heritage by offering features such as:

- Beauty service booking  
- Local product discovery  
- Personalized recommendations  
- Multilingual support (Arabic, English, French)  

The system aims to empower both users and beauty service providers by offering an accessible, scalable, and culturally relevant platform.

---

## ✨ Key Features

### 👤 User Management
- Register, authenticate, and manage user profiles  
- View and update account information  
- Track booking history  

### 🛍️ Product Management
- Explore beauty products available in Tunisia  
- Add, update, delete, and view product details  
- Integration of cultural beauty ingredients and remedies  

### 💇 Service Management
- Browse beauty services offered by salons  
- Manage service details  
- Link products to specific services  

### 📅 Booking Management
- Book beauty services with preferred providers  
- Edit or cancel bookings  
- Track appointment status  

### 🌍 Multilingual Support
Implemented using **Flask-Babel**, supporting:  
- 🇹🇳 Arabic  
- 🇬🇧 English  
- 🇫🇷 French  

---

## 🏛️ Architecture & Technologies

### 🧱 Tech Stack
- **Flask** – Core microframework  
- **Flask-Smorest** – RESTful blueprint structure + OpenAPI support  
- **Flask SQLAlchemy** – ORM for database handling  
- **Marshmallow** – Validation and serialization  
- **Flask-Babel** – Internationalization & localization  
- **dotenv** – Environment variable management  

---

## ✔️ Database Models

- **UserModel** – User credentials, profiles, and booking history  
- **ProductModel** – Beauty products (local + modern)  
- **ServiceModel** – Services offered by salons  
- **BookingModel** – User bookings linked to services and users  

Models use SQLAlchemy relationships to maintain data integrity.


