
def test_create_order_api(client, sample_records):
    response = client.post(
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

    assert response.status_code == 201

    data = response.get_json()
    assert data["order"]["status"] == "PENDING"
    assert data["order"]["total_amount"] == 200.0
    assert len(data["items"]) == 1


def test_create_order_api_rejects_missing_customer_id(client):
    response = client.post(
        "/orders",
        json={"items": [{"menu_item_id": 101, "quantity": 1}]},
    )

    assert response.status_code == 400
    assert "customer_id is required" in response.get_json()["error"]


def test_get_orders_api(client, sample_records):
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

    response = client.get("/orders")

    assert response.status_code == 200
    assert len(response.get_json()["orders"]) == 1


def test_get_order_api(client, sample_records):
    created = client.post(
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
    order_id = created.get_json()["order"]["id"]

    response = client.get(f"/orders/{order_id}")

    assert response.status_code == 200
    assert response.get_json()["order"]["id"] == order_id
    assert len(response.get_json()["items"]) == 1


def test_get_missing_order_api(client):
    response = client.get("/orders/99999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Order not found."


def test_update_order_status_api(client, sample_records):
    created = client.post(
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
    order_id = created.get_json()["order"]["id"]

    response = client.patch(
        f"/orders/{order_id}/status",
        json={"status": "CONFIRMED"},
    )

    assert response.status_code == 200
    assert response.get_json()["order"]["status"] == "CONFIRMED"


def test_update_order_status_api_rejects_invalid_transition(
    client, sample_records
):
    created = client.post(
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
    order_id = created.get_json()["order"]["id"]

    response = client.patch(
        f"/orders/{order_id}/status",
        json={"status": "DELIVERED"},
    )

    assert response.status_code == 400
    assert "cannot move from PENDING to DELIVERED" in (
        response.get_json()["error"]
    )


def test_filter_orders_by_status_api(client, sample_records):
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

    response = client.get("/orders?status=PENDING")

    assert response.status_code == 200
    assert len(response.get_json()["orders"]) == 1
    assert response.get_json()["orders"][0]["status"] == "PENDING"
