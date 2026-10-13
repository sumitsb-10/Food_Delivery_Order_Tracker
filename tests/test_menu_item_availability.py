import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from app.services.menu_item_service import (
    add_menu_item,
    list_available_menu_items,
)


def main():
    available_item_id = add_menu_item(
        "Available Test Item",
        "Available item for filtering test",
        100.00,
        True
    )

    unavailable_item_id = add_menu_item(
        "Unavailable Test Item",
        "Unavailable item for filtering test",
        120.00,
        False
    )

    print("Available test item:", available_item_id)
    print("Unavailable test item:", unavailable_item_id)

    results = list_available_menu_items()

    print("\nAvailable menu items:")

    for item in results:
        print(dict(item))

    result_ids = {item["id"] for item in results}

    assert available_item_id in result_ids
    print("\nAvailable item included: PASS")

    assert unavailable_item_id not in result_ids
    print("Unavailable item excluded: PASS")

    # Verify every returned item is actually available.
    for item in results:
        assert item["available"] == 1

    print("All returned items are available: PASS")

    print("\nMenu item availability test completed successfully.")


if __name__ == "__main__":
    main()