
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
    status = request.args.get("status")

    try:
        if status:
            orders = list_orders_by_status(status)
        else:
            orders = list_orders()

        return jsonify({"orders": [dict(order) for order in orders]}), 200

    except ValueError as error:
        return jsonify({"error": str(error)}), 400


@order_bp.route("/<int:order_id>", methods=["GET"])
def get_order_route(order_id):
    try:
        result = find_order(order_id)

        return jsonify({
            "order": dict(result["order"]),
            "items": [dict(item) for item in result["items"]],
        }), 200

    except ValueError as error:
        return jsonify({"error": str(error)}), 404


@order_bp.route("/<int:order_id>/status", methods=["PATCH"])
def update_order_status_route(order_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    new_status = data.get("status")

    if not isinstance(new_status, str):
        return jsonify({"error": "status is required and must be text."}), 400

    try:
        order = change_order_status(order_id, new_status.strip().upper())
        return jsonify({
            "message": "Order status updated successfully.",
            "order": dict(order),
        }), 200

    except ValueError as error:
        message = str(error)
        status_code = 404 if message == "Order not found." else 400
        return jsonify({"error": message}), status_code
