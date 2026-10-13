from sqlite3 import IntegrityError

from app.repositories.customer_repository import (
    create_customer,
    get_customer,
    get_all_customers,
    update_customer,
    delete_customer,
    search_customers,
)

def add_customer(name, phone, address):
    if not name.strip():
        raise ValueError("Customer name is required.")

    if not phone.strip():
        raise ValueError("Customer phone is required.")

    if not address.strip():
        raise ValueError("Customer address is required.")

    try:
        return create_customer(name, phone, address)
    except IntegrityError:
        raise ValueError("A customer with this phone number already exists.")


def find_customer(customer_id):
    customer = get_customer(customer_id)

    if customer is None:
        raise ValueError("Customer not found.")

    return customer


def list_customers():
    return get_all_customers()
def edit_customer(customer_id, name, phone, address):
    if not name.strip():
        raise ValueError("Customer name is required.")

    if not phone.strip():
        raise ValueError("Customer phone is required.")

    if not address.strip():
        raise ValueError("Customer address is required.")

    try:
        rows_updated = update_customer(
            customer_id,
            name,
            phone,
            address
        )
    except IntegrityError:
        raise ValueError(
            "A customer with this phone number already exists."
        )

    if rows_updated == 0:
        raise ValueError("Customer not found.")

    return get_customer(customer_id)


def remove_customer(customer_id):
    try:
        rows_deleted = delete_customer(customer_id)
    except IntegrityError:
        raise ValueError(
            "Customer cannot be deleted because they have existing orders."
        )

    if rows_deleted == 0:
        raise ValueError("Customer not found.")

    return True

def search_customers_by_name(search_term):
    if not isinstance(search_term, str):
        raise ValueError("Search term must be text.")

    if not search_term.strip():
        raise ValueError("Search term is required.")

    return search_customers(search_term.strip())