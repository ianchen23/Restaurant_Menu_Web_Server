####################################
# Web server using Flask framework #
####################################

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#@app.route('/')

@app.route('/restaurants/<int:restaurantId>/menu/JSON/')
def restaurantMenuJSON(restaurantId):
	restaurant = session.query(Restaurant).filter_by(id = restaurantId).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurantId)
	return jsonify(MenuItem=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurantId>/menu/<int:menuId>/JSON/')
def restaurantMenuItemJSON(restaurantId, menuId):
	item = session.query(MenuItem).filter_by(id = menuId).one()
	return jsonify(MenuItem=item.serialize)

@app.route('/restaurants/<int:restaurantId>/')
def restaurantMenu(restaurantId):
	restaurant = session.query(Restaurant).filter_by(id = restaurantId).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurantId)
	# output = ''
	# for i in items:
	# 	output += i.name + '</br>'
	# 	output += i.price + '</br>'
	# 	output += i.description + '</br>'
	# 	output += '</br>'
	# return output
	return render_template('menu_item.html', restaurant = restaurant, items = items)

@app.route('/restaurants/<int:restaurantId>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurantId):
	if request.method == 'POST':
		newItem = MenuItem(name=request.form['name'], description=request.form['description'],
			price=request.form['price'], course=request.form['course'], restaurant_id=restaurantId)
		session.add(newItem)
		session.commit()
		return redirect(url_for('restaurantMenu', restaurantId=restaurantId))
	else:
		return render_template('new_menu_item.html', restaurant_id=restaurantId)

@app.route('/restaurants/<int:restaurantId>/<int:menuId>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurantId, menuId):
	editedItem = session.query(MenuItem).filter_by(id=menuId).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		session.add(editedItem)
		session.commit()
		flash(editedItem.name + " edited!")
		return redirect(url_for('restaurantMenu', restaurantId=restaurantId))
	else:
		return render_template('edit_menu_item.html', restaurant_id=restaurantId, item=editedItem)

@app.route('/restaurants/<int:restaurantId>/<int:menuId>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurantId, menuId):
	deleteItem = session.query(MenuItem).filter_by(id=menuId).one()
	if request.method == 'POST':
		session.delete(deleteItem)
		session.commit()
		flash(deleteItem.name + " deleted!")
		return redirect(url_for('restaurantMenu', restaurantId=restaurantId))
	else:
		return render_template('delete_menu_item.html', restaurant_id=restaurantId, item=deleteItem)

#############################
if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
