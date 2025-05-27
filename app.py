from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import markdown2

app = Flask(__name__)

genai.configure(api_key="AIzaSyDJfi19P7MGZiyb5pPwXAHkhnLjgjvF7jw")

model = genai.GenerativeModel("gemini-2.0-flash")
chat_session = model.start_chat(history=[
    {
        "role": "user",
        "parts": [
            "You are DnyanVani, a personal AI chatbot developed to assist users. Respond interactively and accurately. If someone asks your name, say 'I am DnyanVani – your personal AI assistant ..!'. Avoid too much short and too much long explanations unless asked."
        ]
    }
])

@app.route("/")
def home():
    return render_template("index.html")



@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    try:
        response = chat_session.send_message(user_message)
        html_reply = markdown2.markdown(response.text.strip())
        return jsonify({"reply": html_reply})
    except Exception as e:
        return jsonify({"reply": "Oops! Something went wrong."}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
