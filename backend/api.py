from flask import Flask, jsonify
from flask_cors import CORS
from backend.main_pipeline import run_pipeline

app = Flask(__name__)
CORS(app)

cached_result = None


@app.route("/")
def home():
    return jsonify({
        "message": "PROTEUS Backend Running!"
    })


@app.route("/forecast")
def forecast():

    global cached_result

    if cached_result is None:
        print("Running AI pipeline...")
        cached_result = run_pipeline()
    else:
        print("Using cached result.")

    return jsonify(cached_result)


if __name__ == "__main__":
    app.run(debug=True)