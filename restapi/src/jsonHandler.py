import datetime

def check_type(val, convert_func):
    try:
        convert_func(val)
        return True
    except ValueError:
        return False

def check_date(val):
    str(val)
    datetime.datetime.strptime(val , '%Y-%m-%d')

def check_timestamp(val):
    str(val)
    datetime.datetime.strptime(val , '%Y-%m-%d %H:%M:%S')

parameter_dict = {
    'surname' : (str, 'string'),
    'givenName' : (str, 'string'),
    'birthday' : (check_date, 'valid date string in the form YYYY-MM-DD'),
    'logisticsID' : (int, 'integer'),
    'medicationName' : (str, 'string'),
    'medicationDose' : (str, 'string'),
    'medicationUnit' : (str, 'string'),
    'medicationTimestamp' : (check_timestamp, 'valid timestamp string in the form YYYY-MM-DD HH:MM:SS'),
    'hospitalWard' : (str, 'string'),
}

def check_key(record_json, key):
    return key in record_json and check_type(record_json[key], parameter_dict[key][0])

def check_validity(record_json):
    for key in parameter_dict.keys():
        if not check_key(record_json, key):
            return False, "you have to provide the entry " + key + " as a " + parameter_dict[key][1]
    return True, "json valid"
