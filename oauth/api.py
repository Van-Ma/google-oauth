from flask import Flask, redirect, url_for, session, jsonify, make_response
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os, secrets

load_dotenv()

# flask setup
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
CORS(app, supports_credentials=True)

# oauth setup
oauth = OAuth(app)
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

#----- routes
@app.route("/login/google")
def login_google():
    google = oauth.create_client("google")
    nonce = secrets.token_urlsafe(16)
    session["nonce"] = nonce
    redirect_uri = url_for("authorize_google", _external=True)
    return google.authorize_redirect(redirect_uri, nonce=nonce)

#----- authorize account
@app.route("/authorize/google")
def authorize_google():
    google = oauth.create_client("google")
    token = google.authorize_access_token()
    nonce = session.pop("nonce", None)
    user_info = google.parse_id_token(token, nonce=nonce)

    # store in session
    session["user"] = {
        "google_id": user_info["sub"],
        "name": user_info.get("name"),
        "email": user_info.get("email"),
    }

    # redirect to frontend
    resp = make_response(redirect("http://localhost:3000"))
    return resp

# get user info
@app.route("/api/user", methods=["GET"])
def get_user():
    # check login state
    user = session.get("user")
    if not user:
        return jsonify({"error": "Not authenticated"}), 401
    return jsonify(user)

# logout
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})



if __name__ == '__main__':
    app.run(debug=True, port=5000)
