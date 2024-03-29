import logging
from bottle import route, get, put, delete, response, request, abort
#from sqlalchemy.exc import SQLAlchemyError

#import config
from app import controller
from app.json_helper import json_encode_query, json_encode, get_date


logger = logging.getLogger('srv.'+__name__)


@route('/users')
def user_listing(db):
    logger.info('Listing users...')
    response.content_type = 'application/json'
    return json_encode_query(controller.get_users(db))


@get('/<phone_id>/is_registered')
def register_user(phone_id, db):
    logging.info('Serving is_registered()')
    is_registered = controller.get_user(db, phone_id) is not None
    return json_encode({"is_registered": is_registered})


@put('/<phone_id>/register')
def register_user(phone_id, db):
    """Registers user. If user already created, request will be ignored"""
    logging.info('Serving register_user()')
    if controller.get_user(db, phone_id):
        return

    fullname = request.query.fullname
    email = request.query.email
    if not fullname or not email:
        abort(400, 'User name or email are not specified in request')

    #TODO: check email
    #TODO: check phone_id
    logging.info(u'Creating new user {0:>s}, {1:>s}, {2:>s}'.format(phone_id, fullname, email))
    controller.create_user(db, phone_id, fullname, email)


@route('/<phone_id>/pending')
def pending_votes(phone_id, db):
    """Returns list of pending votes for a user."""
    user = controller.get_user(db, phone_id)
    response.content_type = 'application/json'
    return json_encode_query(controller.get_pending_votes(db, user))


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
    user = controller.get_user(db, phone_id)
    if not user:
        abort(400, 'Invalid or unregistered phone id')

    response.content_type = 'application/json'
    return json_encode_query(controller.get_top_votes(db, user))


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
    start_date = get_date(request.query.start_date)
    end_date = get_date(request.query.end_date)

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
        start_date=start_date,
        end_date=end_date)
    response.content_type = 'application/json'
    return json_encode(vote)


@put('/<phone_id>/my/<id>/publish')
def publish_vote(phone_id, id, db):
    """Publishes vote."""
    user = controller.get_user(db, phone_id)
    try:
        id = int(id)
    except TypeError:
        abort(400, 'Invalid vote id')

    if not user:
        abort(400, 'Invalid or unregistered phone id')

    vote = controller.publish_vote(db, id, user)
    response.content_type = 'application/json'
    return json_encode(vote)

@put('/<phone_id>/my/<id>/invitations')
def set_invitations(phone_id, id, db):
    """Invites users."""
    user = controller.get_user(db, phone_id)
    users = request.query.users
    try:
        id = int(id)
        users = [int(user_id) for user_id in users.split(',') if user_id]
    except ValueError:
        abort(400, 'Invalid vote id or users\' ids')

    if not user:
        abort(400, 'Invalid or unregistered phone id')

    controller.set_invitations(db, id, user, users)


@get('/<phone_id>/votes/<id>/invitations')
@get('/<phone_id>/my/<id>/invitations')
def get_invitations(phone_id, id, db):
    """Returns invitations vote."""
    user = controller.get_user(db, phone_id)
    try:
        id = int(id)
    except ValueError:
        abort(400, 'Invalid vote id')

    if not user:
        abort(400, 'Invalid or unregistered phone id')

    response.content_type = 'application/json'
    return json_encode(controller.get_invitations(db, id))


@put('/<phone_id>/my/<id>/options')
def set_options(phone_id, id, db):
    """Set vote options."""
    user = controller.get_user(db, phone_id)
    options = request.query.options
    options = [op for op in options.split(',') if op]
    try:
        id = int(id)
    except ValueError:
        abort(400, 'Invalid vote id or users\' ids')

    if not user:
        abort(400, 'Invalid or unregistered phone id')

    controller.set_options(db, id, user, options)


@get('/<phone_id>/votes/<id>/options')
@get('/<phone_id>/my/<id>/options')
def get_options(phone_id, id, db):
    """Returns invitations vote."""
    user = controller.get_user(db, phone_id)
    try:
        id = int(id)
    except ValueError:
        abort(400, 'Invalid vote id')

    if not user:
        abort(400, 'Invalid or unregistered phone id')

    response.content_type = 'application/json'
    return json_encode(controller.get_options(db, id))


@get('/<phone_id>/votes/<id>/choices')
@get('/<phone_id>/my/<id>/choices')
def get_choices(phone_id, id, db):
    """Returns choices for vote."""
    user = controller.get_user(db, phone_id)
    try:
        id = int(id)
    except ValueError:
        abort(400, 'Invalid vote id')

    if not user:
        abort(400, 'Invalid or unregistered phone id')

    response.content_type = 'application/json'
    return json_encode(controller.get_choices(db, id))


@get('/<phone_id>/votes/<id>/my_choices')
@get('/<phone_id>/my/<id>/my_choices')
def get_choices(phone_id, id, db):
    """Returns choices for vote."""
    user = controller.get_user(db, phone_id)
    try:
        id = int(id)
    except ValueError:
        abort(400, 'Invalid vote id')

    if not user:
        abort(400, 'Invalid or unregistered phone id')

    response.content_type = 'application/json'
    return json_encode(controller.get_my_choices(db, id, user))


@get('/<phone_id>/votes/<id>/vote')
@put('/<phone_id>/votes/<id>/vote')
def perform_vote(phone_id, id, db):
    """Perform vote."""
    user = controller.get_user(db, phone_id)
    options_ids = request.query.options
    try:
        id = int(id)
        options_ids = [int(option_id) for option_id in options_ids.split(',') if option_id]
    except ValueError:
        abort(400, 'Invalid vote id or users\' ids')

    if not user:
        abort(400, 'Invalid or unregistered phone id')

    controller.perform_vote(db, id, user, options_ids)


@get('/<phone_id>/votes/<id>/result')
@get('/<phone_id>/my/<id>/result')
def get_choices(phone_id, id, db):
    """Returns results for vote."""
    user = controller.get_user(db, phone_id)
    try:
        id = int(id)
    except ValueError:
        abort(400, 'Invalid vote id')

    if not user:
        abort(400, 'Invalid or unregistered phone id')

    response.content_type = 'application/json'
    return json_encode(controller.get_vote_results(db, id))


@put('/<phone_id>/my/<id>')
def edit_vote(phone_id, id, db):
    """Edits vote."""
    user = controller.get_user(db, phone_id)
    try:
        id = int(id)
    except TypeError:
        abort(400, 'Invalid vote id')

    if not user:
        abort(400, 'Invalid or unregistered phone id')

    title = request.query.title
    text = request.query.text
    is_private = request.query.is_private or False
    is_multiple_choice = request.query.is_multiple_choice or False
    start_date = get_date(request.query.start_date)
    end_date = get_date(request.query.end_date)

    #    if not fullname or not email:
    #        abort(400, 'User name or email are not specified in request')
    #
    #TODO: check params
    try:
        id = int(id)
        vote = controller.edit_vote(db=db,
            id=id,
            author=user,
            title=title,
            text=text,
            is_private=is_private,
            is_multiple_choice=is_multiple_choice,
            start_date=start_date,
            end_date=end_date)
    except TypeError:
        abort(400, 'Vote not found')
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
