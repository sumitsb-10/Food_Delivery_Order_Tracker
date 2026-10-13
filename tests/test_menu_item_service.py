import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.services.menu_item_service import (
    add_menu_item,
    find_menu_item,
    list_menu_items,
    edit_menu_item,
    remove_menu_item,
)


def main():
    # CREATE
    menu_item_id = add_menu_item(
        "Chicken Burger",
        "Grilled chicken burger",
        180.00,
        True,
    )

    print("Created:", menu_item_id)

    # READ
    menu_item = find_menu_item(menu_item_id)

    print("Found:")
    print(dict(menu_item))

    # READ ALL
    menu_items = list_menu_items()

    print("All menu items:")
    for item in menu_items:
        print(dict(item))

    # UPDATE
    updated_item = edit_menu_item(
        menu_item_id,
        "Chicken Burger",
        "Grilled chicken burger with cheese",
        200.00,
        True,
    )

    print("Updated:")
    print(dict(updated_item))

    # DELETE
    removed = remove_menu_item(menu_item_id)

    print("Deleted:", removed)


if __name__ == "__main__":
    main()