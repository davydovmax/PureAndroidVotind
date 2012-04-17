from datetime import datetime
from bottle import route, get, put, delete, response, request, abort
#from sqlalchemy.exc import SQLAlchemyError

#import config
from model import User, Vote, VoteOption
import controller
from json_helper import json_encode_query, json_encode, get_date


@route('/')
def listing(db):
    users = db.query(User)
    response.content_type = 'application/json'
    return json_encode_query(users)


@put('/fill_test_data')
def fill_test_data(db):
    # TODO: delete test data
    db.query(User).delete()
    db.query(Vote).delete()
    db.query(VoteOption).delete()

    # create users
    user1 = controller.create_user(db, 'test_id_1', 'Barak Obama', 'obama@google.com')
    controller.create_user(db, 'test_id_2', 'John Smith', 'smith@google.com')
    controller.create_user(db, 'test_id_3', 'Ivan Petrov', 'petrov@google.com')
    db.commit()

    # create vote
    vote1 = controller.create_vote(db=db,
        author=user1,
        title='USA President Election',
        text='Choose new USA president',
        is_private=False,
        is_multiple_choice=False,
        publication_date=datetime.now(),
        start_date=datetime.now(),
        end_date=datetime.now(),
        results_date=datetime.now())
    db.commit()

    # create vote options
    controller.create_vote_options(db=db,
        vote=vote1,
        options=['Theodore Roosevelt',
                 'John F. Kennedy',
                 'William Howard Taft',
                 'Lyndon B. Johnson',
                 'Woodrow Wilson',
                 'Richard M. Nixon',
                 'Warren G. Harding',
                 'Gerald R. Ford',
                 'Calvin Coolidge',
                 'James Carter',
                 'Herbert Hoover',
                 'Ronald Reagan',
                 'Franklin D. Roosevelt',
                 'George H. W. Bush',
                 'Harry S. Truman',
                 'William J. Clinton',
                 'Dwight D. Eisenhower'])
    db.commit()


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


@get('/<phone_id>/top')
def top_votes(phone_id, db):
    """Returns list of top opened votes for a user."""
    return None


@put('/<phone_id>/my')
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
        author=user,
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
