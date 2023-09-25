import psycopg2

# To connect to "suppliers" database, use connection function of psycopg2.
# User postgres and password "password" are what happen to be my <Lucas'> credentials for pgAdmin.
conn = psycopg2.connect(
host="localhost",
database="brainbit",
user="postgres",
password="password"
)

theCursor = conn.cursor() 

# Return serial number from searching_device table
# TODO Make it print/store value in a variable
def getSerialNumber():
    theCursor.execute("SELECT SerialNumber FROM searching_device")

# Write to data table receiving_resistance as described here: https://pypi.org/project/pyneurosdk2/#receiving-signal
def writeToReceivingResistance(iO1, iO2, iT3, iT4):
    theCursor.execute("""INSERT INTO receiving_resistance ("O1", "O2", "T3", "T4") VALUES(%s, %s, %s, %s);
                      """, 
                      (iO1, iO2, iT3, iT4))

# Testing above function: functional
writeToReceivingResistance(0.1, 0.2, 0.3, 0.4)

# Ensure effects of any data manipulation are not lost
conn.commit()

# Close connections to the cursor and connection
theCursor.close()
conn.close()


