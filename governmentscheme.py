from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# 🌐 Frontend (HTML + JS)
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Government Schemes</title>
    <style>
        body {
            font-family: Arial;
            background: #0f172a;
            color: white;
            text-align: center;
            padding: 40px;
        }
        select {
            padding: 10px;
            margin: 10px;
            border-radius: 5px;
            border: none;
            width: 250px;
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
            text-align: left;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        h3 { color: #22c55e; }
        a {
            color: #38bdf8;
            text-decoration: none;
        }
    </style>
</head>
<body>

    <h1>🏛️ Government Schemes</h1>

    <select id="category">
        <option value="All">All</option>
        <option value="Income Support">Income Support</option>
        <option value="Insurance">Insurance</option>
        <option value="Loan">Loan</option>
        <option value="Subsidy">Subsidy</option>
        <option value="Irrigation">Irrigation</option>
        <option value="Soil">Soil</option>
        <option value="Organic">Organic</option>
        <option value="Fisheries">Fisheries</option>
    </select>

    <button onclick="getSchemes()">Show Schemes</button>

    <div id="result"></div>

    <script>
        function getSchemes() {
            const category = document.getElementById("category").value;

            document.getElementById("result").innerHTML = "Loading...";

            fetch("/schemes", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ category: category })
            })
            .then(res => res.json())
            .then(data => {
                if (data.length === 0) {
                    document.getElementById("result").innerHTML = "No schemes found";
                    return;
                }

                let html = "";
                data.forEach(s => {
                    html += `
                        <div class="card">
                            <h3>${s.name}</h3>
                            <p><strong>📂 Category:</strong> ${s.category}</p>
                            <p><strong>📝 Description:</strong> ${s.description}</p>
                            <p><strong>✅ Eligibility:</strong> ${s.eligibility}</p>
                            <p><strong>🔗 Apply:</strong> <a href="${s.apply_link}" target="_blank">Apply Here</a></p>
                            <p><strong>📞 Helpline:</strong> ${s.helpline}</p>
                        </div>
                    `;
                });

                document.getElementById("result").innerHTML = html;
            })
            .catch(() => {
                document.getElementById("result").innerHTML = "Error";
            });
        }
    </script>

</body>
</html>
"""

# 🏠 Home
@app.route("/")
def home():
    return render_template_string(HTML)

# 🏛️ Schemes Data (from your original code)
GOVERNMENT_SCHEMES = [
    {
        "category": "Income Support",
        "name": "PM-KISAN",
        "description": "Rs 6000 per year to farmers",
        "eligibility": "All landholding farmers",
        "apply_link": "https://pmkisan.gov.in/",
        "helpline": "155261"
    },
    {
        "category": "Insurance",
        "name": "PM Fasal Bima Yojana",
        "description": "Crop insurance scheme",
        "eligibility": "All farmers",
        "apply_link": "https://pmfby.gov.in/",
        "helpline": "18002007710"
    },
    {
        "category": "Loan",
        "name": "Kisan Credit Card",
        "description": "Short-term credit for farmers",
        "eligibility": "Farmers and SHGs",
        "apply_link": "https://www.nabard.org/",
        "helpline": "18002000027"
    },
    {
        "category": "Subsidy",
        "name": "PM Krishi Sinchayee Yojana",
        "description": "Irrigation subsidy scheme",
        "eligibility": "All farmers",
        "apply_link": "https://pmksy.gov.in/",
        "helpline": "18001801551"
    },
    {
        "category": "Soil",
        "name": "Soil Health Card",
        "description": "Soil testing and recommendations",
        "eligibility": "All farmers",
        "apply_link": "https://soilhealth.dac.gov.in/",
        "helpline": "18001801551"
    }
]

# 🏛️ API
@app.route("/schemes", methods=["POST"])
def schemes():
    data = request.json
    category = data.get("category")

    if category == "All":
        return jsonify(GOVERNMENT_SCHEMES)

    filtered = [s for s in GOVERNMENT_SCHEMES if s["category"] == category]
    return jsonify(filtered)

# ▶ Run
if __name__ == "__main__":
    app.run(debug=True)