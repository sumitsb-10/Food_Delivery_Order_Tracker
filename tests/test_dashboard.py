def test_dashboard_reports_empty_database(client):
    response = client.get("/api/dashboard")

    assert response.status_code == 200
    data = response.get_json()
    assert data["summary"] == {
        "customers": 0,
        "menu_items": 0,
        "available_menu_items": 0,
        "orders": 0,
        "delivered_order_value": 0.0,
    }
    assert all(count == 0 for count in data["orders_by_status"].values())
    assert data["recent_orders"] == []


def test_dashboard_reports_order_activity(client, sample_records):
    created = client.post(
        "/orders",
        json={
            "customer_id": sample_records["customer_id"],
            "items": [
                {
                    "menu_item_id": sample_records["burger_id"],
                    "quantity": 2,
                }
            ],
        },
    )
    order_id = created.get_json()["order"]["id"]

    for status in ("CONFIRMED", "PREPARING", "OUT_FOR_DELIVERY", "DELIVERED"):
        response = client.patch(
            f"/orders/{order_id}/status",
            json={"status": status},
        )
        assert response.status_code == 200

    response = client.get("/api/dashboard")

    assert response.status_code == 200
    data = response.get_json()
    assert data["summary"] == {
        "customers": 1,
        "menu_items": 2,
        "available_menu_items": 2,
        "orders": 1,
        "delivered_order_value": 200.0,
    }
    assert data["orders_by_status"]["DELIVERED"] == 1
    assert data["orders_by_status"]["PENDING"] == 0
    assert data["recent_orders"][0]["id"] == order_id


def test_dashboard_includes_only_delivered_order_value(client, sample_records):
    client.post(
        "/orders",
        json={
            "customer_id": sample_records["customer_id"],
            "items": [
                {
                    "menu_item_id": sample_records["burger_id"],
                    "quantity": 1,
                }
            ],
        },
    )

    response = client.get("/api/dashboard")

    assert response.get_json()["summary"]["delivered_order_value"] == 0.0
