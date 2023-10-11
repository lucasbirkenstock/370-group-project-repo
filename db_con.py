#Needed for postgres
#import psycopg2 

#Use sqllite
import sqlite3


def get_db():
    #Postgres
    #return psycopg2.connect(host="localhost", dbname="authme" , user="loki", password="4prez")
    return sqlite3.connect("local_data_base.db")

def get_db_instance():  
    db  = get_db()
    theCursor  = db.cursor()

    return db, theCursor 

def video_db_setup():
    db, theCursor = get_db_instance()
    theCursor.execute("CREATE TABLE example (asdf int, abc int)")

if __name__ == "__main__":
    db, theCursor = get_db_instance()

    video_db_setup()
    theCursor.execute("INSERT INTO example (asdf, abc) VALUES (5, 2)")
    
    #cur.execute("select * from users")
    for r in theCursor.fetchall():
       print(r)

    db.commit()




