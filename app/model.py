import logging
import datetime
from sqlalchemy import Column, Integer, Sequence, Boolean, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

import config


logger = logging.getLogger('srv.'+__name__)


def now():
    return datetime.datetime.now()


class User(config.env.Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    phone_id = Column(String(16), nullable=False, unique=True)
    fullname = Column(String(60), nullable=False)
    email = Column(String(42), nullable=False)
    date_registered = Column(DateTime(), default=now)
    votes = relationship('Vote', cascade='all,delete', backref=backref('author', order_by=id))
    invitations = relationship('VoteInvitation', cascade='all,delete', backref=backref('user', order_by=id))
    choices = relationship('VoteChoice', cascade='all,delete', backref=backref('user', order_by=id))

    def __init__(self, phone_id, fullname, email):
        self.phone_id = phone_id
        self.fullname = fullname
        self.email = email

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.phone_id, self.fullname, self.email)

    def json_dict(self):
        return {'id': self.id,
                'phone_id': self.phone_id,
                'fullname': self.fullname,
                'email': self.email,
                'date_registered': self.date_registered}


class Vote(config.env.Base):
    __tablename__ = 'votes'
    id = Column(Integer, Sequence('vote_id_seq'), primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    title = Column(String(120), nullable=False)
    text = Column(String(330), nullable=True)
    is_private = Column(Boolean(), default=False, nullable=False)
    is_multiple_choice = Column(Boolean(), default=False, nullable=False)
    date_created = Column(DateTime(), default=now, nullable=False)
    publication_date = Column(DateTime(), nullable=False)
    start_date = Column(DateTime(), nullable=False)
    end_date = Column(DateTime(), nullable=False)
    results_date = Column(DateTime(), nullable=False)
    options = relationship('VoteOption', cascade='all,delete', backref=backref('vote', order_by=id))
    invitations = relationship('VoteInvitation', cascade='all,delete', backref=backref('vote', order_by=id))
    choices = relationship('VoteChoice', cascade='all,delete', backref=backref('vote', order_by=id))

    def __init__(self, author_id, title, text, is_private, is_multiple_choice,
                 publication_date, start_date, end_date, results_date):
        self.author_id = author_id
        self.title = title
        self.text = text
        self.is_private = is_private
        self.is_multiple_choice = is_multiple_choice
        self.publication_date = publication_date
        self.start_date = start_date
        self.end_date = end_date
        self.results_date = results_date

    def __repr__(self):
        return "<Vote('%s','%s', '%s')>" % (self.title, self.text, self.author_id)

    def json_dict(self):
        return {'id': self.id,
                'author_id': self.author_id,
                'title':  self.title,
                'text': self.text,
                'is_private': self.is_private,
                'date_created': self.date_created,
                'publication_date': self.publication_date,
                'start_date': self.start_date,
                'end_date': self.end_date,
                'results_date': self.results_date,
                'is_multiple_choice': self.is_multiple_choice}


class VoteOption(config.env.Base):
    __tablename__ = 'options'
    id = Column(Integer, Sequence('vote_option_id_seq'), primary_key=True, nullable=False)
    text = Column(String(120), nullable=False)
    vote_id = Column(Integer, ForeignKey('votes.id', ondelete='CASCADE'))

    def __init__(self, vote_id, text):
        self.vote_id = vote_id
        self.text = text

    def __repr__(self):
        return "<VoteOption('%s','%s')>" % (self.vote_id, self.text)

    def json_dict(self):
        return {'id': self.id,
                'vote_id': self.vote_id,
                'text': self.text}


class VoteInvitation(config.env.Base):
    __tablename__ = 'invitations'
    id = Column(Integer, Sequence('vote_guest_id_seq'), primary_key=True)
    vote_id = Column(Integer, ForeignKey('votes.id', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    is_considered = Column(Boolean(), default=False, nullable=False)
    is_accepted = Column(Boolean(), default=False, nullable=False)

    def __init__(self, vote_id, user_id, is_considered, is_accepted):
        self.vote_id = vote_id
        self.user_id = user_id
        self.is_considered = is_considered
        self.is_accepted = is_accepted

    def __repr__(self):
        return "<VoteInvitation('%s','%s','%s','%s')>" % (self.vote_id, self.user_id,
                                                          self.is_considered, self.is_accepted)

    def json_dict(self):
        return {'id': self.id,
                'vote_id': self.vote_id,
                'user_id': self.user_id,
                'is_considered': self.is_considered,
                'is_accepted': self.is_accepted}


class VoteChoice(config.env.Base):
    __tablename__ = 'choices'
    id = Column(Integer, Sequence('vote_choice_id_seq'), primary_key=True)
    vote_id = Column(Integer, ForeignKey('votes.id', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    option_id = Column(Integer, ForeignKey('options.id', ondelete='CASCADE'))
    date_submitted = Column(DateTime(), default=now)

    def __init__(self, vote_id, user_id, option_id, date_submitted):
        self.vote_id = vote_id
        self.user_id = user_id
        self.option_id = option_id
        self.date_submitted = date_submitted

    def __repr__(self):
        return "<VoteInvitation('{0:>s}','{1:>s}','{2:>s}','{3:>s}')>".\
            format(self.vote_id, self.user_id, self.option_id, self.date_submitted)

    def json_dict(self):
        return {'id': self.id,
                'vote_id': self.vote_id,
                'user_id': self.user_id,
                'option_id': self.option_id,
                'date_submitted': self.date_submitted}
