from flask import Flask, request, session, redirect, jsonify
from flask_cors import CORS
import oracledb

app = Flask(__name__)
CORS(app)

cs = '''(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1521)
(host=adb.us-ashburn-1.oraclecloud.com))(connect_data=(service_name=g4ce17c11a5179b_helloadventuredb_low.adb.oraclecloud.com))
(security=(ssl_server_dn_match=yes)))'''

conn = oracledb.connect(
    user="admin",
    password="Helloadventure123!",
    dsn=cs)  # the connection string copied from the cloud console

@app.route('/verifyRegistration', methods=["GET", "POST"])
def verifyRegistration():
    data = request.get_json()
    account_type = data['account-type']

    if account_type == "admin":
        email = request.form['email']
        user_name = request.form['username']
        password = request.form['password']
        student_group = request.form['student-group']

        # Check if the account already exists
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM admin WHERE email =: temp', temp = email)
        data = cursor.fetchone()
        error = None

        if (data):
            # If the previoud query returns data, then user exists
            error = "This user has already exists"
            return jsonify({
                "result": "FAIL",
                "message": "Admin already exists"
            })

        else:  # Succeed

            cursor.execute('INSERT INTO admin (EMAIL, USERNAME, PASSWORD, STUDENT_GROUP) '
                           'VALUES(:email, :username, :password, :student_group)',
                           [email,user_name, password, student_group] )
            conn.commit()
            cursor.close()
            return jsonify({
                "result": "SUCCEED",
            })

    elif account_type == "student":
        email = request.form['email']
        user_name = request.form['username']
        password = request.form['password']
        student_group = request.form['student-group']

        # Check if the account already exists
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM student WHERE email =: temp', temp=email)
        data = cursor.fetchone()
        error = None

        if (data):
            # If the previous query returns data, then user exists
            error = "This user has already exists"
            return jsonify({
                "result": "FAIL",
                "message": "Student already exists"
            })

        else:  # Succeed

            cursor.execute('INSERT INTO student (EMAIL, USERNAME, PASSWORD, STUDENT_GROUP, PROGRESS) '
                           'VALUES(:email, :username, :password, :student_group, null)',
                           [email, user_name, password, student_group])
            conn.commit()
            cursor.close()
            return jsonify({
                "result": "SUCCEED",
            })

    elif account_type == "guest":
        email = request.form['email']
        user_name = request.form['username']
        password = request.form['password']

        # Check if the account already exists
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM guest WHERE email =: temp', temp=email)
        data = cursor.fetchone()
        error = None

        if (data):
            # If the previous query returns data, then user exists
            error = "This user has already exists"
            return jsonify({
                "result": "FAIL",
                "message": "Guest user already exists"
            })

        else:  # Succeed

            cursor.execute('INSERT INTO guest (EMAIL, USERNAME, PASSWORD, PROGRESS) '
                           'VALUES(:email, :username, :password, null)',
                           [email, user_name, password])
            conn.commit()
            cursor.close()
            return jsonify({
                "result": "SUCCEED",
            })


@app.route('/verifyLogin', methods=["GET", "POST"])
def verifyLogin():
    data = request.get_json()
    account_type = data['account-type']
    username = request.form['username']
    password = request.form['password']

    if account_type == "admin":
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM admin WHERE email =: email and password =: password', [username, password])
        data = cursor.fetchone()
        error = None
        cursor.close()

        if (data):

            return jsonify({}), 200
        else:
            error = "Invalid username or password"
            return jsonify({}), 409

    elif account_type == "student":
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM student WHERE email =: email and password =: password', [username, password])
        data = cursor.fetchone()
        error = None
        cursor.close()

        if (data):

            return jsonify({}), 200
        else:
            error = "Invalid username or password"
            return jsonify({}), 409

    elif account_type == "guest":
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM admin WHERE email =: email and password =: password', [username, password])
        data = cursor.fetchone()
        error = None
        cursor.close()

        if (data):

            return jsonify({}), 200
        else:
            error = "Invalid username or password"
            return jsonify({}), 409


@app.route('/logout', methods=["GET", "POST"])
def logout():
    # TODO: Destroy all session variables
    session.pop('username')
    # redirect
    return jsonify({})


@app.route('/getAssignments', methods=["GET"])
def getAssignments():
    # Get class assignments
    # TODO: Add query for getting assignments

    assignments = [f'Assignment {i+1}' for i in range(3)]

    return jsonify({
        'assignments': assignments,
    })

@app.route('/getStudents', methods=["GET"])
def getStudents():
    # Get class students
    # TODO: Add query for getting students

    students = [
            {
                'name': f'Student {i}',
                'username': f'Username{i}'
            }
            for i in range(1,11)
        ]

    return jsonify({
        'students': students
    })

