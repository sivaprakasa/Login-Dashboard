from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import re

app = Flask(__name__)
app.secret_key = '1234'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'prakasam'
app.config['MYSQL_DB'] = 'institue'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password))
        users = cursor.fetchone()
        cursor.close()
        if users:
            session['loggedin'] = True
            session['username'] = users[1]
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/index')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', username=username)
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cpassword = request.form['cpassword']
        email = request.form['email']
        phone = request.form['phone']
        dob = request.form['dob']
        if password == cpassword:
            if len(password) < 6:
                flash = 'Password must be at least six characters'
                return render_template('register.html')
            elif not re.search(r'[A-Z]{1}', password):
                flash('Password must contain at one letter capital')
                return render_template('register.html')
            elif not re.search(r'[a-z]{3}', password):
                flash('Password must contain at three small latter')
                return render_template('register.html')
            elif not re.search(r'[!@#$&]{1}', password):
                flash('Password must contain at least one special symbol')
                return render_template('register.html')
            elif not re.search(r'\d{1}', password):
                flash('Password must contain at least one digit')
                return render_template('register.html')
            else:
                cursor = mysql.connection.cursor()
                cursor.execute("INSERT INTO user(username,password,cpassword,email,phone,dob)VALUES(%s,%s,%s,%s,%s,%s)",(username,password,cpassword,email,phone,dob))
                mysql.connection.commit()
                cursor.close()
                return redirect(url_for('login'))
        else:
            flash('Passwords do not match')
            return render_template('register.html')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)