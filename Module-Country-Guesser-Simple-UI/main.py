from flask import Flask, render_template, request, jsonify, send_from_directory, session
import json
import random
from fuzzywuzzy import fuzz
import os
import secrets

app = Flask(__name__)

app.secret_key = 'default_secret_key'  
def generate_secret_key():
    return secrets.token_hex(16)
@app.before_request
def ensure_secret_key():
    if 'secret_key' not in session:
        session['secret_key'] = generate_secret_key()
        app.secret_key = session['secret_key']  

# Data and Image Paths
data_folder = "[Backup]_generated_data"
image_folder = os.path.join(data_folder, "images")
country_data_file = os.path.join(data_folder, "country.json")

def load_country_data():
    # Loads the country data from the JSON file.
    with open(country_data_file, "r") as f:
        countries = json.load(f)
    return countries

def choose_random_country(countries):
    # Chooses a random country entry from the provided list.
    return random.choice(countries)

def check_guess(user_guess, correct_country):
    # Matches the correct country using some fuzzy matching just incase the user enters a small typo.
    return fuzz.ratio(user_guess.lower(), correct_country["name"].lower()) >= 90 

@app.route("/")
def guess_the_country():
    # Renders the main template
    countries = load_country_data()
    selected_country = choose_random_country(countries)
    session['selected_country'] = selected_country
    image_filename = selected_country["filename"]
    return render_template("index.html", image_path=image_filename)

@app.route("/get_country_image")
def get_country_image():
    # Sends the image path of the currently selected country in JSON format.
    countries = load_country_data()
    selected_country = choose_random_country(countries)
    # Update session with the new country
    session['selected_country'] = selected_country
    image_filename = selected_country["filename"]
    return jsonify({'image_path': image_filename})
@app.route("/images/<path:filename>")
def serve_image(filename):
    return send_from_directory(image_folder, filename)

@app.route("/check_guess", methods=["POST"])
def handle_guess():
    """Handles user's guess submission and returns a JSON response."""
    selected_country = session.get('selected_country')
    attempts = session.get('attempts', 0)

    if not selected_country:
        return jsonify({'error': 'No country selected'}), 400

    user_guess = request.form["guess"]
    attempts += 1
    session['attempts'] = attempts

    if check_guess(user_guess, selected_country):
        result = {"message": "Congratulations! You guessed it correctly.", "success": True}
        session.pop('attempts', None)  # Clear attempts on correct guess
    elif attempts >= 3:
        result = {
            "message": f"Sorry, that's not quite right. The correct country is {selected_country['name']}.",
            "success": False
        }
        session.pop('attempts', None)  # Clear attempts after the third try
    else:
        result = {
            "message": "Sorry, Thats Wrong. Giving you one more guess. ",
            "success": False
        }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
