from flask import Flask
from flask_cors import CORS
from main_pipeline import run_pipeline

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return {
        "message": "PROTEUS Backend Running!"
    }

@app.route("/forecast")
def forecast():

    result = run_pipeline()

    return result

if __name__ == "__main__":
    app.run(debug=True)