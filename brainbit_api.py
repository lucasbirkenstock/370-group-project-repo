import psycopg2

# To connect to "suppliers" database, use connection function of psycopg2.
# User postgres and password "password" are what happen to be my <Lucas'> credentials for pgAdmin.
conn = psycopg2.connect(
host="localhost",
database="brainbit",
user="postgres",
password="password"
)

