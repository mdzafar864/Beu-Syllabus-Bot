from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Running"

@app.route('/health')
def health():
    return "OK", 200

@app.route('/status')
def status():
    return {
        "status": "active",
        "message": "Bot is running successfully"
    }

if __name__ == '__main__':
    # Get port from environment variable (Render sets this automatically)
    port = int(os.environ.get('PORT', 5000))
    # Run the app on all available IPs
    app.run(host='0.0.0.0', port=port, debug=False)
