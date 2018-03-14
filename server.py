import psycopg2
import psycopg2.extras

from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

def connectToDB():
	connectionString = 'dbname=vetclinic user=vetman password=vet123 host=localhost'
	print connectionString
	try:
		return psycopg2.connect(connectionString)
	except:
		print("Can't connect to database")

@app.route('/vetstaff', methods=['GET', 'POST'])
def showVetStaff():
	conn = connectToDB()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	if request.method == 'POST':
	#add new entry into the database
		try:
			cur.execute("""INSERT INTO vetstaff (staffid, firstname, lastname, title, address, phonenumber, daysoff) 
			VALUES (nextval(%s), %s, %s, %s, %s, %s, %s);""", 
			("vetstaff_sequence", request.form['firstname'], request.form['lastname'], request.form['title'], request.form['address'], 
			request.form['phonenumber'], request.form['daysoff']) )
		except:
			print("ERROR inserting into vetstaff")
			conn.rollback()
		conn.commit()
	try:
		cur.execute("SELECT staffid, Firstname, lastname, title, address, phonenumber, daysoff from vetstaff")
	except:
		print("Error executing SELECT")
	results = cur.fetchall()
	print "FACTORY"
	print results
	return render_template('vetstaff.html', vetstaff=results)


@app.route('/owners')
def showOwnersUsingPythonDictionary():
	conn = connectToDB()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	try:
                cur.execute("select OwnerID, OwnerFirstName, OwnerLastName, Address, PhoneNumber from dogowners")
        except:
                print("Error executing select")
        results = cur.fetchall()
        print "FACTORY"
	print results
	return render_template('owners.html', dogowners=results)



@app.route('/custregresult/<dogname>')
def reply(dogname):
	#dogname=request.form['dogname']
	return render_template('custregresult.html', dogname=dogname)

@app.route('/customerregistration', methods=['GET', 'POST'])
def customerReg():
        conn = connectToDB()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	results = None
	if request.method == 'POST':
	#add new entry into the database
		try:
			cur.execute("""INSERT INTO dogowners (ownerid, ownerfirstname, ownerlastname, address, phonenumber)
                        VALUES (nextval(%s), %s, %s, %s, %s);""",
                        ("dogowners_sequence", request.form['ownerfirstname'], request.form['ownerlastname'], request.form['address'], request.form['phonenumber']) )
			print ("INSERT into dogowner done")
		except:
                        print("ERROR inserting into dogowners")
			conn.rollback()
		conn.commit()
		try:
                	cur.execute("SELECT last_value from dogowners_sequence")
        		fkeyOwner = cur.fetchone()[0]
			print("SELECT done")
			print fkeyOwner
		except:
                	print("Error executing select")
		results = cur.fetchall()
		try:
			cur.execute("""INSERT INTO dogs (dogid, dogname, chipnumber, dateofbirth, breed, ownerid, lastvaccinationdate, knownallergies, petinsurancedetails)
                        VALUES (nextval(%s), %s, %s, %s, %s, %s, %s, %s, %s);""",
                        ("dogs_sequence", request.form['dogname'], request.form['chipnumber'], request.form['dateofbirth'], request.form['breed'], fkeyOwner,
			request.form['lastvaccinationdate'], request.form['knownallergies'], request.form['petinsurancedetails']) )
			print("INSERT into dogs done")
		except:
			print("ERROR inserting into dogs")
			conn.rollback()
		conn.commit()
		return redirect(url_for('.reply', dogname=request.form['dogname']))
	print("FACTORY")
	return render_template('customerregister.html')

@app.route('/medicalHistory', methods=['GET', 'POST'])
def showMedicalHistory():
        conn = connectToDB()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	results = []
        if request.method == 'POST':
		searchTerm = request.form['ownerlastname']
		searchTerm2 = request.form['dogname']
		print ("S", searchTerm, searchTerm2)
        #execute SELECT statement
                try:
			cur.execute("SELECT dogowners.ownerlastname, dogowners.address, dogs.dogname, dogs.chipnumber, visits.dateofvisit, visits.problem, visits.insuranceclaim FROM dogowners RIGHT JOIN dogs on dogowners.ownerid = dogs.ownerid RIGHT JOIN visits on dogs.dogid = visits.dogid WHERE dogowners.ownerlastname = %s and dogs.dogname = %s order by visits.dateofvisit asc", (searchTerm, searchTerm2, ))
			print "Success"
			results = cur.fetchall()
		except Exception as e:
			print("Error selecting from tables: {}".format(e))
        print "FACTORY"
        print results
        return render_template('medicalHistory.html', results=results)


@app.route('/vaccinationDue', methods=['GET', 'POST'])
def showVaccinationDue():
        conn = connectToDB()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        results = []
        if request.method == 'POST':
                searchTerm = request.form['vacfrom']
                searchTerm2 = request.form['vacto']
                print ("S", searchTerm, searchTerm2)
        #execute SELECT statement
                try:
                        cur.execute("SELECT dogowners.ownerfirstname, dogowners.ownerlastname, dogowners.phonenumber, dogs.dogname, dogs.lastvaccinationdate FROM dogowners LEFT JOIN dogs on dogowners.ownerid = dogs.ownerid WHERE dogs. lastvaccinationdate BETWEEN %s and %s order by lastvaccinationdate asc", (searchTerm, searchTerm2, ))
                        print "Success"
                        results = cur.fetchall()
                except Exception as e:
                        print("Error selecting from tables: {}".format(e))
        print "FACTORY"
        print results
        return render_template('vaccinationDue.html', results=results)


#start the server
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug = True)
