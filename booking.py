from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize Firebase
cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    intent = req['queryResult']['intent']['displayName']

    if intent == "Search Guides":
        location = req['queryResult']['parameters'].get('geo-city', 'your location').lower()
        language = req['queryResult']['parameters'].get('Language', '').lower()

        try:
            # Fetch guides from Firebase
            guides_ref = db.collection('guides')
            guides = [
                guide.to_dict()
                for guide in guides_ref.stream()
                if guide.to_dict().get('location', '').lower() == location and
                   guide.to_dict().get('language', '').lower() == language
            ]

            if guides:
                guide_list = "\n".join(
                    [f"{g['name']} (Language: {g['language']}, Contact: {g['contact']})"
                     for g in guides]
                )
                return jsonify({
                    "fulfillmentText": f"Found the following guides in {location}:\n{guide_list}\nWould you like to book one?"
                })
            else:
                return jsonify({
                    "fulfillmentText": f"Sorry, no guides are available in {location} who speak {language}."
                })

        except Exception as e:
            print(f"Error: {e}")
            return jsonify({
                "fulfillmentText": "An error occurred while searching for guides. Please try again later."
            })

    elif intent == "Confirm and Request Guide":
        guide_name = req['queryResult']['parameters'].get('guide_name', 'the guide')

        return jsonify({
            "fulfillmentText": f"Your request has been sent to {guide_name}. They will contact you soon."
        })

    return jsonify({"fulfillmentText": "I didn't understand that."})


if __name__ == "__main__":
    app.run(host = "0.0.0.0",port=5000)
