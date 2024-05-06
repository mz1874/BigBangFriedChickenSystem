from functools import wraps
from flask import jsonify, session
from flask_login import current_user


def requires_permission(permission):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print("Decorator is called")
            if not current_user.is_authenticated:
                return jsonify({'message': 'User is not logged in'}), 401

            user_id = current_user.get_id()
            roles = session.get("role" + str(user_id), [])
            print("Roles:", roles)

            if permission in roles:
                return func(*args, **kwargs)
            else:
                return jsonify({'message': 'User does not have permission'}), 403

        return wrapper

    return decorator
