def test_home_page_loads_tracker_ui(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Food Delivery Order Tracker" in response.data
    assert b'id="dashboard"' in response.data
    assert b'id="customers"' in response.data
    assert b'id="menu"' in response.data
    assert b'id="orders"' in response.data


def test_web_assets_are_served(client):
    script = client.get("/static/app.js")
    stylesheet = client.get("/static/styles.css")

    assert script.status_code == 200
    assert b"/api/dashboard" in script.data
    assert stylesheet.status_code == 200
