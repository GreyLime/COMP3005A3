# Python libary used to communicate with postgres servers
import psycopg2

# This function creates a connection to the server using the provided server configuration/connection details
def connectToDB():
    try:
        # Creates the connection
        conn = psycopg2.connect(
            database='A3',
            user='postgres',
            password='password',
            host= 'localhost', 
            port='5432'
        )
        # returns the connection object
        return conn
    # handles error on connection failure
    except (Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database:", error)

# This function gets all student records with a select * query and prints them to the console.
def getAllStudents():
    conn = connectToDB()
    try:
        # checks if connection was successful
        if conn:
            # Creates a cursor object for the connection which allows SQL statements/requests to be made to the server
            # Cursor acts like a handler for the server connection.
            cursor = conn.cursor()
            # Execute the specified query on to the database server cursor
            cursor.execute("SELECT * FROM students")
            # Gets all the returned records
            rows = cursor.fetchall()
            # Prints the records
            print("All student records:")
            print(rows)
            print("\n") 
            # Closes the cursor and connection 
            cursor.close()
            conn.close()
    # handles error on query failure
    except (Exception, psycopg2.Error) as error:
        print("Error querying all student records from database. Error: ", error)

# This function adds the given student to the database
def addStudent(first_name, last_name, email, enrollment_date):
    # Creates connection to the server.
    conn = connectToDB()
    try:
        # checks if connection was successful
        if conn:
            # creates server connection cursor
            cursor = conn.cursor()
            # Executes the insertion statement to insert the passed in information into the students table for the servers staged changes
            cursor.execute("""
                INSERT INTO students (first_name, last_name, email, enrollment_date)
                VALUES (%s, %s, %s, %s)
                """, (first_name, last_name, email, enrollment_date)
            )
            # commits the current staged database changes to make the changes permament.
            conn.commit()
            # Closes down the cursor and server connection
            cursor.close()
            conn.close()
            print(f"Student {first_name} {last_name} added successfully.\n")
    # handles error upon insertion failure.
    except (Exception, psycopg2.Error) as error:
        print(f"Error adding student {first_name} {last_name} to database. Error: ", error)

# This function updates the specified student's email.
def updateStudentEmail(student_id, new_email):
    # Creates DB connection
    conn = connectToDB()
    try:
        # Checks if connection was successful
        if conn:
            # Creates cursor
            cursor = conn.cursor()
            # Executes the update sql command to update the specified student's ID to the given email in the server's staged changes
            cursor.execute("""
                UPDATE students 
                SET email = %s
                WHERE student_id = %s
            """, (new_email, student_id))

            # Commits the staged changes to the server permanantely.
            conn.commit()
            print(f"Email updated for student with ID {student_id}\n")

            # Closes down the cursor and connection to the server
            cursor.close()
            conn.close()
    # handles error upon update failure.
    except (Exception, psycopg2.Error) as error:
        print(f"Error updating student #{student_id}'s email. Error: ", error)

# This function deletes the specified student_id from the database
def deleteStudent(student_id):
    # Open connection to the server
    conn = connectToDB()
    try:
        # checks if the connection was successful
        if conn:
            # Creates a cursor/handler for the server connection
            cursor = conn.cursor()
            # Executes the Delete command to send it to the server's staged changes
            cursor.execute("""
                DELETE FROM students 
                WHERE student_id = %s
            """, (student_id,))  
            # commit the staged changes to make them permanent.
            conn.commit()
            print(f"Student with ID {student_id} deleted successfully.\n")

            # Close the cursor and server connection
            cursor.close()
            conn.close()
    # handles error upon deletion failure.
    except (Exception, psycopg2.Error) as error:
        print(f"Error deleting student #{student_id} from database. Error: ", error)

# Testing statements
getAllStudents()
addStudent('Liam', 'Letourneau', 'liam.letourneau@example.com', '2019-11-11') 
getAllStudents()
updateStudentEmail(4,"NEW.EMAIL@gmail.com")
getAllStudents()
deleteStudent(4)
getAllStudents()


