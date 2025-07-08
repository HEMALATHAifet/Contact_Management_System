# 📇 Contact Manager - Gradio App

A simple **Contact Management System** built with **Python** and **Gradio**, running fully in **Google Colab** or any Python environment. It allows users to **Create**, **Read**, **Update**, and **Delete (CRUD)** contact details with real-time input validation and a clean user interface.

---

## 🚀 Features

- ✅ Add new contacts with validation
- ✏️ Update specific fields of an existing contact using Contact ID
- 🗑️ Delete contacts by ID
- 📄 Display all saved contacts
- 💾 Stores data locally in a `contacts.json` file
- 🔒 Duplicate email and phone number check
- 🧠 Smart validations for name, email, phone, and address fields

---

## 🛠️ Tech Stack

- **Python 3**
- **Gradio** (for frontend UI)
- **JSON** (for local data storage)
- **Regular Expressions** (for input validation)

---

## 📦 Installation

To run this project, install the following Python package:

```bash
pip install gradio
```
---
## ✅ In Google Colab
-Open Google Colab

- Upload your .py or .ipynb file.

- Install Gradio (if not already installed):
```
!pip install gradio
```
- Run the script with:
```
demo.launch(share=True)
```
A public URL will appear to interact with the app.

---
## 🔐 Validations

Each field in the form is validated using specific rules to ensure clean and reliable data.

| Field        | Validation Rule                                  |
|--------------|--------------------------------------------------|
| First Name   | Required, Minimum 3 alphabets                    |
| Middle Name  | Optional                                         |
| Last Name    | Required, Alphabets only                         |
| Email        | Required, Valid email format                     |
| Phone        | Required, Exactly 10 digits, not all same digits |
| Address      | Required                                         |

> 🛑 **Email and phone number must be unique.**

---
## 🧭 Interface Overview
The app contains 4 main tabs, each for a CRUD operation:

## 🟩 Create
- Add a new contact.

- Required fields: First Name, Last Name, Email, Phone, and Address.

- Middle Name is optional.

- Real-time validation for all fields.

- Checks for duplicate email or phone number.

## 🟦 Update
- Modify an existing contact using the Contact ID.

- You can update only selected fields (partial updates allowed).

- Validates updated fields only.

- Prevents email or phone duplication.

## 🟨 Read
- Displays all saved contacts.

- Each entry includes ID, full name, email, phone, and address.

## 🟥 Delete
- Remove a contact using their ID.

- Confirmation message after successful deletion.

- Shows error if ID is not found.

---
## 🧪 Sample Output
Here’s what the "Read" tab output may look like:

1. Hemalatha A R | hemi@gmail.com | 9876543210 | Chennai
2. John   D      | john@example.com | 9123456780 | Bangalore
3. Priya   M     | priya@gmail.com | 9988776655 | Hyderabad
---
Each entry displays:
- Unique ID
- Full name (first, middle, last)
- Email
- Phone number
- Address

---
