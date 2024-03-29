import csv
from functools import wraps
import pickle
from flask import Flask, jsonify, render_template, request, session, redirect, url_for, flash,Response
from flask_paginate import Pagination, get_page_args
import pandas as pd
from hashlib import md5
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection  import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics import classification_report
# from sklearn.metrics import confusion_matrix
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from imblearn.over_sampling import SMOTE
import io
import xlwt

app = Flask(__name__)
app.secret_key = 'AHjkaIllq!@$%^&*()'
  
# ===============
# ==== Model ====

# conect db MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_buku'

  
# get_book
def get_books(offset=0, per_page=10):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM tbl_buku LIMIT %s, %s', (offset, per_page))
    return cursor.fetchall()

# create tables
def create_tables():
    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='db_buku')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE `tbl_user` (`id_user` int(11) NOT NULL AUTO_INCREMENT,`nama` varchar(50) NOT NULL,`username` varchar(50) NOT NULL,`password` varchar(50) NOT NULL,`email` varchar(50) NOT NULL,`address` varchar(50) NOT NULL,PRIMARY KEY (`id_user`)) ENGINE=InnoDB DEFAULT CHARSET=latin1")
    cursor.execute("CREATE TABLE `tbl_buku` (`id_buku` int(11) NOT NULL AUTO_INCREMENT,`judul` varchar(250) NOT NULL,`penerbit` varchar(50) NOT NULL,`tahun_terbit` int(11) NOT NULL,`tempat_terbit` varchar(50) NOT NULL,`pengarang` varchar(50) NOT NULL,`kategori` varchar(50) NOT NULL,PRIMARY KEY (`id_buku`)) ENGINE=InnoDB DEFAULT CHARSET=latin1")
    cursor.execute("CREATE TABLE `tbl_kategori` (`id_kategori` varchar(50) NOT NULL,`kategori` varchar(50) NOT NULL ) ENGINE=InnoDB DEFAULT CHARSET=latin1;")
    conn.commit()
    conn.close()

# redirect_if_loggedin
def redirect_if_loggedin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('index'))
    return wrap

# membatasi sesi login user
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

# ===============


mysql = MySQL(app)
# =============================================
# Routing Homepage ============================
# =============================================
@app.route('/')
@login_required
def homepage():
    if 'username' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # num rows in table buku
        cursor.execute('SELECT * FROM tbl_buku')
        num_rows = cursor.rowcount
        # fetch all rows from table buku
        num_buku = cursor.fetchall()
        # if login = True then show flash message and redirect to homepage
        if 'login' in session:
            flash('Anda sudah login')
            return redirect(url_for('homepage'))
        # if not login then show homepage
        return render_template('index.html', num_rows=num_rows, num_buku=num_buku)
    else:
        flash('Anda harus login terlebih dahulu')
        return redirect(url_for('login'))


# =============================================
# Routing Login ===============================
# =============================================
# limit user login session
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get form data
        username = request.form['username']
        password = request.form['password']
        # create cursor
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # get user by username
        cursor.execute('SELECT * FROM tbl_user WHERE username = %s', [username])
        # fetch one row
        user = cursor.fetchone()
        # if user not found
        if user is None:
            flash('Username tidak ditemukan')
            return redirect(url_for('login'))
        # if user found
        if user['password'] != md5(password.encode('utf-8')).hexdigest():
            flash('Password salah')
            return redirect(url_for('login'))
        # if user found and password is correct
        session['logged_in'] = True
        session['nama'] = user['nama']
        session['address'] = user['address']
        session['username'] = user['username']
        session['email'] = user['email']
        session['id_user'] = user['id_user']
        flash('Selamat datang ' + session['nama'])
        return redirect(url_for('homepage'))
    return render_template('login.html')

# =============================================
# Routing Logout ==============================
# =============================================

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))

# =============================================
# Routing Register ============================
# =============================================

