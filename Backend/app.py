from flask import Flask, request, jsonify
from flask_cors import CORS
from agent import search_tasks

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():

    data = request.json

    user_message = data.get("message")

    result = search_tasks(user_message)

    return jsonify({
        "results": result["results"],
        "summary": result["summary"]
    })

if __name__ == '__main__':
    app.run(debug=True)