import os
import markdown2
from flask import Blueprint
from flask import render_template, abort
from util import path_for, strip_end

mod = Blueprint('w', __name__)

class Subpage(object):
	def __init__(self, parent_path, subpath):
		subpath = strip_end(subpath, '.md')
		
		self.path = os.path.join(parent_path, subpath)
		self.components = os.path.split(self.path)
		self.title = self.components[-1].replace('_', ' ')

class Page(object):
	subpages = []
	
	def __init__(self, path):
		self.path = path
		self.components = [c for c in self.path.split(os.path.sep) if c]
		self.title = self.components[-1].replace('_', ' ') if self.components else 'Index'
		self.realpath = os.path.abspath(path_for('w', path))
		
		if os.path.isdir(self.realpath):
			self.filepath = os.path.join(self.realpath, '_Index.md')
			self.load_subpages()
		else:
			self.filepath = self.realpath + '.md'
		
		self.exists = os.path.exists(self.filepath)
		if self.exists:
			self.load()
	
	def load(self):
		with open(self.filepath) as f:
			self.html = markdown2.markdown(f.read())
	
	def load_subpages(self):
		self.subpages = [
			Subpage(self.path, item) for item in os.listdir(self.realpath)
			if item != '_Index.md'
		]



@mod.route('/', defaults={'path': ''})
@mod.route('/<path:path>')
def page(path):
	page = Page(path)
	return render_template('w/page.html', page=page)
