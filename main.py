from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_KEY = "bbc1c9526990e6b41d79a0414ebeed1e"

def get_weather(city):

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()
    if response.get("main"):
        temp = response["main"]["temp"]
        condition = response["weather"][0]["main"].lower()
        return temp, condition
    return None, None

def outfit_suggestion(temp, condition):
    
    if temp is None:
        return "No weather data available."

    if temp > 28:
        suggestion = "T-shirt and shorts 🩳"
    elif temp > 18:
        suggestion = "Light jacket or hoodie 🧥"
    else:
        suggestion = "Warm coat, scarf, maybe gloves 🧣"

    if "rain" in condition:
        suggestion += " + Don’t forget an umbrella ☔"
    elif "snow" in condition:
        suggestion += " + Boots and gloves ❄️"

    return suggestion

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form["city"]
        temp, condition = get_weather(city)
        suggestion = outfit_suggestion(temp, condition)
        return render_template("result.html", city=city, temp=temp, condition=condition, suggestion=suggestion)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
