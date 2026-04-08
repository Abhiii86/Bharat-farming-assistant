from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# 🔑 Put your OpenWeather API Key here
OPENWEATHER_API_KEY = "your_api_key_here"

# 🌐 HTML + JS (Frontend)
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Weather Intelligence</title>
    <style>
        body {
            font-family: Arial;
            background: #0f172a;
            color: white;
            text-align: center;
            padding: 50px;
        }
        input {
            padding: 10px;
            width: 200px;
            border-radius: 5px;
            border: none;
        }
        button {
            padding: 10px 15px;
            background: #22c55e;
            border: none;
            border-radius: 5px;
            color: white;
            cursor: pointer;
        }
        .card {
            margin-top: 20px;
            padding: 20px;
            background: #1e293b;
            border-radius: 10px;
            display: inline-block;
        }
    </style>
</head>
<body>

    <h1>🌦️ Weather Intelligence</h1>

    <input type="text" id="city" placeholder="Enter city">
    <button onclick="getWeather()">Get Weather</button>

    <div id="result"></div>

    <script>
        function getWeather() {
            const city = document.getElementById("city").value;

            if (!city) {
                alert("Enter city name");
                return;
            }

            document.getElementById("result").innerHTML = "Loading...";

            fetch("/weather", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ city: city })
            })
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    document.getElementById("result").innerHTML = data.error;
                    return;
                }

                document.getElementById("result").innerHTML = `
                    <div class="card">
                        <h2>${data.city}</h2>
                        <p>🌡 Temperature: ${data.temperature} °C</p>
                        <p>💧 Humidity: ${data.humidity}%</p>
                        <p>🌬 Wind Speed: ${data.wind_speed} m/s</p>
                        <p>☁ Condition: ${data.description}</p>
                    </div>
                `;
            })
            .catch(() => {
                document.getElementById("result").innerHTML = "Error fetching weather";
            });
        }
    </script>

</body>
</html>
"""

# 🏠 Home route
@app.route("/")
def home():
    return render_template_string(HTML)

# 🌦️ Weather API route
@app.route("/weather", methods=["POST"])
def weather():
    data = request.json
    city = data.get("city")

    if not city:
        return jsonify({"error": "City is required"})

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"

    response = requests.get(url)
    weather_data = response.json()

    if weather_data.get("cod") != 200:
        return jsonify({"error": "City not found"})

    result = {
        "city": city,
        "temperature": weather_data["main"]["temp"],
        "humidity": weather_data["main"]["humidity"],
        "wind_speed": weather_data["wind"]["speed"],
        "description": weather_data["weather"][0]["description"]
    }

    return jsonify(result)

# ▶ Run app
if __name__ == "__main__":
    app.run(debug=True)