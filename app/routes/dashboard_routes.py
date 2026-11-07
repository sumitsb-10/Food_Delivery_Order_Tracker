from decimal import Decimal

from flask import Blueprint, jsonify

from app.services.customer_service import list_customers
from app.services.menu_item_service import list_menu_items
from app.services.order_service import list_orders


dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api")

ORDER_STATUSES = (
    "PENDING",
    "CONFIRMED",
    "PREPARING",
    "OUT_FOR_DELIVERY",
    "DELIVERED",
    "CANCELLED",
)


@dashboard_bp.route("/dashboard", methods=["GET"])
def get_dashboard():
    customers = list_customers()
    menu_items = list_menu_items()
    orders = list_orders()
    status_counts = {status: 0 for status in ORDER_STATUSES}

    for order in orders:
        status_counts[order["status"]] += 1

    delivered_order_value = sum(
        (
            Decimal(str(order["total_amount"]))
            for order in orders
            if order["status"] == "DELIVERED"
        ),
        Decimal("0.00"),
    )

    recent_orders = sorted(
        orders,
        key=lambda order: (order["order_date"], order["id"]),
        reverse=True,
    )[:5]

    return jsonify({
        "summary": {
            "customers": len(customers),
            "menu_items": len(menu_items),
            "available_menu_items": sum(
                bool(item["available"]) for item in menu_items
            ),
            "orders": len(orders),
            "delivered_order_value": float(delivered_order_value),
        },
        "orders_by_status": status_counts,
        "recent_orders": [dict(order) for order in recent_orders],
    }), 200
