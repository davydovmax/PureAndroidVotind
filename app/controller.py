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


def set_invitations(db, id, author, user_ids):
    vote = db.query(Vote).filter_by(id=id, author_id=author.id).first()
    if not vote:
        raise ValueError('Vote with id %s not found' % id)

    # remove old
    logger.info('Removing old invitations')
    vote.invitations[:] = []
    db.commit()

    #add new
    for user_id in user_ids:
        logger.info('Creating invitation for user %s' % user_id)
        invitation = VoteInvitation(vote_id=vote.id, user_id=user_id, is_accepted=True, is_considered=True)
        db.add(invitation)
    db.commit()


def get_invitations(db, id):
    vote = db.query(Vote).filter_by(id=id).first()
    if not vote:
        raise ValueError('Vote with id %s not found' % id)

    return vote.invitations


def create_vote_options(db, vote, options):
    result = []
    for text in options:
        option = VoteOption(vote_id=vote.id, text=text)
        db.add(option)
        result.append(option)
    db.commit()
    return result


def set_vote_options(db, id, author, options):
    vote = db.query(Vote).filter_by(id=id, author_id=author.id).first()
    if not vote:
        raise ValueError('Vote with id %s not found' % id)

    # remove old
    logger.info('Removing old invitations')
    vote.options[:] = []
    db.commit()

    for text in options:
        option = VoteOption(vote_id=vote.id, text=text)
        db.add(option)
        db.commit()


def get_options(db, vote_id):
    vote = db.query(Vote).filter_by(id=vote_id).first()
    if not vote:
        raise ValueError('Vote with id %s not found' % vote_id)

    return vote.options


def get_top_votes(db, exclude_user=None):
    if exclude_user:
        return db.query(Vote).filter(Vote.author_id != exclude_user.id,
            Vote.is_private == False,
            or_(Vote.status == VoteStatus.public, Vote.status == VoteStatus.started))

    return db.query(Vote)


def perform_vote(db, id, user, option_ids):
    vote = db.query(Vote).filter_by(id=id).first()
    if not vote:
        raise ValueError('Vote with id %s not found' % id)

    # remove old
    logger.info('Removing old choices')
    to_delete = []
    for vote_choice in vote.choices:
        if vote_choice.user_id == user.id:
            to_delete.append(vote_choice)

    for vote_choice in to_delete:
        db.delete(vote_choice)
    db.commit()

    #add new
    for option_id in option_ids:
        logger.info('Creating vote choice for option %s' % option_id)
        choice = VoteChoice(vote_id=vote.id,
            user_id=user.id,
            option_id=option_id,
            date_submitted=datetime.datetime.now())
        db.add(choice)
    db.commit()


def get_choices(db, vote_id):
    vote = db.query(Vote).filter_by(id=vote_id).first()
    if not vote:
        raise ValueError('Vote with id %s not found' % vote_id)

    return vote.choices


def get_my_choices(db, vote_id, user):
    vote = db.query(Vote).filter_by(id=vote_id).first()
    if not vote:
        raise ValueError('Vote with id %s not found' % vote_id)

    result = []
    for vote_choice in vote.choices:
        if vote_choice.user_id == user.id:
            result.append(vote_choice)

    return result


def get_pending_votes(db, user):
    # votes = db.query(Vote).filter(Vote.author_id!=user.id, Vote.status != VoteStatus.new)
    result = {}
    for invitation in user.invitations:
        result[invitation.vote.id] = invitation.vote

    for choice in user.choices:
        result[choice.vote.id] = choice.vote

    return [v for v in result.itervalues()]


def get_vote_results(db, vote_id):
    vote = db.query(Vote).filter_by(id=vote_id).first()
    if not vote:
        raise ValueError('Vote with id %s not found' % vote_id)

    titles = {}
    scores = {} # choice id, sum
    for choice in vote.choices:
        option = db.query(VoteOption).filter_by(id=choice.option_id).first()
        if not scores.has_key(option.id):
            scores[option.id] = 0

        scores[option.id] += 1
        titles[option.id] = option.text

    result = []
    for id, score in scores.iteritems():
        result.append((titles[id], score))

    max = 0
    max_title = ''

    for title, score in result:
        if score > max:
            max = score
            max_title = title

    result = [VoteResultScore(*pair) for pair in result]
    return VoteResultScoreHolder(vote_id, max_title, max, result)

