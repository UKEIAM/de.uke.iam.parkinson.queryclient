import datetime

def check_type(val: str, convert_func) -> bool:
    """
    Checks if a string can be casted given a specified conversion function

    :param val: the string that should be converted
    :param convert_func: the conversion function used for casting
    :return: Return true if the string can be casted
    """
    try:
        convert_func(val)
        return True
    except ValueError:
        return False

def check_date(val: str) -> None:
    """
    Checks if a string is a date in valid format

    :param val: the input string
    """
    datetime.datetime.strptime(val , '%Y-%m-%d')

def check_timestamp(val: str) -> None:
    """
    Checks if a string is a time stamp in valid format

    :param val: the input string
    """
    datetime.datetime.strptime(val , '%Y-%m-%d %H:%M')

parameters = [
    ('surname', str, 'the surname as string'),
    ('givenName',str, 'the given name as string'),
    ('birthday', check_date, 'the birthday as valid date string in the form YYYY-MM-DD'),
    ('caseID', int, 'the case ID as integer'),
    ('hospitalWard', str, 'the hospital ward as string'),
    ('logisticsID', str, 'the logistics ID as a string'),
    ('medicationName', str, 'the medication name as string'),
    ('medicationDose', float, 'the medication dose as decimal'),
    ('medicationTimeStamp', check_timestamp, 'the medication time stamp as valid timestamp string in the form '
                                             'YYYY-MM-DD HH:MM')
]

def check_validity(record_json) -> (bool, str, dict):
    """
    Transforms the data string with pipes to a dict and checks the validity of all entries

    :param record_json: The JSON retrieved from the PUT request
    :return:
    """
    if 'dataString' not in record_json.keys():
        return False, "you have to provide the key 'dataString' following the print string", {}
    data_string = record_json['dataString']
    fields = data_string.split('|')
    if len(fields) != 9:
        return False, "you have to provide 9 fields in the print string, seperated by '|' characters", {}
    result = {}
    for idx in range(len(fields)):
        key, check, error_string = parameters[idx]
        field = fields[idx]
        if not check_type(field, check):
            return False, "at the " + str(idx+1) + "th field you have to provide " + error_string, {}
        result[key] = field
    return True, "data string valid", result
