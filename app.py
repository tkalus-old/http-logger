#!/usr/bin/env python
import logging
import json
from flask import Flask, request
from os import getenv
app = Flask(__name__)


@app.before_first_request
def setup_logging():
    if not app.debug:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_format = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s'
            '[in %(filename)s:%(lineno)d]')
        console_handler.setFormatter(console_format)
        app.logger.setLevel(logging.DEBUG)
        app.logger.addHandler(console_handler)
        app.logger.info('App startup')


@app.route('/', methods=['GET', 'POST'], defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST'])
def log(path):
    output = []
    if request.headers:
        output.append("\n")
        output.append(str(request.headers))
    if request.form:
        output.append(request.form)
    if request.get_json(silent=True, cache=True):
        output.append(json.dumps(request.get_json(), indent=4))
    app.logger.info("%s\n", "".join(output))
    return 'OK'

if __name__ == '__main__':
    app.run(host=getenv('HOST', '127.0.0.1'),
            port=int(getenv('PORT', '7777')))
