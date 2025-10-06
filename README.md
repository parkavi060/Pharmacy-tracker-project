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

## 🗂 Database Structure

### Tables

1. **Product**
| Column      | Type      | Notes          |
|------------|-----------|----------------|
| product_id | String    | Primary Key 🏷️ |
| name       | String    | Required ✅    |
| description| String    | Optional 📝   |

2. **Location**
| Column       | Type      | Notes          |
|-------------|-----------|----------------|
| location_id | String    | Primary Key 🏬 |
| name        | String    | Required ✅    |
| address     | String    | Optional 📍   |

3. **ProductMovement**
| Column        | Type      | Notes                   |
|---------------|-----------|-------------------------|
| movement_id   | String    | Primary Key 🆔          |
| timestamp     | DateTime  | Defaults to now 🕒      |
| from_location | String    | Nullable, FK to Location 🏬 |
| to_location   | String    | Nullable, FK to Location 🏬 |
| product_id    | String    | FK to Product 🏷️       |
| qty           | Integer   | Required 🔢             |

---

## 🛠 Seed Data
The app automatically creates:
- 💊 **10 products** (Paracetamol, Amoxicillin, Cough Syrup, etc.)
- 🏬 **4 locations** (Main Warehouse, Front Store, Cold Storage, Online Dispatch Unit)
- 🔄 **20 product movements** (Inbound, transfer, outbound)

> Use `/reset-seed` route to reseed database (dev only).

---



