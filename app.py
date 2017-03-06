from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify, g
from functools import wraps
from config import *
from recipes import *
import sqlite3 as sql
import os
import random
import json

app = Flask(__name__)

app.secret_key = os.urandom(24)


@app.before_request
def before_request():
	g.user = None
	if 'user' in session:
		g.user = session['user']

@app.route('/getsession')
def getsession():
	if 'user' in session:
		return session['user']
	return 'Not logged in!'

@app.route("/logout")
def logout():
	session.pop('user', None)
	flash('You were just logged out!')
	return redirect(url_for('index'))


@app.route("/", methods=['GET', 'POST'])
def index():
	session.pop('user', None)
	error = None
	if request.method == 'POST':
		session['user'] = request.form['username']
		enteredPassword = request.form['password']

		con = sql.connect("RTS_DB.db")
		cur = con.execute("SELECT user, password from data")
		resultList = [row[0] for row in cur.fetchall()]

		if session['user'] in resultList:
			return redirect(url_for('map'))
		else:
			print "Failed"
			flash('Invalid Credentials!')
	return render_template("index.html", title="RTS FLASK PROJECT", **globals())



@app.route("/map")
def map():
	if g.user:
		getUserInfo(g.user)
		return render_template("map.html", **globals())
	return redirect(url_for('index'))


@app.route('/gather/<clickedRegion>', methods=['POST'])
def gather(clickedRegion):
	def gatherChances():
		finding = ""
		randomResult = random.random()
		if randomResult <= 0.005:
			if clickedRegion == "water":
				finding = "pearl" #Legendary
			if clickedRegion == "mine":
				finding = "diamond" #Legendary
		elif randomResult > 0.005 and randomResult <= 0.05:
			if clickedRegion == "water":
				finding = "elixir" #Epic
			if clickedRegion == "mine":
				finding = "titanium" #Epic
		elif randomResult > 0.05 and randomResult <= 0.20:
			if clickedRegion == "water":
				finding = "freshWater" #Rare
			if clickedRegion == "mine":
				finding = "coal" #Rare
		else:
			if clickedRegion == "water":
				finding = "saltWater" #Common
			if clickedRegion == "mine":
				finding = "iron" #Common
			
		#print randomResult
		#print finding
		return finding

	finding = gatherChances()

	#Get value from database to show them in HTML
	con = sql.connect("RTS_DB.db")
	cur = con.execute("SELECT " + finding + " from data WHERE user='"+g.user+"'")
	#for row in cur:
		#print row[0]

	#Update the value by one (for now)
	newval = int(row[0]) + 1
	newval = str(newval)

	#Insert new values
	cur.execute("UPDATE data SET " + finding + " =" + newval + " WHERE user='" + g.user +"'")
	con.commit()
	con.close()

	return json.dumps({"finding":finding, "newval":newval})


@app.route("/inventory")
def inventory():
	if g.user:
		return render_template("inventory.html", **globals())
	return redirect(url_for('index'))


@app.route("/craft")
def craft():
	if g.user:
		#Recipes from database no longer used
		
		return render_template("craft.html", **globals())
	return redirect(url_for('index'))


@app.route("/craftProcess/<item>", methods=['POST'])
def craftProcess(item):
	getUserInfo(g.user)
	if item == "medpack":
		saltWater -= basicMedpack.ing_qty_1
		iron -= basicMedpack.ing_qty_2
		print basicMedpack.name

	return saltWater


@app.route("/showComponent/<clickedComponent>")
def showComponent(clickedComponent):
	con = sql.connect("RTS_DB.db")
	cur = con.cursor()
	cur.execute("SELECT * FROM recipes WHERE name="+clickedComponent+"")
	rows = cur.fetchall()
	for row in rows:
		print row
	name= row[1]
	
	

@app.route("/3d_test_1")
def test_1():
	if g.user:
		return render_template("3d_test_1.html")
	return redirect(url_for('index'))


@app.route("/3d_test_2")
def test_2():
	if g.user:
		return render_template("3d_test_2.html")
	return redirect(url_for('index'))

@app.route("/3d_test_3")
def test_3():
	if g.user:
		return render_template("3d_test_3.html")
	return redirect(url_for('index'))


def getUserInfo(userx):
	con = sql.connect("RTS_DB.db")
	cur = con.execute("SELECT * from data WHERE user='"+userx+"'")
	userInfoList = [row[0] for row in cur.fetchall()]
	global saltWater, freshWater, elixir, pearl, \
	iron, coal, titanium, diamond
	saltWater = row[3]
	freshWater = row[4]
	elixir = row[5]
	pearl = row[6]
	iron = row[7]
	coal = row[8]
	titanium = row[9]
	diamond = row[10]
	con.commit()
	con.close()

if __name__ == "__main__":
    app.run(debug=True, threaded=True)