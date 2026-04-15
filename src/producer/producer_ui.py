from flask import Flask, render_template, request, jsonify
from producer import publish_message

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("producer_ui.html")


@app.route("/publish", methods=["POST"])
def publish():
    data = request.get_json()
    content = data.get("message", "").strip()
    severity = data.get("severity", "").strip()

    if not content:
        return jsonify({"error": "Message cannot be empty"}), 400

    if not severity:
        return jsonify({"error:" "Severity cannot be empty"}), 400

    try:
        message_id = publish_message(content, severity)
        return jsonify({"status": "ok", "message_id": message_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)