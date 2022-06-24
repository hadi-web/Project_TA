import os
import psycopg2

conn = psycopg2.connect(
        host="ec2-44-206-89-185.compute-1.amazonaws.com",
        database="dct53dh5u7jt4m",
        user="ixvwirkbsvzgoh",
        password="6c185f67f72bc6cd19631e8d98e3955a647a469af0318626d54cecccebff4f32")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS books;')
cur.execute('CREATE TABLE books (id serial PRIMARY KEY,'
                                 'judul varchar (250) NOT NULL,'
                                 'penerbit varchar (50) NOT NULL,'
                                 'tahun_terbit integer NOT NULL,'
                                 'tempat_terbit varchar (150) NOT NULL,'
                                 'pengarang varchar (250) NOT NULL,'
                                 'kategori varchar (50) NOT NULL);'
                                 )

cur.execute('DROP TABLE IF EXISTS users;')
cur.execute('CREATE TABLE users (id serial PRIMARY KEY,'
                                 'nama varchar (250) NOT NULL,'
                                 'username varchar (50) NOT NULL,'
                                 'password integer NOT NULL,'
                                 'email varchar (150) NOT NULL);'
                                 )

# Insert data into the table


conn.commit()

cur.close()
conn.close()