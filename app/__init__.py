
from flask import Flask


def create_app():
    app = Flask(__name__)

    from app.routes.web_routes import web_bp
    from app.routes.health_routes import health_bp
    from app.routes.customer_routes import customer_bp
    from app.routes.menu_item_routes import menu_item_bp
    from app.routes.order_routes import order_bp
    from app.routes.dashboard_routes import dashboard_bp

    app.register_blueprint(web_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(menu_item_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(dashboard_bp)

    return app
