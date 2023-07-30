from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'student_records'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql_conn = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/add_record', methods=['POST', 'GET'])
def addRecord():
    if request.method == 'POST':
        # Get the form data
        fullname = request.form['fullname']
        midterm1 = request.form['midterm1']
        midterm2 = request.form['midterm2']
        finalexam = request.form['finalexam']

        # Insert the data into the records table
        cursor = mysql_conn.cursor()
        query = "INSERT INTO records (fullname, midterm1, midterm2, finalexam) VALUES (%s, %s, %s, %s)"
        values = (fullname, midterm1, midterm2, finalexam)
        cursor.execute(query, values)
        mysql_conn.commit()
        cursor.close()

        # Redirect to a success page or display a message
        return render_template('recordadded.html')
    else:
        # If it's a GET request, show the form
        return render_template('addrecord.html')


def fetch_records_as_dicts(cursor):
    columns = cursor.description
    result = [{columns[index][0]: column for index,
               column in enumerate(value)} for value in cursor.fetchall()]
    return result


@app.route('/all_records')
def displayRecords():

    cursor = mysql_conn.cursor()
    query = "SELECT fullname, midterm1, midterm2, finalexam FROM records"
    cursor.execute(query)
    records = fetch_records_as_dicts(cursor)

    for record in records:
        midterm1 = record['midterm1']
        midterm2 = record['midterm2']
        finalexam = record['finalexam']
        average_marks = (midterm1 + midterm2 + (2 * finalexam)) / 4
        record['average_marks'] = average_marks

    cursor.close()

    return render_template('displayrecords.html', records=records)


@app.route('/delete_record', methods=['POST', 'GET'])
def deleteRecord():
    if request.method == 'POST':
        # Get the fullname from the form data
        fullname_to_delete = request.form['fullname']

        # Delete the record from the records table
        cursor = mysql_conn.cursor()
        query = "DELETE FROM records WHERE fullname = %s"
        cursor.execute(query, (fullname_to_delete,))
        mysql_conn.commit()
        cursor.close()

        return render_template('recorddeleted.html')

    else:
        return render_template('deleterecord.html')


if __name__ == '__main__':
    app.run(debug=True)
