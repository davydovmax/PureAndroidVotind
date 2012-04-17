from model import *


def get_user(db, phone_id):
    return db.query(User).filter_by(phone_id=phone_id).first()

def create_user(db, phone_id, fullname, email):
    user = User(phone_id=phone_id, fullname=fullname, email=email)
    db.add(user)
    return user

def create_vote(db, author_id, title, text, is_private, is_multiple_choice, publication_date, start_date, end_date, results_date):
    vote = Vote(author_id=author_id,
        title=title,
        text=text,
        is_private=is_private,
        publication_date=publication_date,
        start_date=start_date,
        end_date=end_date,
        results_date=results_date,
        is_multiple_choice=is_multiple_choice)
    db.add(vote)
    return vote