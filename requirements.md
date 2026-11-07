# Version 1 Requirements

This document defines the first release of the Food Delivery Order Tracker. The product is an operations tool for one small food-delivery business, not a customer-facing marketplace.

## Functional requirements

- Create, view, update, delete, and search customer records.
- Create, view, update, delete, search, and filter menu items by availability.
- Create orders for existing customers from one or more available menu items.
- Calculate each order total from the current menu-item prices and store line-item price snapshots.
- List and view orders, filter by status, and validate status transitions.
- Report customer/menu/order counts, order counts by status, recent orders, and total value of delivered orders.
- Provide a responsive browser interface for dashboard, customer, menu, and order workflows.
- Provide a JSON REST API for the same core operations.

## Business rules

- Customer name, phone, and address are required; phone numbers are unique.
- Menu-item name and a positive price are required.
- An order must have at least one item, all quantities must be positive integers, and all referenced records must exist.
- Unavailable menu items cannot be ordered.
- Orders start as `PENDING`.
- Allowed transitions are `PENDING` to `CONFIRMED` or `CANCELLED`; `CONFIRMED` to `PREPARING` or `CANCELLED`; `PREPARING` to `OUT_FOR_DELIVERY` or `CANCELLED`; and `OUT_FOR_DELIVERY` to `DELIVERED`.
- Orders cannot be deleted through the API. Customers or menu items referenced by an order cannot be deleted.

## Non-functional requirements

- Keep application logic modular across Flask routes, services, and repositories.
- Validate API input and return clear HTTP errors for invalid or conflicting requests.
- Use SQLite transactions for order creation and enable foreign-key checks on each connection.
- Allow the SQLite database path to be configured with `FOOD_DELIVERY_DATABASE`.
- Keep the app and UI usable on desktop and mobile screen sizes.
- Test API, business rules, database integrity, and browser delivery with pytest.

## Technology

- Python and Flask
- SQLite
- HTML, CSS, and browser JavaScript
- pytest

## Out of scope

Version 1 does not implement accounts/login, restaurants, customer shopping carts, payment processing, delivery partners, GPS tracking, notifications, reviews, or complex analytics. Delivered order value is a report based on order totals; it does not indicate that a payment was collected.
