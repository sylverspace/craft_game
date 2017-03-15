from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify, g
import sqlite3 as sql
import os
import random
import json
from flask_sqlalchemy import SQLAlchemy
import ast #To change string list to a python list
import collections #To conte duplicate in iventory list using Counter()


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///RTSDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

class Data(db.Model):
	__tablename__ = "data"
	id = db.Column('id', db.Integer, primary_key=True)
	user = db.Column("user", db.String(20))
	password = db.Column("password", db.String(20))
	saltWater = db.Column("saltwater", db.String(20))
	freshWater = db.Column("freshWater", db.String(20))
	elixir = db.Column("elixir", db.String(20))
	pearl = db.Column("pearl", db.String(20))
	iron = db.Column("iron", db.String(20))
	coal = db.Column("coal", db.String(20))
	titanium = db.Column("titanium", db.String(20))
	diamond = db.Column("diamond", db.String(20))



	def __init__(self, id, user, password, saltWater, freshWater, elixir, pearl, iron, coal, titanium, diamond):
		
		self.id = id
		self.user = user
		self.password = password
		self.saltWater = saltWater
		self.freshWater = freshWater
		self.elixir = elixir
		self.pearl = pearl
		self.iron = iron
		self.coal = coal
		self.titanium = titanium
		self.diamond = diamond

	#def __repr__(self):
	#	return '{}'.format(self.id)


class Recipe(db.Model):

	num_of_rec = 0

	__tablename__ = "recipes"
	id = db.Column('id', db.Integer, primary_key=True)
	name = db.Column("name", db.String(20))
	type = db.Column("type", db.String(20))
	result = db.Column("result", db.String(20))
	prereq = db.Column("prereq", db.String(20))
	ing_1 = db.Column("ing_1", db.String(20))
	ing_qty_1 = db.Column("ing_qty_1", db.Integer)
	ing_2 = db.Column("ing_2", db.String(20))
	ing_qty_2 = db.Column("ing_qty_2", db.Integer)
	desc = db.Column("desc", db.String(20))

	def __init__(self, id, name, type, result, prereq, ing_1, ing_qty_1, ing_2, coal, ing_qty_2, desc):
		

		self.id = id
		self.name = name
		self.type = type
		self.result = result
		self.prereq = prereq
		self.ing_1 = ing_1
		self.ing_qty_1 = ing_qty_1
		self.ing_2 = ing_2
		self.ing_qty_2 = ing_qty_2
		self.desc = desc

		Recipe.num_of_rec += 1

	def __repr__(self):
		return '{}'.format(self.result)



'''
findtest = "saltWater"

userStuff = Data.query.filter_by(user="admin").first()
value = getattr(userStuff, findtest)
print (value)


temp = int(value)
temp += 1
value = str(temp)
print (value)
userStuff.saltWater = value

db.session.commit()

#newinfo = ExempleDB(7, 'sixth user', '123456', '25')
#db.session.add(newinfo)
#db.session.commit()

#update_this = ExempleDB.query.filter_by(id=6).first
#update_this.user = "New_user"
#db.session.commit()

'''


@app.route("/test")
def test():
	resultList = Data.query.all()
	return render_template('test.html', resultList=resultList)


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

		con = sql.connect("RTSDB.db")
		cur = con.execute("SELECT user, password from data")
		resultList = [row[0] for row in cur.fetchall()]

		if session['user'] in resultList:
			return redirect(url_for('map'))
		else:
			print "Failed"
			flash('Invalid Credentials!')
	return render_template("index.html", title="RTS FLASK PROJECT", **globals())



#Map_and_resources___________________________________________________________



@app.route("/map")
def map():
	if g.user:
		resources = Data.query.filter_by(user = g.user).all()
		return render_template("map.html", resources=resources)
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
	con = sql.connect("RTSDB.db")
	cur = con.execute("SELECT " + finding + " from data WHERE user='"+g.user+"'")

	for row in cur:
		print row

	#Update the value by one (for now)
	newval = int(row[0]) + 1
	newval = str(newval)

	#Insert new values
	#Data.update().where(user=g.user).with_entities(finding).values(newval)
	#db.session.commit()

	cur.execute("UPDATE data SET " + finding + " = " + newval + " WHERE user='" + g.user +"'")
	con.commit()
	con.close()

	return json.dumps({"finding":finding, "newval":newval})



