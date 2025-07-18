from sqlalchemy.orm import Session 
from datetime import datetime, timedelta
from . import models



def get_challenge_quota(db, user_id):
    return (db.query(models.ChallengeQuota)
            .filter(models.ChallengeQuota.user_id == user_id)
            .first())


def create_challenge_quota(db, user_id):
    db_quota = models.ChallengeQuota(user_id=user_id)
    db.add(db_quota)
    db.commit()
    db.refresh(db_quota)
    return db_quota

def reset_quota_if_needed(db, quota):
    now = datetime.now()
    if now - quota.last_reset_date > timedelta(hours=24):
        quota.remaining_quota = 10
        quota.last_reset_date = now
        db.commit()
        db.refresh(quota)
    return quota

def create_challenge(
        db,
        difficulty, 
        created_by,
        title,
        options,
        correct_answer_id,
        explanation
):
    db_challenge = models.Challenge(
        difficulty=difficulty,
        created_by = created_by,
        title=title,
        options=options,
        correct_answer_id=correct_answer_id,
        explanation=explanation
    )
    db.add(db_challenge)
    db.commit()
    db.refresh(db_challenge)
    return db_challenge


def get_user_challenges(db, user_id):
    return db.query(models.Challenge).filter(models.Challenge.created_by==user_id).all()

