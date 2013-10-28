from flask import Flask, g
from flask import render_template
from modules import u, d, w
from assets import assets

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(u.mod, url_prefix='/u')
app.register_blueprint(d.mod, url_prefix='/d')
app.register_blueprint(w.mod, url_prefix='/w')

assets.init_app(app)

@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