@app.route('/register', methods =['GET', 'POST'])
def register():
    if 'username' not in session:
        if request.method == 'POST' and 'nama' in request.form and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form:
            nama = request.form['nama']
            username = request.form['username']
            password = md5(request.form['password'].encode('utf-8')).hexdigest()
            email = request.form['email']
            address = request.form['address']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM tbl_user WHERE username = % s', (username, ))
            account = cursor.fetchone()
            if account:
                flash('Account already exists !')
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('Invalid email address !')
            elif not re.match(r'[A-Za-z0-9]+', username):
                flash('name must contain only characters and numbers !')
            else:
                cursor.execute('INSERT INTO tbl_user VALUES (NULL, % s, % s, % s, % s, % s )', (nama, username, password, email, address ))
                mysql.connection.commit()
                flash('You have successfully registered !')
        elif request.method == 'POST':
            flash( 'Please fill out the form !')
        return render_template('register.html')
    if 'logged_in' in session:
        return redirect(url_for('homepage'))
    return render_template('register.html')
  
# =============================================
# Routing buku ================================
# =============================================
@app.route('/buku')
def buku():
    if 'username' in session:
        page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
        total = get_total_buku()
        pagination_books = get_books(offset=offset, per_page=per_page)
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap3')
        ctgs = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        ctgs.execute('SELECT * FROM tbl_kategori')
        ctg = ctgs.fetchall()
        return render_template('buku.html',buku=pagination_books,page=page,per_page=10,pagination=pagination, ctg=ctg)
    else:
        flash('Anda harus login terlebih dahulu')
        return redirect(url_for('login'))

def get_total_buku():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM tbl_buku')
    return cursor.rowcount

# Create Search Function
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        book = request.form['book']
        # search by judul, pengarang, penerbit, tahun terbit, penerbit, kategori
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        ctgs = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tbl_buku WHERE judul LIKE %s OR pengarang LIKE %s OR penerbit LIKE %s OR tahun_terbit LIKE %s OR penerbit LIKE %s OR kategori LIKE %s OR tempat_terbit LIKE %s', ('%'+book+'%', '%'+book+'%', '%'+book+'%', '%'+book+'%', '%'+book+'%', '%'+book+'%', '%'+book+'%'))
        ctgs.execute('SELECT * FROM tbl_kategori')
        books = cursor.fetchall()
        categories = ctgs.fetchall()
        # all in the search box will return all the tuples
        if len(books) == 0 and book == 'all':
            cursor.execute('SELECT * FROM tbl_buku')
            ctgs.execute('SELECT * FROM tbl_kategori')
            categories = ctgs.fetchall()
            books = cursor.fetchall()
        return render_template('search.html', books=books, categories=categories)
    else:
        return redirect(url_for('buku'))
   

@app.route('/add_book',methods=['POST'])
@login_required
def add_book():
    if 'username' in session:
        model = pickle.load(open('model.pkl', 'rb'))
        tfidf_model = pickle.load(open('tfidf_vectorizer.pkl', 'rb'))
        if request.method == 'POST':
            judul = request.form['judul']
            penerbit = request.form['penerbit']
            tempat_terbit = request.form['tempat_terbit']
            pengarang = request.form['pengarang']
            tahun_terbit = request.form['tahun_terbit']
            data1 = [judul + penerbit + tempat_terbit + pengarang]
            vect = tfidf_model.transform(data1)
            my_predict = model.predict(vect)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO tbl_buku VALUES (NULL, % s, % s, % s, % s, % s, % s )', (judul, penerbit, tahun_terbit, tempat_terbit, pengarang, my_predict[0] ))
            mysql.connection.commit()
            flash(message = 'Buku berhasil ditambahkan' + ' kedalam kategori ' + my_predict[0].upper())
        elif request.method == 'POST':
            flash('Isi form dengan benar !')
        return redirect(url_for('buku', prediction = my_predict))
    else :
        flash('Anda harus login terlebih dahulu')
        return redirect(url_for('login'))

