import logging
from datetime import datetime
from bottle import route, get, put, delete, response, request, abort

import config
from model import User, Vote, VoteOption
import controller
from json_helper import json_encode_query, json_encode, get_date


logger = logging.getLogger('srv.'+__name__)


@route('/')
def user_listing(db):
    logger.info('Listing users...')
    users = db.query(User)
    response.content_type = 'application/json'
    return json_encode_query(users)


@get('/logs')
def logs(db):
    logger.info('Serving logs()')
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s %(name)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logs = [formatter.format(record) for record in config.env.history.records]
    response.content_type = 'application/json'
    return json_encode_query(logs)


def fill_test_data(db, current_user=None):
    logger.info('Creating test data')
    # TODO: delete test data
    logger.debug('Cleaning db')
    if current_user:
        db.query(User).filter(User.id != current_user.id).delete()
    else:
        db.query(User).delete()
    db.query(Vote).delete()
    db.query(VoteOption).delete()
    db.commit()

    # create users
    logger.debug('Creating users')
    user1 = controller.create_user(db, 'test_id_1', 'Barak Obama', 'obama@google.com')
    controller.create_user(db, 'test_id_2', 'John Smith', 'smith@google.com')
    controller.create_user(db, 'test_id_3', 'Ivan Petrov', 'petrov@google.com')
    db.commit()

    # create vote and options
    logger.debug('Creating vote and options')
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

    if current_user:
        # create vote for a user
        logger.debug('Creating user vote')
        vote_2 = controller.create_vote(db=db,
            author=current_user,
            title='Color You Like',
            text='Choose any color that suits you best at the moment. FYI, my favorite color is red.',
            is_private=False,
            is_multiple_choice=False,
            publication_date=datetime.now(),
            start_date=datetime.now(),
            end_date=datetime.now(),
            results_date=datetime.now())
        db.commit()

        # create vote options
        controller.create_vote_options(db=db,
            vote=vote_2,
            options=['White',
                     'Pink',
                     'Red',
                     'Orange',
                     'Brown',
                     'Yellow',
                     'Gray',
                     'Green',
                     'Cyan',
                     'Blue',
                     'Violet'])
        db.commit()


@put('/<phone_id>/fill_test_data')
def fill_test_data_user(db, phone_id):
    logger.info('Serving fill_test_data_user()')
    user = controller.get_user(db, phone_id)
    if not user:
        abort(400, 'Invalid or unregistered phone id')
    fill_test_data(db, user)


@put('/fill_test_data')
def fill_test_data_general(db):
    logger.info('Serving fill_test_data()')
    fill_test_data(db)