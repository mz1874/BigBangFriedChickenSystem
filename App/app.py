from App import create_app
from flask import jsonify, render_template, request,session
from werkzeug.exceptions import MethodNotAllowed
from functools import wraps
from App.common.CommonResponse import CommonResponse
from flask_login import current_user
from App.common.decorators import requires_permission
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

    return jsonify(CommonResponse.failure(str(error), data=None, status_code=500))

@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed(error):
    return jsonify({"error": "Method Not Allowed"}), 405  # 返回自定义的错误响应和状态码 405

@app.route("/example")
def example_route():
    raise Exception("This is an example exception")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404




if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
