from flask import Flask, jsonify, request
import pyodbc

app = Flask(__name__)

# Database connection setup
server = 'DESKTOP-VMJ10VF\\SQLEXPRESS'
database = 'Testing'  # Replace with your actual database name
username = 'zaki'
password = '12365'


# Create a connection to the SQL Server
def get_db_connection():
    connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    return connection


# -----------------------------------
# CRUD Operations for UserAuthentication Table
# -----------------------------------

@app.route('/auth', methods=['GET'])
def get_user_authentication():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM UserAuthentication')
    rows = cursor.fetchall()

    users = []
    for row in rows:
        user_auth = {
            'UAID': row.UAID,
            'Email': row.Email,
            'Username': row.Username,
            'PhoneNo': row.PhoneNo,
            'Created_on': row.Created_on,
            'Updated_on': row.Updated_on
        }
        users.append(user_auth)

    conn.close()
    return jsonify({'auth_users': users})


@app.route('/auth', methods=['POST'])
def register_user():
    data = request.get_json()
    email = data.get('Email')
    username = data.get('Username')
    password = data.get('Password')
    confirm_password = data.get('ConfirmPassword')
    phone = data.get('PhoneNo')

    # Check if the user already exists by email or username
    conn = get_db_connection()
    cursor = conn.cursor()
    user = cursor.execute('SELECT * FROM UserAuthentication WHERE Email = ? OR Username = ?',
                          (email, username)).fetchone()

    if user:
        # Return a 409 Conflict if the email or username is already registered
        return jsonify({'message': 'User with this email or username already exists'}), 409

    # Continue with registration logic (e.g., hashing password, saving user to the database)
    query = '''INSERT INTO UserAuthentication (Email, Username, Password, ConfirmPassword, PhoneNo, Created_on, Updated_on) 
               VALUES (?, ?, ?, ?, ?, GETDATE(), GETDATE())'''

    cursor.execute(query, (email, username, password, confirm_password, phone))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User registered successfully!'}), 201


@app.route('/auth/<int:uaid>', methods=['PUT'])
def update_user_authentication(uaid):
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    query = '''UPDATE UserAuthentication 
               SET Email = ?, Username = ?, PhoneNo = ?, Updated_on = GETDATE() 
               WHERE UAID = ?'''

    cursor.execute(query, (
        data['Email'],
        data['Username'],
        data.get('PhoneNo'),
        uaid
    ))

    conn.commit()
    conn.close()

    return jsonify({'message': 'User authentication record updated successfully!'})


@app.route('/auth/<email>', methods=['DELETE'])
def delete_user_authentication(email):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Use the email to delete the record
    cursor.execute('DELETE FROM UserAuthentication WHERE email = ?', (email,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User authentication record deleted successfully!'})


# -----------------------------------
# CRUD Operations for Users Table
# -----------------------------------

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Users')
    rows = cursor.fetchall()

    users = []
    for row in rows:
        user_data = {
            'UTID': row.UTID,
            'First_Name': row.First_Name,
            'Middle_Name': row.Middle_Name,
            'Last_Name': row.Last_Name,
            'Age': row.Age,
            'Country': row.Country,
            'City': row.City,
            'Anonymous_name': row.Anonymous_name,
            'Postal_Code': row.Postal_Code,
            'UAID': row.UAID,
            'Created_on': row.Created_on,
            'Updated_on': row.Updated_on
        }
        users.append(user_data)

    conn.close()
    return jsonify({'users': users})


@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    query = '''INSERT INTO Users (First_Name, Middle_Name, Last_Name, Age, Country, City, Anonymous_name, Postal_Code, UAID, Created_on, Updated_on) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE(), GETDATE())'''

    cursor.execute(query, (
        data['First_Name'],
        data.get('Middle_Name'),
        data['Last_Name'],
        data.get('Age'),
        data.get('Country'),
        data.get('City'),
        data.get('Anonymous_name'),
        data.get('Postal_Code'),
        data['UAID']  # Foreign key reference to UserAuthentication
    ))

    conn.commit()
    conn.close()

    return jsonify({'message': 'User added successfully!'})


@app.route('/users/<int:utid>', methods=['PUT'])
def update_user(utid):
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    query = '''UPDATE Users 
               SET First_Name = ?, Middle_Name = ?, Last_Name = ?, Age = ?, Country = ?, City = ?, Anonymous_name = ?, Postal_Code = ?, Updated_on = GETDATE()
               WHERE UTID = ?'''

    cursor.execute(query, (
        data['First_Name'],
        data.get('Middle_Name'),
        data['Last_Name'],
        data.get('Age'),
        data.get('Country'),
        data.get('City'),
        data.get('Anonymous_name'),
        data.get('Postal_Code'),
        utid
    ))

    conn.commit()
    conn.close()

    return jsonify({'message': 'User updated successfully!'})


@app.route('/users/<int:utid>', methods=['DELETE'])
def delete_user(utid):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM Users WHERE UTID = ?', (utid,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User deleted successfully!'})


