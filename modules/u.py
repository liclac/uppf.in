import os
import hashlib
from urlparse import urlparse
from flask import Blueprint, request
from flask import render_template, url_for, redirect, abort
from util import path_for, make_identifier, plaintextify

mod = Blueprint('u', __name__)

class URL(object):
	def __init__(self, id=None, hash=None, url=None):
		if id:
			self.id = id
			self.url = self.read_from('url_by_id', self.id)
		elif hash:
			self.hash = hash
			self.id = self.read_from('id_by_hash', self.hash)
			self.url = self.read_from('url_by_id', self.id)
		elif url:
			self.url = url if urlparse(url).scheme else 'http://' + url
			try:
				self.id = self.read_from('id_by_hash', self.hash)
			except:
				while True:
					# Keep doing this until we find an unoccupied slot...
					self.id = make_identifier()
					if not os.path.exists(path_for('u', 'url_by_id', self.id + '.txt')):
						break
		else:
			raise Exception("Can't create an URL without an ID, a Hash or an URL")
	
	@property
	def hash(self):
		# This is EXPENSIVE, so don't do it unnecessarily...
		if not getattr(self, '_hash', None):
			self._hash = hashlib.sha1(self.url).hexdigest()
		return self._hash
	
	@hash.setter
	def set_hash(self, hash):
		self._hash = hash
	
	def read_from(self, type_, key):
		path = path_for('u', type_, key + '.txt')
		with open(path) as f:
			return f.read()
	
	def save(self):
		with open(path_for('u', 'id_by_hash', self.hash + '.txt'), 'w') as f:
			f.write(self.id)
		with open(path_for('u', 'url_by_id', self.id + '.txt'), 'w') as f:
			f.write(self.url)

@mod.route('/')
def index():
	if 'url' in request.args:
		url = URL(url=request.args['url'])
		url.save()
		return plaintextify(url_for('.go', id=url.id, _external=True))
	return render_template('u/index.html')

@mod.route('/<id>')
def go(id):
	url = URL(id=id)
	try:
		return redirect(url.url)
	except:
		abort(404)
