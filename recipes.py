#
#########
#RECIPES#
#########
#

class Recipes:

	_registry = []
	recipesCount = 0

	def __init__(self, name, type, result, prereq, ing_1, ing_1_qty, ing_2, ing_2_qty, desc):
		self._registry.append(self)
		self.name = name
		self.type = type
		self.result = result
		self.prereq = prereq
		self.ing_1 = ing_1
		self.ing_1_qty = ing_1_qty
		self.ing_2 = ing_2
		self.ing_2_qty = ing_2_qty
		self.desc = desc

	def getName(self):
		return self.name

	def displayCount(self):
		print "Number of recipes: %s" % Recipes.recipesCount

	def __getitem__(self, val):
		print val


#Recipes list


basicPistol = Recipes("Basic pistol", "weapon", "basicPistol", None, "saltWater", 20, "iron", 5, "Light hand gun.")


basicMedpack = Recipes("Basic Medpack", "Tools", "medpack", None, "saltWater", 20, "freshWater", 5, "Heals 10 health points.")

recipeDict = {}

for recipe in Recipes._registry:
	recipeDict[str(recipe.result)] = recipe

print recipeDict



'''
for recipe in Recipes._registry:
	print recipe
'''

#####