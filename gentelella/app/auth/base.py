from ..config import authe


def create_account(email, passw):
    # Setup initial user account
    try:
        user = authe.create_user_with_email_and_password(email, passw)
        # TODO: create user entry in database and auto setup
    except Exception as e:
        return None, e

    return user, None


def log_in(email, passw):
    # Log the user in
    try:
        user = authe.sign_in_with_email_and_password(email, passw)
        # TODO: update user records
    except Exception as e:
        return None, e
    return user, None
