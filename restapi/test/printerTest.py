import sys, asyncio, pytest
sys.path.append('../src')
import printHandler, inputHandler

record_json = {
    "dataString":"Apfel|Anna|1967-08-08|12348|Station 2|Medi0815|Ibu 400|10.3|2022-09-09 11:08"
}

def test_label_printer():
    """
    This test should fail, because the label printer is not attached
    """
    ok, msg, record = inputHandler.check_validity(record_json)
    assert ok
    # id is normally set by database, have to set it manually here
    record['id'] = 42
    label_ok = printHandler.print_label(record)
    assert not label_ok

def test_medication_printer():
    """
        This test passes, when the medication printer 'MedicationPrinter' was added on the Repetier server,
        but was not installed. Additionally a G-Code file was uploaded and assigned the name "Test"
    """
    av_str = asyncio.get_event_loop().run_until_complete(printHandler.check_if_medication_printer_available())
    assert av_str == 'MedicationPrinter not online'
    # G-Code with name "Test" was uploaded
    test_id = asyncio.get_event_loop().run_until_complete(printHandler.get_model_id('Test'))
    assert test_id == 1
    # G-Code with name "LogisticsID" does not exist
    log_id = asyncio.get_event_loop().run_until_complete(printHandler.get_model_id('LogisticsID'))
    assert  log_id == -1
    print_str = asyncio.get_event_loop().run_until_complete(printHandler.print_dose(record_json))
    assert print_str == 'MedicationPrinter not online'



if __name__ == '__main__':
    pytest.main(['printerTest.py'])