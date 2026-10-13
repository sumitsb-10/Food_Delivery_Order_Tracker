import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from app.services.menu_item_service import (
    add_menu_item,
    search_menu_items_by_name,
)


def main():
    burger_1 = add_menu_item(
        "Search Burger",
        "Burger for search testing",
        150.00,
        True
    )

    burger_2 = add_menu_item(
        "Chicken Burger",
        "Chicken burger for search testing",
        220.00,
        True
    )

    pizza = add_menu_item(
        "Search Pizza",
        "Pizza for search testing",
        250.00,
        True
    )

    print("Created test menu items:")
    print("Burger 1:", burger_1)
    print("Burger 2:", burger_2)
    print("Pizza:", pizza)

    # Search using lowercase.
    results = search_menu_items_by_name("burger")

    print("\nSearch results for 'burger':")

    for item in results:
        print(dict(item))

    result_ids = {item["id"] for item in results}

    assert burger_1 in result_ids
    assert burger_2 in result_ids
    assert pizza not in result_ids

    print("\nPartial name search: PASS")

    # Search should be case-insensitive.
    results = search_menu_items_by_name("BURGER")

    result_ids = {item["id"] for item in results}

    assert burger_1 in result_ids
    assert burger_2 in result_ids

    print("Case-insensitive search: PASS")

    # Search term with spaces should be trimmed.
    results = search_menu_items_by_name("  burger  ")

    result_ids = {item["id"] for item in results}

    assert burger_1 in result_ids
    assert burger_2 in result_ids

    print("Search term trimming: PASS")

    # Empty search should fail.
    try:
        search_menu_items_by_name("   ")

        assert False, (
            "Expected ValueError was not raised."
        )

    except ValueError as error:
        print("Empty search validation: PASS")
        print("Expected error:", error)

    print("\nMenu item search test completed successfully.")


if __name__ == "__main__":
    main()