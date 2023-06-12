from PyQt5 import QtCore, QtGui, QtWidgets
from flask_mysqldb import MySQL
from flask import Flask,render_template,request,redirect,url_for,session,flash
import pymysql
import MySQLdb.cursors
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bangkit123'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pintarkur'
mysql = MySQL(app)

#Authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        if '@' not in email:
            flash('Invalid Email', 'Cek Kembali Email Anda')
            return email
        else:
            password = request.form['password']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM user WHERE email = %s AND PASSWORD = %s", ([(email), (password)]))
            account = cursor.fetchone()
            if account:
                session['loggedin'] = True
                session['nama'] = account['nama']
                return redirect(url_for('analisis'))
            else:
                flash("Email/password! salah", "danger")
    return render_template('auth/login.html',title="Login")

@app.route('/daftar', methods=['GET','POST'])
def daftar():
    if request.method == 'POST' and 'nama' in request.form and 'password' in request.form and 'email' in request.form:
        nik = request.form['nik']
        if len(nik) != 16 :
            flash("Masukkan 16 digit NIK anda!", "danger")
        elif nik.isnumeric() == False :
            flash("Masukkan angka dengan benar!", "danger") 
        else:
            nama = request.form['nama']
            email = request.form['email']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute( "SELECT * FROM user WHERE email LIKE %s", [email] )
            account = cursor.fetchone()
            if account:
                flash("Email telah digunakan!", "danger")
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash("Alamat email invalid!", "danger")
            else:
                password = request.form['password']
                cursor.execute('INSERT INTO user VALUES (%s,%s,%s,%s)', (nik,nama,email,password))
                mysql.connection.commit()
                flash("Registrasi Berhasil!", "Success")
                return redirect(url_for('login'))
    elif request.method == 'POST':
        flash("Mohon isi form!", "danger")
    return render_template('auth/daftar.html',title="Sign up")
#End of Authentication


#Cari
@app.route('/cari')
def cari():
    if 'logged_in' in session:
        return render_template('features/cari.html',title="Cari Penyalur")
    return redirect(url_for('login'))

@app.route('/cari/penyalur_terdekat')
def cari_terdekat():
    if 'loggedin' in session:
        return render_template('features/cari_penyalur_terdekat.html', tittle="Cari Penyalur Terdekat")
    return redirect(url_for('login'))
#End of Cari


@app.route('/analisis')
def analisis():
    if 'loggedin' in session:
        return render_template('features/analisis.html',title="Analisis")
    return redirect('login')

#Home
@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('auth/home.html',nama=session['nama'],title="Home")
    return redirect(url_for('login'))

if __name__ == "__main__" :
    app.run(debug=True)