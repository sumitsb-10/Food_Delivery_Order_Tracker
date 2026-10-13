from sqlite3 import IntegrityError

from app.repositories.menu_item_repository import (
    create_menu_item,
    get_menu_item,
    get_all_menu_items,
    update_menu_item,
    delete_menu_item,
    search_menu_items,
    get_available_menu_items,
)


def add_menu_item(name, description, price, available=True):
    if not name.strip():
        raise ValueError("Menu item name is required.")

    if price <= 0:
        raise ValueError("Menu item price must be greater than zero.")

    if not isinstance(available, bool):
        raise ValueError("Availability must be True or False.")

    return create_menu_item(name, description, price, available)


def find_menu_item(menu_item_id):
    menu_item = get_menu_item(menu_item_id)

    if menu_item is None:
        raise ValueError("Menu item not found.")

    return menu_item


def list_menu_items():
    return get_all_menu_items()


def edit_menu_item(menu_item_id, name, description, price, available):
    if not name.strip():
        raise ValueError("Menu item name is required.")

    if price <= 0:
        raise ValueError("Menu item price must be greater than zero.")

    if not isinstance(available, bool):
        raise ValueError("Availability must be True or False.")

    rows_updated = update_menu_item(
        menu_item_id,
        name,
        description,
        price,
        available
    )

    if rows_updated == 0:
        raise ValueError("Menu item not found.")

    return get_menu_item(menu_item_id)


def remove_menu_item(menu_item_id):
    try:
        rows_deleted = delete_menu_item(menu_item_id)

    except IntegrityError:
        raise ValueError(
            "Menu item cannot be deleted because it is used in an existing order."
        )

    if rows_deleted == 0:
        raise ValueError("Menu item not found.")

    return True

def search_menu_items_by_name(search_term):
    if not isinstance(search_term, str):
        raise ValueError("Search term must be text.")

    if not search_term.strip():
        raise ValueError("Search term is required.")

    return search_menu_items(search_term.strip())

def list_available_menu_items():
    return get_available_menu_items()