from flask import Flask
from src.controllers.controller import productos_c

app = Flask(__name__,template_folder="src/templates")

app.register_blueprint(productos_c)

if __name__ == "__main__":
  app.run(debug=True)