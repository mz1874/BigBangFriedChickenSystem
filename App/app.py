from App import create_app
from flask import jsonify, render_template, request
from functools import wraps

app = create_app()


@app.before_request
def before_request():
    if not request.path.startswith('/static/'):
        pass


@app.after_request
def after_request(response):
    if not request.path.startswith('/static/'):
        pass
    return response


@app.teardown_appcontext
def teardown_request(exception=None):
    if exception is not None:
        pass


@app.errorhandler(Exception)
def handle_global_exception(error):
    error_response = {
        "error": str(error),
        "message": "An internal server error occurred"
    }
    return jsonify(error_response), 500


@app.route("/example")
def example_route():
    raise Exception("This is an example exception")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# def requires_permission(permission):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             return func(*args, **kwargs)
#
#         return wrapper
#     return decorator


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
