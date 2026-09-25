# src/routes/email_intake.py
# SCRUM-50: Flask routes for email ingestion and review queue

from flask import Blueprint, request, jsonify
from src.services.email_extractor import EmailExtractor, review_queue

email_bp = Blueprint("email", __name__, url_prefix="/api/email")
extractor = EmailExtractor()


@email_bp.route("/ingest", methods=["POST"])
def ingest_email():
    """POST /api/email/ingest — receive raw email and trigger extraction."""
    raw_email = request.get_json()
    if not raw_email:
        return jsonify({"error": "No email payload provided"}), 400

    parsed = extractor.parse_email(raw_email)
    if not parsed:
        return jsonify({"error": "Parsing failed, flagged for review"}), 422

    fields = extractor.extract_fields(parsed)
    if not fields:
        return jsonify({"error": "Extraction failed, flagged for review"}), 422

    is_valid = extractor.validate_fields(fields)
    if not is_valid:
        return jsonify({"error": "Validation failed, flagged for review"}), 422

    # TODO: persist validated fields to the database (e.g. SQLAlchemy)
    return jsonify({"message": "Email processed successfully",
                    "fields": fields}), 200


@email_bp.route("/review", methods=["GET"])
def review_failures():
    """GET /api/email/review — list all flagged failures for human review."""
    # TODO: replace in-memory queue with persistent DB query
    return jsonify({
        "flagged_count": len(review_queue),
        "items": review_queue
    }), 200