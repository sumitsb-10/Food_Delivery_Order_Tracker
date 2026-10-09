# Food Delivery Order Management System

A simple food delivery application developed as an individual learning project. The system focuses on managing customers, menu items, and orders while practicing core software-development concepts.

## Problem Statement

Small food-delivery operations need a simple way to manage customer information, menu items, orders, and pending work.

This application provides basic CRUD operations, validation, search/filtering, and simple reports through a web interface.

## Features

- Customer/profile management
- Menu item management
- Food order management
- CRUD operations
- Search and filtering
- Input and business validation
- Order status tracking
- Simple dashboard/reports
- Exception handling
- Relational database
- Basic REST API
- Basic test cases

## Core Entities

```text
Customer
MenuItem
Order
OrderItem
```

Relationships:

```text
Customer 1 ──── * Order
Order    1 ──── * OrderItem
MenuItem 1 ──── * OrderItem
```

## Tech Stack

- **Backend:** Python + Flask/FastAPI
- **Database:** SQLite / PostgreSQL
- **Frontend:** HTML, CSS, JavaScript
- **Testing:** pytest
- **Version Control:** Git + GitHub

## Project Structure

```text
food-delivery-tracker/
├── app/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── repositories/
│   └── validators/
├── tests/
├── database/
├── templates/
├── static/
├── requirements.txt
├── README.md
└── run.py
```

## Main Order Flow

```text
PENDING
   ↓
CONFIRMED
   ↓
PREPARING
   ↓
OUT_FOR_DELIVERY
   ↓
DELIVERED
```

Orders may also be cancelled according to business rules.

## Learning Objectives

This project is intended to strengthen:

- Programming fundamentals
- OOP and data structures
- SQL and relational databases
- CRUD and validation
- Exception handling and debugging
- HTTP/API concepts
- Git/GitHub
- Testing and documentation
- Problem decomposition and Design Thinking

## Development Roadmap

- [ ] Requirements & Design
- [ ] Database Design
- [ ] Customer CRUD
- [ ] Menu CRUD
- [ ] Order Management
- [ ] Validation & Exceptions
- [ ] Search & Filtering
- [ ] REST API
- [ ] Dashboard
- [ ] Simple Web UI
- [ ] Testing
- [ ] Documentation

## Out of Scope

Version 1 will not include:

- Online payments
- GPS/live tracking
- Delivery partner management
- Reviews/ratings
- Notifications
- Advanced authentication
- Complex analytics

## Project Status

**Status:** Planning / Initial Development

This project is primarily intended for learning and is not a production-ready food delivery platform.

## Author

**Name:** Sumit Singh Bora 
**GitHub:** `<your-github-profile>`