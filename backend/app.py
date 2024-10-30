from flask import Flask, jsonify, request
from flask_cors import CORS

from airbnb_recommendator import AirbnbRecommendator

app = Flask(__name__)
CORS(app)


@app.route("/respond", methods=["POST"])
def recommend_airbnb():
    """Recommend airbnb route

    Returns:
        recommendation (Json): Airbnb recommendation
    """
    data = request.json
    user_message = data.get("message", "")

    airbnb_recommendator = AirbnbRecommendator()
    recommendation = airbnb_recommendator.get_recommendation(
        user_query=user_message,
    )
    
    print(f"Frontend recommendation: {recommendation}")
    print()

    return jsonify(recommendation)


if __name__ == "__main__":
    app.run(debug=True)
