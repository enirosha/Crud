# app.py

from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL connection setup
db_config = {
    'user': 'root',  # Replace with your MySQL username
    'password': 'Admin@123',  # Replace with your MySQL password
    'host': 'localhost',  # Or the IP of the server hosting MySQL
    'database': 'flask_crud',  # The name of your database
}

# get_db_connection is the user defined function, to connet to database with respective user credentials
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection


# Route to the home page
@app.route('/')
def index():
    return render_template('index.html')


# Route to view all users
@app.route('/users')
def users():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users_list = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('users.html', users=users_list)


# Route to add a new user
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (username, email))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('users'))

    return render_template('add_user.html')


# Route to delete a user
@app.route('/delete_user/<int:id>')
def delete_user(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('users'))


# Route to edit a user (update)
@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    # Fetch the user to be edited
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if user is None:
        return redirect(url_for('users'))  # If the user doesn't exist, go back to the user list

    if request.method == 'POST':
        # Update user data
        username = request.form['username']
        email = request.form['email']

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET username = %s, email = %s WHERE id = %s", (username, email, id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('users'))

    return render_template('edit_user.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
