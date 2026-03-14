"""
Yukti AI — Government Services Automation Platform
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from agents.orchestrator import AgentOrchestrator
import os
import traceback

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'

orchestrator = AgentOrchestrator()

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('forms/filled', exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/process', methods=['POST'])
def process_request():
    try:
        data = request.get_json(force=True)
        user_request = data.get('request', '').strip()
        if not user_request:
            return jsonify({"error": "No request provided"}), 400
        uploaded_data = data.get('uploaded_data', {})
        result = orchestrator.run(user_request, uploaded_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500


@app.route('/api/services', methods=['GET'])
def list_services():
    services = [
        {"id": "aadhaar",           "name": "Aadhaar Enrolment / Update",  "emoji": "🔵", "time": "~10 min", "desc": "Update name, address, DOB or biometrics",        "auth": "UIDAI"},
        {"id": "pan",               "name": "PAN Card (Form 49A)",          "emoji": "💳", "time": "~12 min", "desc": "Apply for new PAN or correction in existing PAN", "auth": "Income Tax Department"},
        {"id": "voter_id",          "name": "Voter ID (Form-6)",            "emoji": "🗳", "time": "~8 min",  "desc": "New voter registration — Election Commission",    "auth": "Election Commission of India"},
        {"id": "birth_certificate", "name": "Birth Certificate",            "emoji": "👶", "time": "~7 min",  "desc": "Issue birth certificate from municipality",       "auth": "Registrar of Births & Deaths"},
        {"id": "death_certificate", "name": "Death Certificate",            "emoji": "📜", "time": "~7 min",  "desc": "Issue death certificate from municipality",       "auth": "Registrar of Births & Deaths"},
        {"id": "ration_card",       "name": "Ration Card (NFSA)",           "emoji": "🛒", "time": "~15 min", "desc": "National Food Security Act consumer card",        "auth": "Dept. of Food & Supplies"},
        {"id": "passport",          "name": "Passport Renewal",             "emoji": "📗", "time": "~20 min", "desc": "Renewal or fresh application for Indian passport", "auth": "Ministry of External Affairs"},
        {"id": "driving_license",   "name": "Driving License Renewal",      "emoji": "🚗", "time": "~15 min", "desc": "Renewal of expired or expiring driving license",  "auth": "Regional Transport Office"},
    ]
    return jsonify(services)


@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json(force=True)
        messages = data.get('messages', [])
        service_context = data.get('service_context', '')
        if not messages:
            return jsonify({"error": "No messages"}), 400

        system_prompt = (
            "You are Yukti, a helpful AI assistant for Indian government services. "
            "Help citizens with forms, documents, eligibility, fees and timelines. "
            "Be concise and friendly. Services: Aadhaar, PAN, Voter ID, Passport, "
            "Birth/Death certificates, Ration card, Driving license."
        )
        if service_context:
            system_prompt += f" User is working on: {service_context}."

        try:
            from groq import Groq
            client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))
            resp = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "system", "content": system_prompt}] + messages,
                max_tokens=512, temperature=0.7
            )
            reply = resp.choices[0].message.content.strip()
        except Exception:
            last = messages[-1].get("content", "").lower() if messages else ""
            reply = _fallback(last, service_context)

        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def _fallback(msg, ctx):
    if any(w in msg for w in ["hello","hi","hey","namaste"]):
        return "Namaste! 🙏 I'm Yukti, your government services assistant. Ask me about Aadhaar, PAN, Voter ID, Passport or any other service."
    if "aadhaar" in msg or "aadhar" in msg:
        return "For Aadhaar you need: Proof of Identity (Passport/Voter ID/PAN), Proof of Address (utility bill < 3 months), and Date of Birth proof. Visit myaadhaar.uidai.gov.in."
    if "pan" in msg:
        return "For PAN Card (Form 49A) you need: Aadhaar, address proof, DOB proof. Apply at tin.tin.nsdl.com. Fee: ₹107. Takes 15–20 working days."
    if "voter" in msg:
        return "For Voter ID (Form-6) you need age proof and address proof. Apply at voters.eci.gov.in. Must be 18+. Takes ~30 days."
    if "passport" in msg:
        return "For Passport renewal: bring current passport + Aadhaar + address proof to a Passport Seva Kendra. Book at passportindia.gov.in."
    if "fee" in msg or "cost" in msg:
        return "Fees: Aadhaar — Free | PAN Card — ₹107 | Voter ID — Free | Passport — ₹1,500 | DL Renewal — ₹200–400."
    if "time" in msg or "long" in msg or "days" in msg:
        return "Processing: Aadhaar — 90 days | PAN — 15–20 days | Voter ID — 30 days | Passport — 30–45 days | Birth/Death cert — 7–15 days."
    if "document" in msg:
        return "Common documents needed: ✅ Aadhaar Card ✅ PAN Card ✅ Voter ID ✅ Passport ✅ Utility bill (< 3 months) ✅ Bank passbook."
    return "I can help with Aadhaar, PAN Card, Voter ID, Passport, Birth/Death Certificates, Ration Card, and Driving License. What do you need?"


@app.route('/forms/<path:filename>')
def download_form(filename):
    return send_from_directory('forms', filename)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
