from flask import Blueprint, request, jsonify, make_response
from db_logic import get_db_connection, dislike_promo_code
import uuid

dislike_blueprint = Blueprint('dislike_blueprint', __name__)  # Define the Blueprint

@dislike_blueprint.route('/dislike', methods=['POST'])
def dislike():
    # Check if the user has a unique identifier in cookies
    user_id = request.cookies.get('user_id')
    if not user_id:
        # Generate a new unique identifier if not present
        user_id = str(uuid.uuid4())

    promocode_id = request.json.get('promocode_id')
    if not promocode_id:
        return jsonify({'status': 'error', 'message': 'Promo code ID is missing'}), 400

    db = get_db_connection()
    dislike_promo_code(db, user_id, promocode_id)
    
    # Fetch updated counts
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT likes, dislikes FROM PromoCodes WHERE id = %s", (promocode_id,)
    )
    counts = cursor.fetchone()
    cursor.close()
    db.close()

    # Set the user_id cookie if it wasn't already set
    response = jsonify({
        'status': 'success',
        'message': 'Promo code disliked!',
        'likes': counts['likes'],
        'dislikes': counts['dislikes']
    })
    response.set_cookie('user_id', user_id, max_age=60*60*24*365)  # Set cookie for 1 year
    return response
