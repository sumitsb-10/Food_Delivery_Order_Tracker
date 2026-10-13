import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.repositories.customer_repository import (
    create_customer,
    get_customer,
    get_all_customers,
)


def main():
    # Create a customer
   

    # Get all customers
    customers = get_all_customers()

    print("\nAll customers:")

    for customer in customers:
        print(dict(customer))


if __name__ == "__main__":
    main()