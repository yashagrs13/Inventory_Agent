# app.py
import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from src.db import init_db

load_dotenv()


def create_app():
    """Flask application factory."""
    app = Flask(__name__)
    CORS(app)

    app.config['UPLOAD_FOLDER'] = 'data'
    app.config['REPORTS_FOLDER'] = 'reports'
    app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

    # Ensure required directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['REPORTS_FOLDER'], exist_ok=True)

    # Initialize database
    init_db()

    # Register blueprints
    from src.routes.upload import upload_bp
    from src.routes.results import results_bp
    from src.routes.history import history_bp
    from src.routes.chat import chat_bp
    from src.routes.alerts import alerts_bp
    from src.routes.forecast import forecast_bp
    from src.routes.audit import audit_bp

    app.register_blueprint(upload_bp)
    app.register_blueprint(results_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(alerts_bp)
    app.register_blueprint(forecast_bp)
    app.register_blueprint(audit_bp)

    # Health check at app level
    @app.route('/health')
    def health_check():
        return jsonify({"status": "healthy", "message": "Inventory Agent API is running"})

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
