#booking
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    intent = req['queryResult']['intent']['displayName']

    if intent == "Search Guides":
        location = req['queryResult']['parameters'].get('geo-city', 'your location')
        language = req['queryResult']['parameters'].get('Language')
        date = req['queryResult']['parameters'].get('date')

        # Mock data for guide search
        guides = [
            {"name": "John Doe", "language": "English", "contact": "1234567890"},
            {"name": "Ravi Kumar", "language": "Hindi", "contact": "9876543210"},
        ]

        # Filter guides by language
        filtered_guides = [
            guide for guide in guides if guide['language'].lower() == language.lower()
        ]

        if filtered_guides:
            guide_list = "\n".join(
                [f"{g['name']} (Language: {g['language']}, Contact: {g['contact']})"
                 for g in filtered_guides]
            )
            return jsonify({
                "fulfillmentText": f"Found the following guides in {location}:\n{guide_list}\nWould you like to book one?"
            })
        else:
            return jsonify({
                "fulfillmentText": f"Sorry, no guides are available in {location} who speak {language}."
            })

    elif intent == "Confirm and Request Guide":
        guide_name = req['queryResult']['parameters'].get('guide_name', 'the guide')

        return jsonify({
            "fulfillmentText": f"Your request has been sent to {guide_name}. They will contact you soon."
        })

    return jsonify({"fulfillmentText": "I didn't understand that."})


if __name__ == "__main__":
    app.run(port=5000)