# update book
@app.route('/update_book', methods=['GET', 'POST'])
def update_book():
    if 'username' in session:
        data = pd.read_csv('data buku.csv',encoding='latin-1')
        
        data['everything'] = pd.DataFrame(data['Judul'] + ' ' + data['Penerbit'] + ' ' + data['Tempat Terbit'] + ' ' + data['Pengarang'])
        tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        tfidf_buku_bersih = tfidf_vectorizer.fit_transform(data['everything'])
        
        smote = SMOTE()
        X_train_smote, y_train_smote = smote.fit_resample(tfidf_buku_bersih, data['Tipe Koleksi'])
        x_train  , x_test, y_train, y_test =train_test_split(tfidf_buku_bersih, data['Tipe Koleksi'], test_size=0.15 ,random_state=80)

        clf = MultinomialNB()
        clf.fit(X_train_smote,y_train_smote)
        
        if request.method == 'POST':
            id_buku = request.form['id_buku']
            judul = request.form['judul']
            penerbit = request.form['penerbit']
            tempat_terbit = request.form['tempat_terbit']
            pengarang = request.form['pengarang']
            tahun_terbit = request.form['tahun_terbit']
            data1 = [judul + penerbit + tempat_terbit + pengarang]
            vect = tfidf_vectorizer.transform(data1)
            my_predict = clf.predict(vect)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # account = cursor.fetchone()
            cursor.execute('UPDATE tbl_buku SET judul = % s, penerbit = % s, tahun_terbit = % s, tempat_terbit = % s, pengarang = % s, kategori = % s WHERE id_buku = % s', (judul, penerbit, tahun_terbit, tempat_terbit, pengarang, my_predict[0], id_buku))
            mysql.connection.commit()
            flash('Buku berhasil diubah'+ ' kedalam kategori ' + my_predict[0])
        elif request.method == 'POST':
            flash('Isi form dengan benar !')
        return redirect(url_for('buku', prediction = my_predict))
    else :
        flash('Anda harus login terlebih dahulu')
        return redirect(url_for('login'))

# update kategori
@app.route('/update_kategori', methods=['GET', 'POST'])
def update_kategori():
    if 'username' in session:
        if request.method == 'POST':
            id_buku = request.form['id_buku']
            judul = request.form['judul']
            penerbit = request.form['penerbit']
            tempat_terbit = request.form['tempat_terbit']
            pengarang = request.form['pengarang']
            tahun_terbit = request.form['tahun_terbit']
            kategori = request.form['kategori']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # account = cursor.fetchone()
            cursor.execute('UPDATE tbl_buku SET judul = % s, penerbit = % s, tahun_terbit = % s, tempat_terbit = % s, pengarang = % s, kategori = % s WHERE id_buku = % s', (judul, penerbit, tahun_terbit, tempat_terbit, pengarang, kategori, id_buku))
            mysql.connection.commit()
            flash('Kategori berhasil diubah')
        elif request.method == 'POST':
            flash('Isi form dengan benar !')
        return redirect(url_for('buku'))
    else :
        flash('Anda harus login terlebih dahulu')
        return redirect(url_for('login'))
    
# hapus data buku
@app.route("/delete_buku", methods =['GET', 'POST'])
@login_required
def delete_buku():
    if 'username' in session:
        if request.method == 'POST' and 'id_buku' in request.form:
            id_buku = request.form['id_buku']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('DELETE FROM tbl_buku WHERE id_buku = % s', (id_buku, ))
            mysql.connection.commit()
            flash('Buku berhasil dihapus')
            return redirect(url_for('buku'))
        return redirect(url_for('buku'))
    else :
        flash('Anda harus login terlebih dahulu')
        return redirect(url_for('login'))

# =============================================
# Routing Model ===============================
# =============================================

@app.route('/model')
@login_required
def model():
    if 'username' in session:
        return render_template('model.html')
    else :
        flash('Anda harus login terlebih dahulu')
        return redirect(url_for('login'))
    
@app.route("/api")
@login_required
def api():
    data = {}
    csvs = [row for row in csv.reader(open('model.csv', 'r', encoding='utf-8'))]
    data['data'] = csvs
    return jsonify(data)

