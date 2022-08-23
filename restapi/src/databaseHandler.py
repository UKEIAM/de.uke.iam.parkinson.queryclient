import psycopg2, datetime

def count_entries(cursor):
    cursor.execute("SELECT COUNT(*) FROM printjobs")
    return cursor.fetchone()[0]

def initialize_statements(cursor):
    cursor.execute(
        "DO $$ "
        "BEGIN "
        "IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'status') THEN "
        "CREATE TYPE status AS ENUM ('open', 'processed'); "
        "END IF; "
        "END$$;")

    cursor.execute("CREATE TABLE IF NOT EXISTS printjobs ("
                   "id SERIAL PRIMARY KEY,"
                   "surname VARCHAR (200),"
                   "givenname VARCHAR (200),"
                   "birthday DATE,"
                   "logisticsID INTEGER,"
                   "medicationname VARCHAR (200),"
                   "dose VARCHAR (50),"
                   "unit VARCHAR (50),"
                   "medicationtimestamp TIMESTAMP,"
                   "ward VARCHAR(200),"
                   "printstatus status DEFAULT 'open');")

def initialize_db():
    # Connect to an existing database
    connection = psycopg2.connect(user="qcuser",
                                  password="qcpassword",
                                  host="qc_database",
                                  port="5432",
                                  database="printjobs")

    # Create a cursor to perform database operations
    cursor = connection.cursor()

    initialize_statements(cursor)

    connection.commit()

    return connection, cursor

def insert_job(cursor, record):
    cursor.execute(
        "INSERT INTO printjobs (surname,"
        "givenname,"
        "birthday,"
        "logisticsID,"
        "medicationname,"
        "dose,"
        "unit,"
        "medicationtimestamp,"
        "ward) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;",(
            record['surname'],
            record['givenName'],
            datetime.datetime.strptime(record['birthday'], '%Y-%m-%d'),
            int(record['logisticsID']),
            record['medicationName'],
            record['medicationDose'],
            record['medicationUnit'],
            datetime.datetime.strptime(record['medicationTimestamp'], '%Y-%m-%d %H:%M:%S'),
            record['hospitalWard']))

    result = cursor.fetchone()
    if len(result) == 0:
        return -1
    return result[0]

def get_open_jobs(cursor):
    cursor.execute("SELECT * FROM printjobs WHERE printstatus = 'open';")
    result = []
    for row in cursor.fetchall():
        row_result = {
            'id' : row[0],
            'surname' : row[1],
            'givenName' : row[2],
            'birthday': row[3].strftime('%Y-%m-%d'),
            'logisticsID' : row[4],
            'medicationName' : row[5],
            'medicationDose' : row[6],
            'medicationUnit' : row[7],
            'medicationTimeStamp': row[8].strftime('%Y-%m-%d %H:%M:%S'),
            'hospitalWard' : row[9]
        }
        result.append(row_result)
    return result

def mark_job_processed(cursor, id):
    cursor.execute("UPDATE printjobs SET printstatus = 'processed' WHERE id = " + str(id) + ' RETURNING id;')
    result = cursor.fetchone()
    if result is None or len(result) == 0 or result[0] != id:
        print(result)
        print('ID ' + str(id) + ' not found in database')
        return False
    return True

def remove_job(cursor, id):
    cursor.execute("DELETE FROM printjobs WHERE id = " + str(id) + ' RETURNING id;')
    result = cursor.fetchone()
    if result is None or len(result) == 0 or result[0] != id:
        print(result)
        print('ID ' + str(id) + ' not found in database')
        return False
    return True