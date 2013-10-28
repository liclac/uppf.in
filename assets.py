from flask.ext.assets import Environment, Bundle

assets = Environment()

css = Bundle(
	'css/style.less',
	
	filters='less', output='gen/style.css'
)

js = Bundle(
	'lib/jquery.js',
	'lib/bootstrap/dist/js/bootstrap.js',
	'js/script.js',
	
	filters=None, output='gen/script.js'
)

assets.register('css_all', css)
assets.register('js_all', js)
