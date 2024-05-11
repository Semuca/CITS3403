"""Entry point for the flask application"""

from app import create_app

flask_app = create_app('dev')
if __name__ == "__main__":
    flask_app.run("0.0.0.0", port=5000)