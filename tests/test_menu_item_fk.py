import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.services.menu_item_service import remove_menu_item


def main():
   try:
    result = remove_menu_item(1)
    print("Menu item deleted:", result)
   except ValueError as error:
    print("Application error:", error)


if __name__ == "__main__":
    main()