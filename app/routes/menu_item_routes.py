
from flask import Blueprint, jsonify, request

from app.services.menu_item_service import (
    add_menu_item,
    find_menu_item,
    list_menu_items,
    edit_menu_item,
    remove_menu_item,
    search_menu_items_by_name,
    list_available_menu_items,
)

menu_item_bp = Blueprint(
    "menu_items",
    __name__,
    url_prefix="/api/menu-items",
)


def menu_item_to_dict(menu_item):
    return {
        "id": menu_item["id"],
        "name": menu_item["name"],
        "description": menu_item["description"],
        "price": float(menu_item["price"]),
        "available": bool(menu_item["available"]),
        "created_at": menu_item["created_at"],
    }


@menu_item_bp.route("", methods=["GET"])
def get_menu_items():
    search_term = request.args.get("search")
    available_only = request.args.get("available")

    try:
        if search_term is not None:
            menu_items = search_menu_items_by_name(search_term)
        elif available_only == "true":
            menu_items = list_available_menu_items()
        else:
            menu_items = list_menu_items()

        return jsonify([
            menu_item_to_dict(item) for item in menu_items
        ]), 200

    except ValueError as error:
        return jsonify({"error": str(error)}), 400


@menu_item_bp.route("/<int:menu_item_id>", methods=["GET"])
def get_menu_item_by_id(menu_item_id):
    try:
        menu_item = find_menu_item(menu_item_id)
        return jsonify(menu_item_to_dict(menu_item)), 200
    except ValueError as error:
        return jsonify({"error": str(error)}), 404


@menu_item_bp.route("", methods=["POST"])
def create_menu_item_route():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must be a JSON object."
        }), 400

    try:
        menu_item_id = add_menu_item(
            data.get("name", ""),
            data.get("description", ""),
            data.get("price"),
            data.get("available", True),
        )

        menu_item = find_menu_item(menu_item_id)
        return jsonify(menu_item_to_dict(menu_item)), 201

    except (ValueError, TypeError) as error:
        return jsonify({"error": str(error)}), 400


@menu_item_bp.route("/<int:menu_item_id>", methods=["PUT"])
def update_menu_item_route(menu_item_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must be a JSON object."
        }), 400

    try:
        menu_item = edit_menu_item(
            menu_item_id,
            data.get("name", ""),
            data.get("description", ""),
            data.get("price"),
            data.get("available", True),
        )

        return jsonify(menu_item_to_dict(menu_item)), 200

    except ValueError as error:
        status_code = (
            404 if str(error) == "Menu item not found." else 400
        )
        return jsonify({"error": str(error)}), status_code
    except TypeError as error:
        return jsonify({"error": str(error)}), 400


@menu_item_bp.route("/<int:menu_item_id>", methods=["DELETE"])
def delete_menu_item_route(menu_item_id):
    try:
        remove_menu_item(menu_item_id)
        return jsonify({
            "message": "Menu item deleted successfully."
        }), 200

    except ValueError as error:
        message = str(error)
        status_code = (
            404 if message == "Menu item not found." else 409
        )
        return jsonify({"error": message}), status_code
