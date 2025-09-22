from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Simple in-memory session storage (for demo only; use DB in production)
user_sessions = {}

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").strip().lower()
    sender = request.values.get("From")
    resp = MessagingResponse()
    msg = resp.message()

    # Start new conversation if user not in session
    if sender not in user_sessions:
        user_sessions[sender] = {"step": 1}
        msg.body(
            "👋 Hello! Welcome to *Thryvix AI – Intelligence. Orchestrated.*\n\n"
            "We design *custom AI solutions* that adapt to your business.\n\n"
            "💡 To get started, may I know what type of business you run?"
        )
        return str(resp)

    # Step 1: Ask about business
    if user_sessions[sender]["step"] == 1:
        user_sessions[sender]["business"] = incoming_msg
        user_sessions[sender]["step"] = 2
        msg.body(
            "Great! Thanks for sharing. 😊\n\n"
            "Now tell me — what’s the *biggest challenge* your business faces right now?"
        )
        return str(resp)

    # Step 2: Ask about challenge
    if user_sessions[sender]["step"] == 2:
        user_sessions[sender]["challenge"] = incoming_msg
        user_sessions[sender]["step"] = 3

        business = user_sessions[sender]["business"]
        challenge = user_sessions[sender]["challenge"]

        msg.body(
            f"Got it 👍 So you run a *{business}* business, and your main challenge is *{challenge}*.\n\n"
            "Here’s how *Thryvix AI* can help:\n"
            "✅ Automating repetitive tasks\n"
            "✅ Improving customer engagement\n"
            "✅ Boosting efficiency & sales\n\n"
            "We don’t do one-size-fits-all — everything is *custom-tailored* for your business needs."
        )
        msg.body(
            "🚀 Would you like to:\n"
            "1️⃣ Book a free consultation\n"
            "2️⃣ See case studies of how we’ve helped others"
        )
        return str(resp)

    # Step 3: Call-to-action
    if user_sessions[sender]["step"] == 3:
        if "1" in incoming_msg:
            user_sessions[sender]["step"] = 4
            msg.body(
                "Awesome! 🎉 Our team will reach out to schedule your free consultation.\n\n"
                "Can you please share your *email* or *preferred contact*?"
            )
        elif "2" in incoming_msg:
            user_sessions[sender]["step"] = 4
            msg.body(
                "Sure! 📖 Here are some highlights:\n"
                "- Helped a retail business boost sales by 35%\n"
                "- Saved 20+ hours/week for a healthcare clinic\n"
                "- Automated lead engagement for a logistics firm\n\n"
                "👉 Want us to explore what’s possible for your business? (Reply YES to proceed 🚀)"
            )
        else:
            msg.body("Please reply with *1* or *2* so we can guide you best. 🙂")
        return str(resp)

    # Step 4: Capture final info
    if user_sessions[sender]["step"] == 4:
        msg.body(
            "✅ Thank you! Your details have been noted.\n\n"
            "Our team will connect with you shortly.\n\n"
            "Meanwhile, feel free to reply *MENU* if you'd like to restart the conversation."
        )
        user_sessions[sender]["step"] = 5
        return str(resp)

    # Restart conversation if user types MENU
    if "menu" in incoming_msg:
        del user_sessions[sender]
        msg.body("🔄 Restarting the conversation...\n\nPlease say hi to begin again. 👋")
        return str(resp)

    return str(resp)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
