from bottle import route, get, put, delete, response, request, abort
#from sqlalchemy.exc import SQLAlchemyError

#import config
from model import User, Vote
import controller
from json_helper import json_encode_query, json_encode, get_date


@route('/')
def listing(db):
    users = db.query(User)
    response.content_type = 'application/json'
    return json_encode_query(users)


@put('/register/<phone_id>')
def register_user(phone_id, db):
    """Registers user. If user already created, request will be ignored"""
    if controller.get_user(db, phone_id):
        return

    fullname = request.query.fullname
    email = request.query.email
    if not fullname or not email:
        abort(400, 'User name or email are not specified in request')

    #TODO: check email
    #TODO: check phone_id
    controller.create_user(db, phone_id, fullname, email)


@route('/:phone_id/pending')
def pending_votes(phone_id, db):
    """Returns list of pending votes for a user."""
    user = controller.get_user(db, phone_id)
    response.content_type = 'application/json'
    return json_encode_query(user)


@get('/<phone_id>/my')
def my_votes(phone_id, db):
    """Returns list of pending votes for a user."""
    user = controller.get_user(db, phone_id)
    if not user:
        abort(400, 'Invalid or unregistered phone id')

    response.content_type = 'application/json'
    return json_encode_query(user.votes)


@get('/:phone_id/top')
def top_votes(phone_id, db):
    """Returns list of top opened votes for a user."""
    return None


@put('/:phone_id/my')
def create_vote(phone_id, db):
    """Creates vote."""
    user = controller.get_user(db, phone_id)
    if not user:
        abort(400, 'Invalid or unregistered phone id')

    title = request.query.title
    text = request.query.text
    is_private = request.query.is_private or False
    is_multiple_choice = request.query.is_multiple_choice or False
    publication_date = get_date(request.query.publication_date)
    start_date = get_date(request.query.start_date)
    end_date = get_date(request.query.end_date)
    results_date = get_date(request.query.results_date)

#    if not fullname or not email:
#        abort(400, 'User name or email are not specified in request')
#
    #TODO: params
    vote = controller.create_vote(db=db,
        author_id=user.id,
        title=title,
        text=text,
        is_private=is_private,
        is_multiple_choice=is_multiple_choice,
        publication_date=publication_date,
        start_date=start_date,
        end_date=end_date,
        results_date=results_date)
    response.content_type = 'application/json'
    return json_encode(vote)


#@delete('/:name')
#def delete_name(name):
#    session = config.create_session()
#    try:
#        user = session.query(User).filter_by(name=name).first()
#        session.delete(user)
#        session.commit()
#    except SQLAlchemyError, e:
#        session.rollback()
#        raise bottle.HTTPError(500, "Database Error", e)
#    finally:
#        session.close()
