import os
import string
import random
import hashlib
from flask import current_app, Response

def path_for(*components):
	components = [ path.replace('../', '') for path in components ]
	dir_path = os.path.join(current_app.root_path, 'content', *components[:-1])
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	return os.path.join(dir_path, components[-1])

def make_identifier(max_length=10):
	possible_chars = string.ascii_uppercase + \
						string.ascii_lowercase + \
						string.digits
	length = random.randint(1, max_length)
	return ''.join(random.choice(possible_chars) for _ in range(length))

def plaintextify(text):
	return Response(text, content_type='text/plain')

def strip_end(text, suffix):
	if not text.endswith(suffix):
		return text
	return text[:len(text)-len(suffix)]
