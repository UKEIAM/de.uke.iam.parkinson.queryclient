import psycopg2, datetime

def initialize_db():
    """
    Opens a connection the database, creates the table if it doesn't exist

    :return: Returns the connection and cursor objects
    """
    # Connect to an existing database
    connection = psycopg2.connect(user="qcuser",
                                  password="qcpassword",
                                  host="qc_database",
                                  port="5432",
                                  database="printjobs")

    # Create a cursor to perform database operations
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS printjobs ("
                   "id SERIAL PRIMARY KEY,"
                   "surname VARCHAR (200),"
                   "givenname VARCHAR (200),"
                   "birthday DATE,"
                   "caseid INTEGER,"
                   "ward VARCHAR(200),"
                   "logisticsID VARCHAR (200),"
                   "medicationname VARCHAR (200),"
                   "dose REAL,"
                   "medicationtimestamp TIMESTAMP);")

    connection.commit()

    return connection, cursor

def insert_job(cursor, record) -> int:
    """
    Inserts a print job into the database, generating an ID for it

    :param cursor: The database cursor used for insertion
    :param record: The record JSON of the print job to be inserted
    :return: Returns the generated ID of the inserted job
    """
    cursor.execute(
        "INSERT INTO printjobs (surname,"
        "givenname,"
        "birthday,"
        "caseid,"
        "ward,"
        "logisticsID,"
        "medicationname,"
        "dose,"
        "medicationtimestamp) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;",(
            record['surname'],
            record['givenName'],
            datetime.datetime.strptime(record['birthday'], '%Y-%m-%d'),
            int(record['caseID']),
            record['hospitalWard'],
            record['logisticsID'],
            record['medicationName'],
            record['medicationDose'],
            datetime.datetime.strptime(record['medicationTimeStamp'], '%Y-%m-%d %H:%M')))

    result = cursor.fetchone()
    if len(result) == 0:
        return -1
    return result[0]

def get_all_jobs(cursor) -> list:
    """
    Retrieves all print jobs contained in the database

    :param cursor: The database cursor used for retrieval
    :return: Returns a list of dicts, each containing the data for one print job
    """
    cursor.execute("SELECT * FROM printjobs;")
    result = []
    for row in cursor.fetchall():
        row_result = {
            'id' : row[0],
            'surname' : row[1],
            'givenName' : row[2],
            'birthday': row[3].strftime('%Y-%m-%d'),
            'caseID' : row[4],
            'hospitalWard' : row[5],
            'logisticsID' : row[6],
            'medicationName' : row[7],
            'medicationDose' : row[8],
            'medicationTimeStamp': row[9].strftime('%Y-%m-%d %H:%M')
        }
        result.append(row_result)
    return result

def get_job(cursor, id: int) -> dict:
    """
    Retrieves the job for the given ID if it exists in the database

    :param cursor: The database cursor used for retrieval
    :param id: The ID used to identify the print job
    :return: Returns dict containing the data for the print job. The dict is empty if the ID was invalid
    """
    cursor.execute("SELECT * FROM printjobs WHERE id = " + str(id) + ';')
    db_result = cursor.fetchall()
    if db_result is None or len(db_result) == 0:
        print('ID ' + str(id) + ' not found in database')
        return {}
    entry = db_result[0]
    return {
        'id' : entry[0],
        'surname' : entry[1],
        'givenName' : entry[2],
        'birthday': entry[3].strftime('%Y-%m-%d'),
        'caseID' : entry[4],
        'hospitalWard' : entry[5],
        'logisticsID' : entry[6],
        'medicationName' : entry[7],
        'medicationDose' : entry[8],
        'medicationTimeStamp': entry[9].strftime('%Y-%m-%d %H:%M')}


def remove_job(cursor, id: int) -> bool:
    """
    Removes the specified job from the database

    :param cursor: The database cursor used for removal
    :param id: The ID used to identify the print job
    :return: Returns true, if the ID was valid (and the job was deleted) and false otherwise
    """
    cursor.execute("DELETE FROM printjobs WHERE id = " + str(id) + ' RETURNING id;')
    result = cursor.fetchone()
    if result is None or len(result) == 0 or result[0] != id:
        print('ID ' + str(id) + ' not found in database')
        return False
    return True