import os
import markdown2
from flask import Blueprint
from flask import render_template, abort
from util import path_for

mod = Blueprint('d', __name__)

class Document(object):
	def __init__(self, path):
		self.path = path
		self.filename = os.path.basename(path)
		with open(self.path) as f:
			text = f.read()
			text = text.replace('->', '&rarr;')
			text = text.replace('<-', '&larr;')
			self.html = markdown2.markdown(text)

@mod.route('/')
def index():
	return render_template('d/index.html')

@mod.route('/<path:path>')
def document(path):
	path = path_for('d', path)
	if not os.path.exists(path):
		abort(404)
	doc = Document(path)
	return render_template('d/document.html', document=doc)

