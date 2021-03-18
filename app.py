from flask import Flask, render_template, request, url_for, redirect, flash, json
from flask_mysqldb import MySQL

app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'Admin'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"


@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts")
    data = cur.fetchall()
    return render_template("index.html", contacts=data)


@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form["fullname"]
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)",
                    (fullname, phone, email))
        mysql.connection.commit()
        flash("Contact Added successfully")

        return redirect(url_for("Index"))


@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()	
    cur.execute("SELECT * FROM contacts WHERE id = {0}".format(id))
    data = cur.fetchall()
    print(data[0])
	
    return render_template('edit-contact.html', contact=data[0])


@app.route("/update/<id>", methods=["POST"])
def updata_contact(id):
    if request.method == "POST":
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
			UPDATE contacts
			SET fullname = %s,
				email = %s,
				phone = %s
			WHERE id= %s	
		""", (fullname, email, phone, id))
        mysql.connection.commit()
        flash("Contact Updated Successfully")
        return redirect(url_for("Index"))


@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM contacts WHERE id = {0}".format(id))
    mysql.connection.commit()
    flash('Contact Removed successfully')
    return redirect(url_for("Index"))


@app.route("/ruta_json")
def json_arch():

    data = query_db("SELECT * FROM contacts")
    archijson = json.dumps(data)
    print(archijson)
    with open("sample.json", "w") as outfile: 
    	outfile.write(archijson)
    flash('File Create')
    return redirect(url_for("Index"))


def query_db(query, args=(), one=False):
    cur = mysql.connection.cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
              for i, value in enumerate(row)) for row in cur.fetchall()]

    return (r[0] if r else None) if one else r


if __name__ == '__main__':
    app.run(port=3000, debug=True)