@app.route('/getAccountType', methods=["GET"])
def getAccountType():
    # Get account type
    # TODO: Check session for account type

    account_type = 'NONE'

    return jsonify({'account-type':account_type})

@app.route('/getAssignmentDetails', methods=["GET"])
def getAssignmentDetails():
    # GET args
    assignment_title = request.args.get('assignment')
    
    # Get assignment description and date
    # TODO: Check if signed in as a student or admin
    # TODO: Add a query for getting the assignment details
    assignment_description = "Just an assignment, nothing to see here"
    assignment_date = "2023-05-04"
    assignment_world = 1
    assignment_level = 2
    return jsonify({
        'title': assignment_title,
        'description': assignment_description,
        'date': assignment_date,
        'world': assignment_world,
        'level': assignment_level
    })

@app.route('/updateAssignment', methods=["GET", "POST"])
def updateAssignment():
    if(request.method == 'POST'):
        data = request.get_json()
        title, description, date = data['title'], data['description'], data['date']
        world, level = data['world'], data['level']


        # Update the assignment
        # TODO: Add query to update database at assignment title

    return jsonify({})


@app.route('/createAssignment', methods=["GET", "POST"])
def createAssignment():
    data = request.get_json()
    title, description, date = data['title'], data['description'], data['date']
    world, level = data['world'], data['level']

    # Check if the assignment title already exists
    check = True

    # Create the assignment
    # TODO: Add query to create new assignment
    if check:   # Success
        # TODO: Compile relevant information into dictionary
        return jsonify({}), 200
    else:       # Failure
        # TODO: Compile relevant information into dictionary
        return jsonify({}), 409


@app.route('/getProfile', methods=["GET"])
def getProfile():
    # TODO: Get the account type from the session
    # TODO: Get the username from the session
    account_type = 'STUDENT'
    username = 'Username123'

    if account_type == 'STUDENT':
        # Get the account details
        # TODO: Add a query to query profile information from students
        name = "Student name 123"
        email = "Student email 456"
        bio = "Student bio 789"
    elif account_type == 'ADMIN':
        # Get the account details
        # TODO: Add a query to query profile information from admins
        name = "Admin name 123"
        email = "Admin email 456"
        bio = "Admin bio 789"
    else:
        # Get the account details
        # TODO: Add a query to query profile information from guests
        name = "Guest name 123"
        email = "Guest email 456"
        bio = "Guest bio 789"
    
    details = {
        'username': username,
        'name': name,
        'email': email,
        'bio': bio
    }

    return jsonify(details)


@app.route('/updateProfile', methods=['GET', 'POST'])
def updateProfile():
    # TODO: Get the account type from the session
    # TODO: Get the username from the session
    account_type = 'ADMIN'
    username = 'Username123'

    data = request.get_json()
    name, email, bio = data['name'], data['email'], data['bio']

    if account_type == 'STUDENT':
        # Get the account details
        # TODO: Add a query to update profile information from students
        pass
    elif account_type == 'ADMIN':
        # Get the account details
        # TODO: Add a query to update profile information from admins
        pass
    else:
        # Get the account details
        # TODO: Add a query to update profile information from guests
        pass
    
    return jsonify({})


@app.route("/deleteAccount", methods=["GET", "DELETE"])
def deleteAccount():
    # TODO: Get the account type from the session
    # TODO: Get the username from the session
    account_type = 'ADMIN'
    username = 'Username123'

    if account_type == 'ADMIN':
        # TODO: Change all students under this admin to guest accounts

        # TODO: Delete this account from admin table
        pass
    elif account_type == 'GUEST':
        # TODO: Delete this account from guest table
        pass

    # TODO: Destroy all session variables

    return jsonify({})

@app.route("/getStudentInformation", methods=["GET"])
def getStudentInformation():
    # GET args
    student_username = request.args.get('username')

    # Get student information 
    # TODO: Add a query to get student details
    name = 'Johnathan Dope'
    email = 'johnnydoe11@gmail.com'
    bio = 'Hey, this is my super cool bio!'

    # Get all completed assignments
    # TODO: Add a query that gets all assignment titles completed by this student
    assignments = [f'Assignment {i}' for i in range(1,4)]

    return jsonify({
        'username': student_username,
        'name': name,
        'email': email,
        'bio': bio,
        'assignments': assignments
    })

@app.route("/dropStudent", methods=["GET", "POST"])
def dropStudent():
    data = request.get_json()
    student_username = data['username']

    # Move student account to guest account
    # TODO: Add a query to create a new guest account

    # Delete the old student account
    # TODO: Add a query to delete the old student account

    return jsonify({})


app.secret_key = 'some other random key'


if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)