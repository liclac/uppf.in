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

class Component(object):
	def __init__(self, last_component, new_part):
		self.path = os.path.join(last_component.path if last_component else '', new_part)
		self.title = new_part

class Page(object):
	subpages = []
	
	def __init__(self, path):
		self.path = path
		
		self.components = []
		last_component = None
		for comp in self.path.split(os.path.sep):
			if comp:
				last_component = Component(last_component, comp.replace('_', ' '))
				self.components.append(last_component)
		
		self.title = last_component.title if last_component else 'Index'
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
