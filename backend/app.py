from flask import Flask, jsonify, request
from flask_cors import CORS

from airbnb_recommendator_routine import AirbnbRecommendatorRoutine

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
    print(f"User input: {user_message}")
    
    airbnb_recommendation_routine = AirbnbRecommendatorRoutine()
    recommendation = airbnb_recommendation_routine.airbnb_recommendation_routine(user_message=user_message)
    
    print(f"Frontend recommendation: {recommendation}")
    print()
    
    return jsonify(recommendation)


if __name__ == "__main__":
    app.run(debug=True)
