import logging

from app.model import *
from sqlalchemy import or_


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


def edit_vote(db, id, author, title, text, is_private, is_multiple_choice, start_date, end_date):
    vote = db.query(Vote).filter_by(id=id, author_id=author.id).first()
    if not vote:
        raise ValueError('Vote with id %s not found' % id)

    vote.title = title
    vote.text = text
    vote.is_private = is_private
    vote.is_multiple_choice = is_multiple_choice
    vote.start_date = start_date
    vote.end_date = end_date
    db.commit()
    return vote


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


def publish_vote(db, id, author):
    vote = db.query(Vote).filter_by(id=id, author_id=author.id).first()
    if not vote:
        raise ValueError('Vote with id %s not found' % id)

    if vote.status != VoteStatus.new:
        raise ValueError("Vote with id %s is not new. Can't publish" % id)

    vote.status = VoteStatus.public
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
        return db.query(Vote).filter(Vote.author_id != exclude_user.id,
        or_(Vote.status == VoteStatus.public, Vote.status == VoteStatus.started))

    return db.query(Vote)
