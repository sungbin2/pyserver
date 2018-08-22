from shared.commons import *
from shared.bundle_str import *
from types import SimpleNamespace
from flask import abort
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

import json

num_per_page = 10
json_quality = 1


def is_(): return request.method == ''


def is_GET(): return request.method == 'GET'


def is_POST(): return request.method == 'POST'


def is_PUT(): return request.method == 'PUT'


def is_DELETE(): return request.method == 'DELETE'


def is_json(): return request.accept_mimetypes["application/json"] >= json_quality


def data_GET(_k=None): return request.args if nohere(_k) else request.args[_k]


def data_POST(_k=None): return request.form if nohere(_k) else request.form[_k]


def data_json(_k=None): return request.json if nohere(_k) else request.json[_k]


def display(**kwargs):
    template = request.path \
        .replace('/new', '_edit') \
        .replace('/edit', '_edit')
    if fs2i(template[template.rfind('/') + 1:]) is not None:
        template = template[:template.rfind('/')]
    else:
        pass
    return render_template(template + '.html', sess=session, **kwargs)
