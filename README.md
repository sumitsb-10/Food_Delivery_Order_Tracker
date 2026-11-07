# Food Delivery Order Tracker

A lightweight food-delivery operations app for managing customers, menu items, and orders. It includes a responsive browser interface, a JSON REST API, SQLite persistence, and automated tests.

## Features

- Customer and menu-item create, view, update, delete, and name search
- Availability filtering for menu items
- Multi-item order creation with server-calculated prices and totals
- Order history, status filtering, and validated status transitions
- Dashboard counts, order-status summary, recent orders, and delivered order value
- Responsive UI served by Flask; no frontend build step or external runtime service
- SQLite foreign-key enforcement and transaction-safe order creation

## Requirements

- Python 3.10 or later
- Dependencies listed in `requirements.txt`

## Run locally

From the project directory, create/activate a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Initialize the SQLite database and optionally add sample data (safe to rerun):

```powershell
python database\init_db.py
python database\seed_db.py
```

Start the app:

```powershell
python run.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000). To use another SQLite file, set `FOOD_DELIVERY_DATABASE` to its path before starting the app. The database parent folder is created automatically. `database\reset_db.py` deletes and recreates the development database; it is destructive.

## Web interface

The home page provides the dashboard and forms for customer management, menu management, and order creation/status updates. Search fields filter customers and menu items. Order status choices follow the allowed flow:

```text
PENDING -> CONFIRMED -> PREPARING -> OUT_FOR_DELIVERY -> DELIVERED
   |           |            |
   +-----------+------------+-> CANCELLED
```

The dashboard's delivered value sums the totals of delivered orders; it is an operational report, not a payment ledger.

## REST API

All responses use JSON except the browser UI.

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/dashboard` | Counts, status totals, recent orders, delivered value |
| `GET`, `POST` | `/api/customers` | List/search or create customers |
| `GET`, `PUT`, `DELETE` | `/api/customers/<id>` | Read, update, or delete a customer |
| `GET`, `POST` | `/api/menu-items` | List/search/filter or create menu items |
| `GET`, `PUT`, `DELETE` | `/api/menu-items/<id>` | Read, update, or delete a menu item |
| `GET`, `POST` | `/orders` | List/filter orders or create an order |
| `GET` | `/orders/<id>` | Read an order and its line items |
| `PATCH` | `/orders/<id>/status` | Move an order to a valid next status |

Use `?search=<text>` on customer/menu list endpoints, `?available=true` for available menu items, and `?status=<status>` on `/orders`. Creating an order requires a positive `customer_id` and a non-empty `items` array; each item contains a positive `menu_item_id` and `quantity`.

Example:

```json
{
  "customer_id": 1,
  "items": [
    { "menu_item_id": 1, "quantity": 2 }
  ]
}
```

## Tests

```powershell
python -m pytest -q
```

Tests create an isolated SQLite database for each test. No production data is used.

## Project scope

This is a learning project and is not production-ready. Version 1 intentionally excludes user authentication, online payments, restaurant management, delivery-partner/GPS tracking, notifications, reviews, and complex analytics.

## Project structure

```text
app/
  repositories/   SQLite queries and transaction helpers
  routes/         Flask API and web routes
  services/       Validation and order business rules
  static/         Browser JavaScript and CSS
  templates/      Main web page
database/         SQLite schema and setup/seed/reset scripts
tests/            pytest test suite
run.py            Local Flask entry point
```

## Author

Sumit Singh Bora · [GitHub](https://github.com/sumit-sb-10)
