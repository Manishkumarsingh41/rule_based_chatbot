from flask import Flask, render_template, request, jsonify
import re
import difflib
import requests

app = Flask(__name__)

def chatbot_response(user_input):
    greetings = ["hi", "hello", "hey", "greetings", "what's up", "howdy"]
    keywords = ["weather", "time", "name", "age", "food", "hobby", "help"]
    
    user_input = user_input.lower()

    if user_input in greetings:
        return "Hello! How can I help you today?"

    elif user_input in ["how are you", "how are you doing"]:
        return "I'm just a bot, but I'm doing well! How about you?"

    elif user_input in ["what is your name", "who are you"]:
        return "My name is Chatbot! What's yours?"

    elif re.search(r"\bage\b", user_input):
        return "I don't have an age like humans do, but I'm always learning new things!"

    elif re.search(r"\bhobby\b", user_input):
        return "I love helping people! What's your favorite hobby?"

    elif re.search(r"\bfood\b", user_input):
        return "I don't eat, but I hear pizza is a popular choice! What's your favorite food?"

    elif re.search(r"\bhelp\b", user_input):
        return "I'm here to assist you! Ask me anything you'd like."

    elif re.search(r"\bweather\b", user_input):
        return "The weather is great today! What do you want to know about it?"

    elif re.search(r"\btime\b", user_input):
        return "I can’t tell the time, but I can help with time zones if needed!"

    elif re.search(r"\byes\b", user_input):
        return "Great! Let me know if you need anything else."

    elif re.search(r"\bno\b", user_input):
        return "No worries! Feel free to ask me anything."

    else:
        closest_match = difflib.get_close_matches(user_input, keywords, n=1)
        if closest_match:
            if closest_match[0] == "weather":
                return "It seems like you meant 'weather'. The weather is great today!"
            elif closest_match[0] == "time":
                return "It seems like you meant 'time'. I can’t tell the time, but I can help with time zones!"
            elif closest_match[0] == "name":
                return "It seems like you meant 'name'. My name is Chatbot! What's yours?"
            elif closest_match[0] == "age":
                return "It seems like you meant 'age'. I don't have an age, but I was created to help!"
            elif closest_match[0] == "food":
                return "It seems like you meant 'food'. What's your favorite food?"
            elif closest_match[0] == "hobby":
                return "It seems like you meant 'hobby'. What's your favorite hobby?"
        else:
            # If no match is found, call the external API for a more complex response
            return fetch_external_response(user_input)

def fetch_external_response(user_message):
    """Fetches response from the external API if user input doesn't match any predefined patterns."""
    try:
        response = requests.post(
            "https://backend.buildpicoapps.com/aero/run/llm-api?pk=v1-Z0FBQUFBQm5IZkJDMlNyYUVUTjIyZVN3UWFNX3BFTU85SWpCM2NUMUk3T2dxejhLSzBhNWNMMXNzZlp3c09BSTR6YW1Sc1BmdGNTVk1GY0liT1RoWDZZX1lNZlZ0Z1dqd3c9PQ==",
            json={"prompt": user_message},
            headers={"Content-Type": "application/json"}
        )
        response_data = response.json()
        if response.ok and response_data.get("status") == "success":
            return response_data.get("text", "I'm not sure I understand. Can you rephrase?")
        else:
            return "There was an error processing your request. Please try again later."
    except requests.RequestException as e:
        print("Error:", e)
        return "There was an error contacting the chatbot API. Please try again later."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["GET", "POST"])
def get_bot_response():
    user_input = request.args.get('msg')
    bot_response = chatbot_response(user_input)
    return jsonify(bot_response)

if __name__ == "__main__":
    app.run(debug=True)
