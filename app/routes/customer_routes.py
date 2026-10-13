
from flask import Blueprint, jsonify, request

from app.services.customer_service import (
    add_customer,
    find_customer,
    list_customers,
    edit_customer,
    remove_customer,
    search_customers_by_name,
)

customer_bp = Blueprint("customers", __name__, url_prefix="/api/customers")


def customer_to_dict(customer):
    return {
        "id": customer["id"],
        "name": customer["name"],
        "phone": customer["phone"],
        "address": customer["address"],
        "created_at": customer["created_at"],
    }


@customer_bp.route("", methods=["GET"])
def get_customers():
    search_term = request.args.get("search")

    try:
        if search_term is not None:
            customers = search_customers_by_name(search_term)
        else:
            customers = list_customers()

        return jsonify([
            customer_to_dict(customer)
            for customer in customers
        ]), 200

    except ValueError as error:
        return jsonify({"error": str(error)}), 400


@customer_bp.route("/<int:customer_id>", methods=["GET"])
def get_customer_by_id(customer_id):
    try:
        customer = find_customer(customer_id)
        return jsonify(customer_to_dict(customer)), 200
    except ValueError as error:
        return jsonify({"error": str(error)}), 404


@customer_bp.route("", methods=["POST"])
def create_customer_route():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    try:
        customer_id = add_customer(
            data.get("name", ""),
            data.get("phone", ""),
            data.get("address", ""),
        )

        customer = find_customer(customer_id)
        return jsonify(customer_to_dict(customer)), 201

    except ValueError as error:
        return jsonify({"error": str(error)}), 400


@customer_bp.route("/<int:customer_id>", methods=["PUT"])
def update_customer_route(customer_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    try:
        customer = edit_customer(
            customer_id,
            data.get("name", ""),
            data.get("phone", ""),
            data.get("address", ""),
        )
        return jsonify(customer_to_dict(customer)), 200

    except ValueError as error:
        status_code = 404 if str(error) == "Customer not found." else 400
        return jsonify({"error": str(error)}), status_code


@customer_bp.route("/<int:customer_id>", methods=["DELETE"])
def delete_customer_route(customer_id):
    try:
        remove_customer(customer_id)
        return jsonify({
            "message": "Customer deleted successfully."
        }), 200

    except ValueError as error:
        message = str(error)
        status_code = 404 if message == "Customer not found." else 409
        return jsonify({"error": message}), status_code
