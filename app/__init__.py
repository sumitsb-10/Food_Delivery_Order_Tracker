
from flask import Flask


def create_app():
    app = Flask(__name__)

    from app.routes.health_routes import health_bp
    from app.routes.customer_routes import customer_bp
    from app.routes.menu_item_routes import menu_item_bp
    from app.routes.order_routes import order_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(menu_item_bp)
    app.register_blueprint(order_bp)

    return app
