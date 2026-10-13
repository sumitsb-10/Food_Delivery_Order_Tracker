
def test_health_endpoint(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "success"


def test_get_menu_items(client):
    response = client.get("/api/menu-items")

    assert response.status_code == 200
    assert response.get_json() == []


def test_search_menu_items(client):
    response = client.get("/api/menu-items?search=Burger")

    assert response.status_code == 200
    assert response.get_json() == []


def test_available_menu_items(client):
    response = client.get("/api/menu-items?available=true")

    assert response.status_code == 200
    assert response.get_json() == []


def test_create_menu_item_rejects_negative_price(client):
    response = client.post(
        "/api/menu-items",
        json={
            "name": "Invalid Item",
            "description": "Validation test",
            "price": -10,
            "available": True,
        },
    )

    assert response.status_code == 400
    assert "error" in response.get_json()

def test_create_menu_item(client):
    response = client.post(
        "/api/menu-items",
        json={
            "name": "Paneer Wrap",
            "description": "Grilled paneer wrap",
            "price": 150,
            "available": True,
        },
    )

    assert response.status_code in (200, 201)
    data = response.get_json()
    assert data["name"] == "Paneer Wrap"
    assert float(data["price"]) == 150.0


def test_get_menu_item_by_id(client):
    create_response = client.post(
        "/api/menu-items",
        json={
            "name": "Test Pizza",
            "description": "Cheese pizza",
            "price": 220,
            "available": True,
        },
    )

    assert create_response.status_code in (200, 201)
    item_id = create_response.get_json()["id"]

    response = client.get(f"/api/menu-items/{item_id}")

    assert response.status_code == 200
    assert response.get_json()["name"] == "Test Pizza"


def test_update_menu_item(client):
    create_response = client.post(
        "/api/menu-items",
        json={
            "name": "Old Name",
            "description": "Test item",
            "price": 100,
            "available": True,
        },
    )

    assert create_response.status_code in (200, 201)
    item_id = create_response.get_json()["id"]

    response = client.put(
        f"/api/menu-items/{item_id}",
        json={
            "name": "Updated Name",
            "description": "Updated description",
            "price": 125,
            "available": False,
        },
    )

    assert response.status_code == 200

    get_response = client.get(f"/api/menu-items/{item_id}")
    assert get_response.status_code == 200
    assert get_response.get_json()["name"] == "Updated Name"
    assert float(get_response.get_json()["price"]) == 125.0
    assert get_response.get_json()["available"] is False


def test_delete_menu_item(client):
    create_response = client.post(
        "/api/menu-items",
        json={
            "name": "Item To Delete",
            "description": "Temporary test item",
            "price": 75,
            "available": True,
        },
    )

    assert create_response.status_code in (200, 201)
    item_id = create_response.get_json()["id"]

    delete_response = client.delete(f"/api/menu-items/{item_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/api/menu-items/{item_id}")
    assert get_response.status_code == 404

def test_get_nonexistent_menu_item(client):
    response = client.get("/api/menu-items/99999")

    assert response.status_code == 404
    assert "error" in response.get_json()


def test_delete_nonexistent_menu_item(client):
    response = client.delete("/api/menu-items/99999")

    assert response.status_code == 404
    assert "error" in response.get_json()

def test_create_menu_item_rejects_missing_name(client):
    response = client.post(
        "/api/menu-items",
        json={
            "description": "Item without a name",
            "price": 100,
            "available": True,
        },
    )

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_create_menu_item_rejects_zero_price(client):
    response = client.post(
        "/api/menu-items",
        json={
            "name": "Zero Price Item",
            "description": "Invalid price test",
            "price": 0,
            "available": True,
        },
    )

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_create_menu_item_rejects_invalid_availability(client):
    response = client.post(
        "/api/menu-items",
        json={
            "name": "Invalid Availability",
            "description": "Availability must be boolean",
            "price": 100,
            "available": "yes",
        },
    )

    assert response.status_code == 400
    assert "error" in response.get_json()