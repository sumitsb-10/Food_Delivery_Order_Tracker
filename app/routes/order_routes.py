
from flask import Blueprint, jsonify, request

from app.services.order_service import (
    create_new_order,
    find_order,
    list_orders,
    change_order_status,
    list_orders_by_status,
)

order_bp = Blueprint("orders", __name__, url_prefix="/orders")


@order_bp.route("", methods=["POST"])
def create_order_route():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    customer_id = data.get("customer_id")
    items = data.get("items")

    if customer_id is None:
        return jsonify({"error": "customer_id is required."}), 400

    if not isinstance(items, list):
        return jsonify({"error": "items must be a list."}), 400

    if not items:
        return jsonify({
            "error": "An order must contain at least one menu item."
        }), 400

    if (
        not isinstance(customer_id, int)
        or isinstance(customer_id, bool)
        or customer_id <= 0
    ):
        return jsonify({
            "error": "customer_id must be a positive integer."
        }), 400

    for item in items:
        if not isinstance(item, dict):
            return jsonify({
                "error": "Each order item must be a JSON object."
            }), 400

        if "menu_item_id" not in item:
            return jsonify({
                "error": "menu_item_id is required for each order item."
            }), 400

        if "quantity" not in item:
            return jsonify({
                "error": "quantity is required for each order item."
            }), 400

        quantity = item["quantity"]

        if (
            not isinstance(quantity, int)
            or isinstance(quantity, bool)
            or quantity <= 0
        ):
            return jsonify({
                "error": "Each item quantity must be a positive integer."
            }), 400

        menu_item_id = item["menu_item_id"]

        if (
            not isinstance(menu_item_id, int)
            or isinstance(menu_item_id, bool)
            or menu_item_id <= 0
        ):
            return jsonify({
                "error": "menu_item_id must be a positive integer."
            }), 400

    try:
        order_id = create_new_order(customer_id, items)
        result = find_order(order_id)

        return jsonify({
            "message": "Order created successfully.",
            "order": dict(result["order"]),
            "items": [dict(item) for item in result["items"]],
        }), 201

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

@order_bp.route("", methods=["GET"])
def get_orders_route():
    if "status" in request.args:
        status = request.args.get("status", "").strip()

        if not status:
            return jsonify({
                "error": "status cannot be empty."
            }), 400

        try:
            orders = list_orders_by_status(status)
            return jsonify({
                "orders": [dict(order) for order in orders]
            }), 200

        except ValueError as error:
            return jsonify({"error": str(error)}), 400

    orders = list_orders()
    return jsonify({
        "orders": [dict(order) for order in orders]
    }), 200


@order_bp.route("/<int:order_id>", methods=["GET"])
def get_order_route(order_id):
    if order_id <= 0:
        return jsonify({
            "error": "order_id must be a positive integer."
        }), 400

    try:
        result = find_order(order_id)

        return jsonify({
            "order": dict(result["order"]),
            "items": [dict(item) for item in result["items"]],
        }), 200

    except ValueError as error:
        if str(error) == "Order not found.":
            return jsonify({"error": str(error)}), 404

        return jsonify({"error": str(error)}), 400


@order_bp.route("/<int:order_id>/status", methods=["PATCH"])
def update_order_status_route(order_id):
    if order_id <= 0:
        return jsonify({
            "error": "order_id must be a positive integer."
        }), 400

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must be a JSON object."
        }), 400

    new_status = data.get("status")

    if not isinstance(new_status, str) or not new_status.strip():
        return jsonify({
            "error": "status is required and must be a non-empty string."
        }), 400

    new_status = new_status.strip().upper()

    try:
        order = change_order_status(order_id, new_status)

        return jsonify({
            "message": "Order status updated successfully.",
            "order": dict(order),
        }), 200

    except ValueError as error:
        message = str(error)

        if message == "Order not found.":
            return jsonify({"error": message}), 404

        return jsonify({"error": message}), 400
