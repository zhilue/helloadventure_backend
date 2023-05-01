import getpass
import oracledb

cs = '''(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1521)
(host=adb.us-ashburn-1.oraclecloud.com))(connect_data=(service_name=g4ce17c11a5179b_helloadventuredb_low.adb.oraclecloud.com))
(security=(ssl_server_dn_match=yes)))'''
connection = oracledb.connect(
    user="admin",
    password="Helloadventure123!",
    dsn=cs)  # the connection string copied from the cloud console

print("Successfully connected to Oracle Database")

# Create a table

# Now query the rows back
with connection.cursor() as cursor:
    temp1 = 'Task 1'
    temp2 = 0
    cursor.execute('select description, done from todoitem where description =: temp1 and done =: temp2', [temp1, temp2])
    data = cursor.fetchone()
    print(data)
    if(data):

        description = 'Task 6'
        done = 1
        cursor.execute('INSERT into TODOITEM(description, done) values(:description, :done)', [description, done])
        connection.commit()
        print('success')
    else:
        print("ERROR!")

