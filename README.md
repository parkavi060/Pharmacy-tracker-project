# 💊 Pharmacy Stock & Sales Tracker 🏥

A **Flask-based web app** to manage inventory, track product movements, and check balances across multiple warehouses. Perfect for pharmacies or small businesses! 🚀

---

## ✨ Features

### 1️⃣ Product Management
- ➕ Add, ✏️ Edit, 👁️ View products
- Each product has:
  - 🆔 Product ID
  - 🏷️ Name
  - 📝 Description

### 2️⃣ Location Management
- ➕ Add, ✏️ Edit, 👁️ View locations
- Each location has:
  - 🆔 Location ID
  - 🏬 Name
  - 📍 Address

### 3️⃣ Product Movements
- Record product movements:
  - 🔹 Inbound to a location
  - 🔹 Outbound from a location
  - 🔹 Transfers between locations
- Each movement includes:
  - 🆔 Movement ID
  - 🕒 Timestamp
  - 📦 Product
  - 🚚 From / To location
  - 🔢 Quantity

### 4️⃣ Reports 📊
- View **current balance of products per location** in a grid:
  - Product 🏷️
  - Location/Warehouse 🏬
  - Quantity 🔢

---


## 🛠 Seed Data
The app automatically creates:
- 💊 **10 products** (Paracetamol, Amoxicillin, Cough Syrup, etc.)
- 🏬 **4 locations** (Main Warehouse, Front Store, Cold Storage, Online Dispatch Unit)
- 🔄 **20 product movements** (Inbound, transfer, outbound)

> Use `/reset-seed` route to reseed database (dev only).

---



