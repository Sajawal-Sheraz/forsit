# 🛒 E-commerce Admin API

A **FastAPI-powered backend API** designed to support an admin dashboard for e-commerce managers. It provides endpoints for managing products, inventory, and sales data, along with support for detailed analytics and insights.

---

## ✅ Prerequisites

Make sure the following tools are installed on your system before proceeding:

- **Python 3.8+**
- **MySQL Server**
- **pip** (Python package installer)
- **Git**
- _(Recommended)_ Python virtual environment tool: `venv`

---

## 🗃️ Step 1: MySQL Setup

This project leverages **MySQL** as the primary relational database for managing products, inventory, and sales data.

### 🔧 Installation

To install MySQL on your system, follow the official documentation:

- [MySQL Installation Guide](https://dev.mysql.com/doc/refman/8.0/en/installing.html)

> ✅ Ensure that the MySQL Server is running locally and accessible before proceeding.

---

### ⚙️ Database Configuration

Before running the project, you need to configure the **database connection string** in the `database.py` file.

The format of the connection string (SQLAlchemy compatible) is:

```bash
mysql+pymysql://<username>:<password>@<host>/<database_name>
```

For example, if you're using default local settings:

```bash
mysql+pymysql://root:admin@localhost/ecommerce
```

Update the credentials based on your local setup.

---

## 🚀 Step 2: Project Setup

Follow the instructions below to clone and set up the project in your development environment.

### 🔁 1. Clone the Repository

Use Git to clone the repository and change into the project directory:

```bash
git clone https://github.com/Sajawal-Sheraz/forsit.git
cd forsit
```

---

### 🧪 2. Create & Activate a Virtual Environment

We recommend using a virtual environment to isolate project dependencies.

##### On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

##### 📦 3. Install Dependencies

Install the required Python packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

##### 📦 4. Populate Dummy Data

To populate the database with initial/demo data, run the following script:

```bash
python insert_data.py
```

---

## Guide for APIs

### 📦 Inventory

These endpoints allow you to **monitor and manage inventory levels** for all products in the system.

---

#### 1️⃣ Get Inventory Status

**Endpoint:**  
`GET /inventory/`

**Description:**  
Retrieves the current inventory status for all products. Optionally, you can filter to show only products with a quantity below a specified threshold.

**Query Parameters:**

| Parameter   | Type    | Required | Description                                        |
| ----------- | ------- | -------- | -------------------------------------------------- |
| `threshold` | integer | Optional | Filters to products with quantity below this value |

**Sample Request:**

```http
GET http://localhost:8000/inventory/?threshold=20
```

**Sample Response:**

```json
{
  "status": "success",
  "message": "Inventory Retrieved",
  "result": [
    {
      "product_id": 8,
      "quantity": 19,
      "updated_at": "2025-05-18T17:48:23"
    }
  ]
}
```

---

#### 2️⃣ Update Inventory

**Endpoint:**  
`POST /inventory/update`

**Description:**  
Updates the inventory quantity for a specific product. The product must already exist in the database.

**Sample Request Body:**

````json
{
  "product_id": 1,
  "quantity": 25
}```


**Sample Response:**

```json
{
    "status": "success",
    "message": "Inventory updated",
    "result": {
        "product_id": 1,
        "quantity": 25,
        "updated_at": "2025-05-18T17:54:07"
    }
}
````

---

### 🛒 Products APIs

These endpoints allow you to **retrieve** and **register new products** in the system.

---

#### 1️⃣ Retrieve Products (Paginated)

**Endpoint:**  
`GET /products/`

**Description:**  
Retrieves a paginated list of products. Use query parameters to control pagination behavior.

**Query Parameters:**

| Parameter | Type    | Required | Default | Description                 |
| --------- | ------- | -------- | ------- | --------------------------- |
| `page`    | integer | Optional | 1       | Page number to fetch        |
| `size`    | integer | Optional | 10      | Number of products per page |

**Sample Request:**

```http
GET http://localhost:8000/products/?page=1&size=5
```

**Sample Response:**

```json
{
  "status": "success",
  "message": "Products retrieved successfully",
  "result": {
    "products": [
      {
        "id": 1,
        "name": "Wireless Mouse",
        "category": "Electronics",
        "price": 29.99,
        "created_at": "2025-05-18T16:00:47"
      },
      {
        "id": 2,
        "name": "Bluetooth Keyboard",
        "category": "Electronics",
        "price": 49.99,
        "created_at": "2025-05-18T16:00:47"
      }
      ........
    ],
    "total": 12,
    "page": 1,
    "size": 10
  }
}
```

---

#### 2️⃣ Create New Product

**Endpoint:**  
`POST /products/create`

**Description:**  
Registers a new product in the system. You must include `name`, `category`, and `price` in the request body.

**Request Body (JSON):**

```json
{
  "name": "Ergonomic Chair",
  "category": "Furniture",
  "price": 199.99
}
```

**Sample Request:**

```http
POST http://localhost:8000/products/create
```

**Sample Response:**

```json
{
  "id": 13,
  "name": "Ergonomic Chair",
  "category": "Furniture",
  "price": 199.99,
  "created_at": "2025-05-18T18:54:01"
}
```

> 📝 The created product is returned immediately, including its auto-generated ID and creation timestamp.

---

## 📊 Sales APIs

These endpoints offer comprehensive insights into revenue and sales data, with support for filtering, comparison, and trend analysis.

---

#### 1️⃣ Sales Summary

**Endpoint:**  
`GET /sales/summary`

**Description:**  
Returns summarized revenue data grouped by a specific time interval.

**Query Parameters:**

| Parameter | Type   | Required | Default | Description                                           |
| --------- | ------ | -------- | ------- | ----------------------------------------------------- |
| interval  | string | Optional | daily   | Time grouping: `daily`, `weekly`, `monthly`, `yearly` |

**Sample Request:**

```http
GET http://localhost:8000/sales/summary?interval=monthly
```

**Sample Response:**

```json
{
  "status": "success",
  "message": "Sales summary",
  "result": [
    { "period": "2025-03", "revenue": 15000.0 },
    { "period": "2025-04", "revenue": 21800.5 }
  ]
}
```

---

#### 2️⃣ Compare Revenue Between Two Date Ranges

**Endpoint:**  
`GET /sales/compare`

**Description:**  
Compares total revenue between two date ranges, with optional filtering by product category.

**Query Parameters:**

| Parameter | Type | Required | Description                                |
| --------- | ---- | -------- | ------------------------------------------ |
| start1    | date | ✅       | Start date for first period (`YYYY-MM-DD`) |
| end1      | date | ✅       | End date for first period                  |
| start2    | date | ✅       | Start date for second period               |
| end2      | date | ✅       | End date for second period                 |

**Sample Request:**

```http
GET http://localhost:8000/sales/compare?start1=2025-03-01&end1=2025-03-31&start2=2025-04-01&end2=2025-04-30
```

**Sample Response:**

```json
{
  "status": "success",
  "message": "Revenue comparison",
  "result": {
    "period_1": 15200.0,
    "period_2": 18900.0,
    "difference": 3700.0
  }
}
```

---

#### 3️⃣ Compare Revenue Between Two Categories

**Endpoint:**  
`GET /sales/compare-category`

**Description:**  
Compares revenue generated between two product categories.

**Query Parameters:**

| Parameter | Type   | Required | Description                        |
| --------- | ------ | -------- | ---------------------------------- |
| category1 | string | ✅       | First product category to compare  |
| category2 | string | ✅       | Second product category to compare |

**Sample Request:**

```http
GET http://localhost:8000/sales/compare-category?category1=Electronics&category2=Furniture
```

**Sample Response:**

```json
{
  "status": "success",
  "message": "Revenue comparison between Electronics and Furniture",
  "result": {
    "category1": {
      "name": "Electronics",
      "revenue": 24500.0
    },
    "category2": {
      "name": "Furniture",
      "revenue": 18200.0
    },
    "difference": -6300.0
  }
}
```

---

#### 4️⃣ Filter Sales by Date, Product, or Category

**Endpoint:**  
`GET /sales/filter`

**Description:**  
Filters sales records based on optional parameters such as date range, product ID, or category.

**Query Parameters:**

| Parameter  | Type    | Required | Description                         |
| ---------- | ------- | -------- | ----------------------------------- |
| start_date | date    | Optional | Start date of filter (`YYYY-MM-DD`) |
| end_date   | date    | Optional | End date of filter                  |
| product_id | integer | Optional | Filter by specific product ID       |
| category   | string  | Optional | Filter by product category          |

**Sample Request:**

```http
GET http://localhost:8000/sales/filter?start_date=2025-05-01&end_date=2025-05-10&category=Furniture
```

**Sample Response:**

```json
{
  "status": "success",
  "message": "Filtered sales",
  "result": [
    {
      "id": 71,
      "product_id": 4,
      "quantity": 3,
      "total_price": 450.0,
      "timestamp": "2025-05-03T15:10:12"
    },
    {
      "id": 72,
      "product_id": 4,
      "quantity": 1,
      "total_price": 150.0,
      "timestamp": "2025-05-05T09:20:17"
    }
  ]
}
```