# create model
@app.route('/model/hasil', methods =['GET', 'POST'])
@login_required
def hasil():
   if 'username' in session:
        if request.method == 'GET':
            return render_template('model.html')
        elif request.method == 'POST':
            model = pickle.load(open('model.pkl', 'rb'))
            tfidf_model = pickle.load(open('tfidf_vectorizer.pkl', 'rb'))
            xlsx_file = request.files['xlsx_file']
            X_test = pd.read_excel(xlsx_file)
            X_test_tfidf = X_test['Judul'] + ' ' + X_test['Penerbit'] + ' ' + X_test['Tempat Terbit'] + ' ' + X_test['Pengarang']
            tfidf = tfidf_model.transform(X_test_tfidf)
            pred = model.predict(tfidf)
            X_test['prediksi'] = pred
            # model.fit(tfidf,pred)
            df = pd.DataFrame(X_test)
            df.columns = ['judul', 'penerbit', 'tahun_terbit', 'tempat_terbit', 'pengarang','prediksi']
            # df.to_excel(r'model.xlsx', index = False, header=True)
            df.to_csv(r'model.csv', index = False, header=True)
            # upload to mysql database
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            data = pd.read_csv (r'model.csv')
            for raw in data.itertuples():
                cursor.execute('INSERT INTO tbl_buku VALUES (NULL, % s, % s, % s, % s, % s, % s)',
                               (raw.judul, raw.penerbit, raw.tahun_terbit, raw.tempat_terbit, 
                                raw.pengarang, raw.prediksi))
            mysql.connection.commit()
            flash('Data Berhasil Di Simpan')
            
            # flash('Tingkat Akurasi Yang Dihasilkan Adalah: {:.2f}'.format(model.score(tfidf, X_test['tipe_koleksi'])))
            # print('Classification report for testing data :-')
            # print(classification_report(X_test['tipe_koleksi'], pred))
            # print('confussion matrix = ')
            # print(confusion_matrix(X_test['tipe_koleksi'], pred))
            return redirect(url_for('model'))
        else :
            flash('Anda harus login terlebih dahulu')
            return redirect(url_for('login'))

@app.route('/buku/download')
def master_data():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT judul, penerbit, tahun_terbit, tempat_terbit, pengarang, kategori FROM tbl_buku')
    result = cursor.fetchall()
    
    #output in bytes
    output = io.BytesIO()
    #create WorkBook object
    workbook = xlwt.Workbook()
    #add a sheet
    sh = workbook.add_sheet('Books Report')
    
    #add headers
    sh.write(0, 0, 'Judul')
    sh.write(0, 1, 'Penerbit')
    sh.write(0, 2, 'Tahun Terbit')
    sh.write(0, 3, 'Tempat Terbit')
    sh.write(0, 4, 'Pengarang')
    sh.write(0, 5, 'Kategori')
    
    idx = 0
    for row in result:
        sh.write(idx+1, 0, row['judul'])
        sh.write(idx+1, 1, row['penerbit'])
        sh.write(idx+1, 2, str(row['tahun_terbit']))
        sh.write(idx+1, 3, row['tempat_terbit'])
        sh.write(idx+1, 4, row['pengarang'])
        sh.write(idx+1, 5, row['kategori'])
        idx += 1
    
    workbook.save(output)
    output.seek(0)
    
    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=master_data_buku.xls"})

@app.route('/model/template')
def template():
    #output in bytes
    output = io.BytesIO()
    #create WorkBook object
    workbook = xlwt.Workbook()
    #add a sheet
    sh = workbook.add_sheet('Books Report')
    
    #add headers
    sh.write(0, 0, 'Judul')
    sh.write(0, 1, 'Penerbit')
    sh.write(0, 2, 'Tahun Terbit')
    sh.write(0, 3, 'Tempat Terbit')
    sh.write(0, 4, 'Pengarang')
    
    workbook.save(output)
    output.seek(0)
    
    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=template data buku baru.xls"})


if __name__ == '__main__':
    app.run(debug=True)