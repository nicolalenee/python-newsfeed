from flask import Blueprint, request, jsonify, session
from app.models import User
from app.db import get_db
import sys

bp = Blueprint('api', __name__, url_prefix='/api')

# create a new user
@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json()
  db = get_db()

  try:
  # try create a new user dictionary
    newUser = User(
      username = data['username'],
      email = data['email'],
      password = data['password']
    )
    # save in database
    db.add(newUser)
    db.commit()
  except:
    print(sys.exc_info()[0])
    # insert failed, so rollback and send error to front end
    db.rollback()
    return jsonify(message = 'Signup failed'), 500
  # clear any existing session data and create new session properties: user_id & boolean for templates
  session.clear()
  session['user_id'] = newUser.id
  session['loggedIn'] = True

  return jsonify(id = newUser.id)

# logout
@bp.route('/users/logout', methods=['POST'])
def logout():
  # remove session variables
  session.clear()
  return '', 204

#login
@bp.route('/users/login', methods=['POST'])
def login():
  # check if email address exists in the database
  data = request.get_json()
  db = get_db()

  try:
    user = db.query(User).filter(User.email == data['email']).one()
  except:
    print(sys.exc_info()[0])

  if user.verify_password(data['password']) == False:
    return jsonify(message = 'Incorrect credentials'), 400
  # create the session and send back a valid response
  session.clear()
  session['user_id'] = user.id
  session['loggedIn'] = True
  return jsonify(id = user.id)