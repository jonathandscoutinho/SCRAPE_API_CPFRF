from flask import Flask, request, jsonify
from scraper.cpfrfconsult import scraping

app = Flask(__name__)

@app.route("/cpfrfconsult", methods=["POST"])
def consult():
    data = request.get_json()
    cpf = data.get("cpf")
    birth_date = data.get("birthdate")

    result = scraping(cpf, birth_date)
    if isinstance(result, dict):    
        return jsonify(result)
    else:
        return jsonify({"error": result}), 400

if __name__ == "__main__":
    app.run(debug=True)
