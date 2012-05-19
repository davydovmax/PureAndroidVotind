import logging

from app.model import *


logger = logging.getLogger('srv.'+__name__)


def get_user(db, phone_id):
    return db.query(User).filter_by(phone_id=phone_id).first()


def get_users(db):
    return db.query(User)


def create_user(db, phone_id, fullname, email):
    user = User(phone_id=phone_id, fullname=fullname, email=email)
    db.add(user)
    db.commit()
    return user


def create_vote(db, author, title, text, is_private, is_multiple_choice, start_date, end_date):
    vote = Vote(author_id=author.id,
        title=title,
        text=text,
        is_private=is_private,
        is_multiple_choice=is_multiple_choice,
        start_date=start_date,
        end_date=end_date)
    db.add(vote)
    db.commit()
    return vote


def create_vote_options(db, vote, options):
    result = []
    for text in options:
        option = VoteOption(vote_id=vote.id, text=text)
        db.add(option)
        result.append(option)
    db.commit()
    return result


def get_top_votes(db, exclude_user=None):
    if exclude_user:
        return db.query(Vote).filter(Vote.author_id != exclude_user.id)

    return db.query(Vote)
