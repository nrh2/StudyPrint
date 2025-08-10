# -*- coding: utf-8 -*-
from flask import Blueprint

narabikae_bp = Blueprint('narabikae', __name__, template_folder='templates',url_prefix='/narabikae')

from . import views  # noqa: E402,F401

