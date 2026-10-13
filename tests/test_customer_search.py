import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from app.services.customer_service import (
    add_customer,
    search_customers_by_name,
)


def main():
    customer_1 = add_customer(
        "Search Rahul",
        "9000000001",
        "Bengaluru"
    )

    customer_2 = add_customer(
        "Rahul Kumar",
        "9000000002",
        "Mysuru"
    )

    customer_3 = add_customer(
        "Search Priya",
        "9000000003",
        "Bengaluru"
    )

    print("Created test customers:")
    print("Customer 1:", customer_1)
    print("Customer 2:", customer_2)
    print("Customer 3:", customer_3)

    # Partial name search.
    results = search_customers_by_name("rahul")

    print("\nSearch results for 'rahul':")

    for customer in results:
        print(dict(customer))

    result_ids = {customer["id"] for customer in results}

    assert customer_1 in result_ids
    assert customer_2 in result_ids
    assert customer_3 not in result_ids

    print("\nPartial name search: PASS")

    # Case-insensitive search.
    results = search_customers_by_name("RAHUL")

    result_ids = {customer["id"] for customer in results}

    assert customer_1 in result_ids
    assert customer_2 in result_ids

    print("Case-insensitive search: PASS")

    # Search term trimming.
    results = search_customers_by_name("  rahul  ")

    result_ids = {customer["id"] for customer in results}

    assert customer_1 in result_ids
    assert customer_2 in result_ids

    print("Search term trimming: PASS")

    # Empty search validation.
    try:
        search_customers_by_name("   ")

        assert False, (
            "Expected ValueError was not raised."
        )

    except ValueError as error:
        print("Empty search validation: PASS")
        print("Expected error:", error)

    print("\nCustomer search test completed successfully.")


if __name__ == "__main__":
    main()