# -----------------------------------
# CRUD Operations for UserProfileImage Table
# -----------------------------------

@app.route('/user-images', methods=['GET'])
def get_user_profile_images():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM UserProfileImage')
    rows = cursor.fetchall()

    images = []
    for row in rows:
        image_data = {
            'UPID': row.UPID,
            'Real_Image': row.Real_Image,
            'Hide_Image': row.Hide_Image,
            'UTID': row.UTID,
            'Created_on': row.Created_on,
            'Updated_on': row.Updated_on
        }
        images.append(image_data)

    conn.close()
    return jsonify({'user_images': images})


@app.route('/user-images', methods=['POST'])
def add_user_profile_image():
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    query = '''INSERT INTO UserProfileImage (Real_Image, Hide_Image, UTID, Created_on, Updated_on) 
               VALUES (?, ?, ?, GETDATE(), GETDATE())'''

    cursor.execute(query, (
        data['Real_Image'],
        data.get('Hide_Image'),
        data['UTID']  # Foreign key reference to Users
    ))

    conn.commit()
    conn.close()

    return jsonify({'message': 'User profile image added successfully!'})


@app.route('/user-images/<int:upid>', methods=['PUT'])
def update_user_profile_image(upid):
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    query = '''UPDATE UserProfileImage 
               SET Real_Image = ?, Hide_Image = ?, Updated_on = GETDATE() 
               WHERE UPID = ?'''

    cursor.execute(query, (
        data['Real_Image'],
        data.get('Hide_Image'),
        upid
    ))

    conn.commit()
    conn.close()

    return jsonify({'message': 'User profile image updated successfully!'})


@app.route('/user-images/<int:upid>', methods=['DELETE'])
def delete_user_profile_image(upid):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM UserProfileImage WHERE UPID = ?', (upid,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User profile image deleted successfully!'})


# -----------------------------------
# Combined Data from All Tables
# -----------------------------------

@app.route('/combined', methods=['GET'])
def get_combined_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = '''
    SELECT 
        ua.UAID, ua.Email, ua.Username, ua.PhoneNo, ua.Created_on AS Auth_Created_On, ua.Updated_on AS Auth_Updated_On,
        u.UTID, u.First_Name, u.Middle_Name, u.Last_Name, u.Age, u.Country, u.City, u.Anonymous_name, u.Postal_Code, u.Created_on AS User_Created_On, u.Updated_on AS User_Updated_On,
        up.UPID, up.Real_Image, up.Hide_Image, up.Created_on AS Image_Created_On, up.Updated_on AS Image_Updated_On
    FROM UserAuthentication ua
    LEFT JOIN Users u ON ua.UAID = u.UAID
    LEFT JOIN UserProfileImage up ON u.UTID = up.UTID
    '''

    cursor.execute(query)
    rows = cursor.fetchall()

    combined_data = []
    for row in rows:
        data = {
            'UAID': row.UAID,
            'Email': row.Email,
            'Username': row.Username,
            'PhoneNo': row.PhoneNo,
            'Auth_Created_On': row.Auth_Created_On,
            'Auth_Updated_On': row.Auth_Updated_On,
            'UTID': row.UTID,
            'First_Name': row.First_Name,
            'Middle_Name': row.Middle_Name,
            'Last_Name': row.Last_Name,
            'Age': row.Age,
            'Country': row.Country,
            'City': row.City,
            'Anonymous_name': row.Anonymous_name,
            'Postal_Code': row.Postal_Code,
            'User_Created_On': row.User_Created_On,
            'User_Updated_On': row.User_Updated_On,
            'UPID': row.UPID,
            'Real_Image': row.Real_Image,
            'Hide_Image': row.Hide_Image,
            'Image_Created_On': row.Image_Created_On,
            'Image_Updated_On': row.Image_Updated_On
        }
        combined_data.append(data)

    conn.close()
    return jsonify({'combined_data': combined_data})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
