# -*- coding: utf-8 -*-
from flask import Blueprint

top_bp = Blueprint('top', __name__, template_folder='templates')

from . import views  # noqa: E402,F401

