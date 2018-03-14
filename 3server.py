from lib.config import *
from lib import data_postgresql as pg

from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)


@app.route('/vetstaff', methods=['GET', 'POST'])
def showVetStaff():
	if request.method =='POST' and  'firstname' and 'lastname' and 'title' and 'address' and 'phonenumber' and 'daysoff' in request.form:
		result = pg.add_vetstaff("vetstaff_sequence", request.form['firstname'], request.form['lastname'], request.form['title'], request.form['address'],
                        request.form['phonenumber'], request.form['daysoff'])
	print "HERE"
	results = pg.get_vetstaff()
	return render_template('vetstaff.html', vetstaff=results)




#start the server
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug = True)
