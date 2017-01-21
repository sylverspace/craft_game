from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps

app = Flask(__name__)

app.secret_key = "secretkey"


def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('index'))
	return wrap


@app.route("/", methods=['GET', 'POST'])
def index():
	error=None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid credentials. Please try again.'
		else:
			session['logged_in'] = True
			flash('You were just logged in!')
			return redirect(url_for('lobby'))
	return render_template("index.html", title="RTS FLASK PROJECT", error=error)


@app.route("/logout")
def logout():
	session.pop('logged_in', None)
	flash('You were just logged out!')
	return redirect(url_for('index'))


@app.route("/lobby")
@login_required
def lobby():
    return render_template("lobby.html")


@app.route("/level_01")
def level_01():
    return render_template("level_01.html")



if __name__ == "__main__":
    app.run(debug=True, threaded=True)