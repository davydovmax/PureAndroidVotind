import logging
from datetime import datetime, timedelta
from bottle import route, get, put, delete, response, abort, request, template
from sqlalchemy.exc import SQLAlchemyError
from app import controller

import config
from app.model import User, Vote, VoteOption
from app.json_helper import json_encode_query


logger = logging.getLogger('srv.'+__name__)


@get('/logs')
def logs(db):
    logger.info('Serving logs()')
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s %(name)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logs = [formatter.format(record) for record in config.env.history.records]

    if 'json' not in request.query:
        return template('logs.tpl', rows=logs)

    response.content_type = 'application/json'
    return json_encode_query(logs)


def fill_test_data(db, current_user=None):
    logger.info('Creating test data')
    # TODO: delete test data
    logger.debug('Cleaning db')
    # raise Exception('spam', 'eggs')
    session = config.env.create_session()
    try:
        if current_user:
            session.query(User).filter(User.id != current_user.id).delete()
        else:
            session.query(User).delete()
        session.query(Vote).delete()
        session.query(VoteOption).delete()
        session.commit()
    except SQLAlchemyError, e:
        session.rollback()
        raise
    finally:
        session.close()

    # create users
    logger.debug('Creating users')
    user1 = controller.create_user(db, 'test_id_1', 'Barak Obama', 'obama@google.com')
    user2 = controller.create_user(db, 'test_id_2', 'John Smith', 'smith@google.com')
    user3 = controller.create_user(db, 'test_id_3', 'Ivan Petrov', 'petrov@google.com')
    db.commit()

    # create vote and options
    logger.debug('Creating vote and options')
    vote1 = controller.create_vote(db=db,
        author=user1,
        title='USA President Election',
        text='Choose new USA president',
        is_private=False,
        is_multiple_choice=False,
        start_date=datetime.now() - timedelta(hours=2),
        end_date=datetime.now() + timedelta(hours=10))
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
    controller.publish_vote(db, vote1.id, user1)

    if current_user:
        # create vote for a user
        logger.debug('Creating user vote')
        vote_2 = controller.create_vote(db=db,
            author=current_user,
            title='Color You Like',
            text='Choose any color that suits you best at the moment. FYI, my favorite color is red.',
            is_private=False,
            is_multiple_choice=False,
            start_date=datetime.now() - timedelta(hours=2),
            end_date=datetime.now() + timedelta(hours=10))
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

        #invite someone
        controller.set_invitations(db=db,
            id=vote_2.id,
            author=current_user,
            user_ids=[user1.id, user2.id, user3.id]
        )

        # create vote and options
        logger.debug('Creating vote and options')
        vote10 = controller.create_vote(db=db,
            author=user2,
            title='Favorite day of Week',
            text='The day you like most of all',
            is_private=False,
            is_multiple_choice=True,
            start_date=datetime.now() - timedelta(hours=2),
            end_date=datetime.now() + timedelta(hours=10))
        db.commit()

        controller.create_vote_options(db=db,
            vote=vote10,
            options=['Monday',
                     'Tuesday',
                     'Wednesday',
                     'Thursday',
                     'Friday',
                     'Saturday',
                     'Sunday'])
        db.commit()
        controller.publish_vote(db, vote10.id, user2)

        # create vote and options
        logger.debug('Creating vote and options')
        vote12 = controller.create_vote(db=db,
            author=user2,
            title='Present for Walter',
            text='Happy Birthday soon, we should think ahead, chaps!',
            is_private=True,
            is_multiple_choice=True,
            start_date=datetime.now() - timedelta(hours=2),
            end_date=datetime.now() + timedelta(hours=10))
        db.commit()

        controller.create_vote_options(db=db,
            vote=vote12,
            options=['Finger Bike',
                     'Book',
                     'Vintage Photo Camera',
                     'Subscription for man\'s magazines',
                     'Nothing!',
                     'Ask Natasha...'])
        db.commit()
        #invite someone
        controller.set_invitations(db=db,
            id=vote12.id,
            author=user2,
            user_ids=[user1.id, user2.id, current_user.id]
        )
        controller.publish_vote(db, vote12.id, user2)


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