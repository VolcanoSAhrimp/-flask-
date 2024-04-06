from datetime import datetime

from flask import Blueprint, render_template, request, g, redirect, url_for, jsonify
from sqlalchemy.orm import aliased

from exts import db
from models import BorrowHistoryModel, UserModel, BooksModel, TagModel
from pandas import DataFrame

bp = Blueprint('simulation', __name__, url_prefix='/simulation')


@bp.route('/submit-book', methods=['GET'])
def submit_book():
    return render_template('simulation_add.html')
