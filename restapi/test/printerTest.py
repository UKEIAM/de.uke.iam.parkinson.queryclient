import sys
sys.path.append('../src')
import printHandler, inputHandler

record_json = {
    "dataString":"Apfel|Anna|1967-08-08|12348|Station 2|Medi0815|Ibu 400|10.3|2022-09-09 11:08"
}

def test_label_printer():
    """
    This test should only be called if the label printer is actually attached
    """
    ok, msg, record = inputHandler.check_validity(record_json)
    assert ok
    # id is normally set by database, have to set it manually here
    record['id'] = 42
    label_ok = printHandler.print_label(record)
    assert label_ok

if __name__ == '__main__':
    test_label_printer()