#Inventory____________________________________________________


@app.route("/inventory")
def inventory():
	if g.user:

		con = sql.connect("RTSDB.db")

		#Showing ressources
		resources = Data.query.filter_by(user = g.user).all()

		#Getting current inventory
		cur = con.execute("SELECT items from inventory WHERE user='" + g.user +"'").fetchone()
		#First row of the list (all items)
		x = cur[0]
		#Stinged list as real list
		currInv = ast.literal_eval(x)

		counter = collections.Counter(currInv)
		print counter
		return render_template("inventory.html", resources=resources, currInv=currInv, counter=counter)
	return redirect(url_for('index'))



#Crafting______________________________________________________


@app.route("/craft")
def craft():
	if g.user:
		#Get all recipes from Table recipes
		resources = Data.query.filter_by(user = g.user).all()
		recipes = Recipe.query.all()


		return render_template("craft.html", recipes=recipes, resources=resources)

	return redirect(url_for('index'))


'''
@app.route("/showComponent/<clickedComponent>")
def showComponent(clickedComponent):
	recipe = Data.query.filter_by(name = clickedComponent).all()
	return recipe
'''



@app.route("/craftProcess/<item>", methods=['POST'])
def craftProcess(item):

	con = sql.connect("RTSDB.db")
	#Getting FIRST required mats
	cur = con.execute("SELECT ing_1 from recipes WHERE result='"+item+"'").fetchone()
	ing_1 = cur[0]
	cur = con.execute("SELECT ing_qty_1 from recipes WHERE result='"+item+"'").fetchone()
	ing_qty_1 = cur[0]

	#Getting SECOND required mats
	cur = con.execute("SELECT ing_2 from recipes WHERE result='"+item+"'").fetchone()
	ing_2 = cur[0]
	cur = con.execute("SELECT ing_qty_2 from recipes WHERE result='"+item+"'").fetchone()
	ing_qty_2 = cur[0]
	
	#Getting FIRST concerned ressource and removing
	cur = con.execute("SELECT " + ing_1 + " from data WHERE user='" + g.user +"'").fetchone()
	oldVal = cur[0]
	newVal1 = int(oldVal) - ing_qty_1

	#Getting SECOND concerned ressource and removing
	cur = con.execute("SELECT " + ing_2 + " from data WHERE user='" + g.user +"'").fetchone()
	oldVal = cur[0]
	newVal2 = int(oldVal) - ing_qty_1
	
	#Updating resources
	con.execute("UPDATE data SET " +\
		ing_1 + " = " + str(newVal1) +","+\
		ing_2 + " = " + str(newVal2) +\
		" WHERE user='" + g.user +"'")

	#Getting current inventory
	cur = con.execute("SELECT items from inventory WHERE user='" + g.user +"'").fetchone()
	# Tuple into list
	x = list(cur)
	#First row of the list (all items)
	x = x[0]
	#Stinged list as real list
	x = ast.literal_eval(x)
	# Add the item
	x.append(item)
	# Restring the list
	x = json.dumps(x)
	print x
	
	#Update the items
	con.execute('UPDATE inventory SET items = ? WHERE user = ? ', (x, g.user,))


	con.commit()
	con.close()

	#From SQLAlchemy
	#clickedItem = Recipes.query.filter_by(result = item).all()
	#resource = Data.query.filter_by(user = g.user).all()
	stringMessage = item + ' was added to inventory!'
	return json.dumps({'stringMessage':stringMessage, 'newVal1':newVal1, 'newVal2':newVal2})
	

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
	con = sql.connect("RTSDB.db")
	cur = con.execute("SELECT * from data WHERE user='"+userx+"'")
	print "Userx is: %s", userx
	userInfoList = [row[0] for row in cur.fetchall()]
	print userInfoList
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