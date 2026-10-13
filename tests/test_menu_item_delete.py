import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.services.menu_item_service import add_menu_item, remove_menu_item


def main():
    menu_item_id = add_menu_item(
        "Temp Delete Test Item",
        "Created for delete test",
        99.99,
        True,
    )

    try:
        removed = remove_menu_item(menu_item_id)
        print("Menu item deleted successfully:", removed)
    except Exception as error:
        print("Error:", error)


if __name__ == "__main__":
    main()