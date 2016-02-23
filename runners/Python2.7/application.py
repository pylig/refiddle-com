import json
import settings
from flask import Flask, request
from worker import Worker


app = Flask(
    import_name=settings.APPLICATION_NAME
)


@app.route(settings.EVALUATE_URL, methods=['POST'])
def evaluate():
    return __validate(action='evaluate')


@app.route(settings.REPLACE_URL, methods=['POST'])
def replace():
    return __validate(action='replace')


def __validate(action):
    error = {}

    pattern = request.form.get('pattern', None)
    corpus_text = request.form.get('corpus_text', None)
    replace_text = request.form.get('replace_text', '')

    if not pattern:
        error['pattern'] = ['This field is required']
    if not corpus_text:
        error['corpus_text'] = ['This field is required']

    if error:
        return json.dumps(error), 400

    worker = Worker(
        action=action,
        pattern=pattern,
        corpus_text=corpus_text,
        replace_text=replace_text
    )

    return (
        (json.dumps(worker.result, separators=(',', ':'))
         if worker.result else ''),
        (200 if worker.is_success else 400)
    )
