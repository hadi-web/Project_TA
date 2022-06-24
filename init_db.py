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
                                 'kategori varchar (50) NOT NULL,'
                                 'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                 )

# Insert data into the table

cur.execute('INSERT INTO books (judul, penerbit, tahun_terbit, tempat_terbit, pengarang, kategori)'
            'VALUES (%s, %s, %s, %s, %s, %s, %s)',
            ('Pendidikan Agama Islam',
             'Noura Books',
             2004,
             'Jakarta',
             'Wahyudin, Achmad, M.Ilyas, M.Saifullah'
             'umum')
            )


conn.commit()

cur.close()
conn.close()