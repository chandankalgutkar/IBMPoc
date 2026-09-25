# src/routes/auth.py
# SCRUM-40: User Login - Backend Route

from flask import Blueprint, request, jsonify, redirect, url_for, session

auth_bp = Blueprint("auth", __name__)

MAX_FAILED_ATTEMPTS = 3

# TODO: Replace with DB-backed user store
failed_attempts = {}  # { username: int }
locked_accounts = set()  # { username }


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    POST /login
    Body: { "username": str, "password": str }
    - Valid credentials  → redirect to /dashboard
    - Invalid credentials → 401 with error message
    - 3 failed attempts  → 423 account locked
    """
    data = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    if username in locked_accounts:
        return jsonify({"error": "Account locked. Contact support."}), 423

    # TODO: Replace with hashed password check against DB
    is_valid = _verify_credentials(username, password)

    if is_valid:
        failed_attempts[username] = 0
        session["user"] = username
        return jsonify({"redirect": url_for("dashboard.index")}), 200
    else:
        failed_attempts[username] = failed_attempts.get(username, 0) + 1
        if failed_attempts[username] >= MAX_FAILED_ATTEMPTS:
            locked_accounts.add(username)
            # TODO: Persist lock status to DB
            return jsonify({"error": "Account locked after 3 failed attempts."}), 423
        remaining = MAX_FAILED_ATTEMPTS - failed_attempts[username]
        return jsonify({
            "error": f"Invalid credentials. {remaining} attempt(s) remaining."
        }), 401


def _verify_credentials(username: str, password: str) -> bool:
    # TODO: Implement DB lookup with bcrypt password verification
    return False