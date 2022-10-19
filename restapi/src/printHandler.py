import tempfile, os, websockets, json
import config
def generate_label_string(record: dict) -> str:
       """
       Generates the code for the label printer containing all information for label, such as texts, fonts, positions,
       font sizes and paper feeding.
       Hint: Sometimes the printer might lose the right position and produce faulty labels in the process. In this case
       uncomment the 'HOME' command in the second line of the string to reset the position of the empty labels

       :param record: The JSON of the print job
       :return: Returns the text for the label printer within its code syntax
       """
       return "REM Uncomment HOME for initialization of length\n" \
              "REM HOME\n" \
              "OFFSET 3 mm\n" \
              "CLS\n" \
              "TEXT 16,8,\"A.FNT\",0,1,1,0,\"Parkinson Algorithm deTecT\"\n" \
              "TEXT 16,17,\"A.FNT\",0,1,1,0,\"movEment patteRNs\"\n" \
              "TEXT 280,8,\"ROMAN.TTF\",0,6,6,3,\"QC_ID " + str(record['id']) + "\"\n\n" \
              "REM Patientendaten\n" \
              "TEXT 10,27,\"ROMAN.TTF\",0,8,8,0,\"Pat.:" + record['surname'] + "," + record['givenName'] + "\"\n" \
              "TEXT 10,50,\"ROMAN.TTF\",0,8,8,\"Station:" + record['hospitalWard'] + "\"\n" \
              "TEXT 10,73,\"ROMAN.TTF\",0,7,7,\"Fallnummer:" + str(record['caseID']) + "\"\n" \
              "TEXT 10,94,\"ROMAN.TTF\",0,7,7,\"Geb.:" + record['birthday'] +  "\"\n" \
              "REM Arzneimittelbezeichnung\n" \
              "TEXT 10,117,\"ROMAN.TTF\",0,8,8,\"" + record['medicationName'] + "\"\n" \
              "TEXT 10,140,\"ROMAN.TTF\",0,8,8,\"Gabe:" + record['medicationTimeStamp'] + "\"\n" \
              "TEXT 210,140,\"ROMAN.TTF\",0,8,8,\"Dosis:" + str(record['medicationDose']) + "\"\n" \
              "TEXT 10,165,\"ROMAN.TTF\",0,6,6,\"LogistikID:" + record['logisticsID'] + "\"\n\n" \
              "PRINT 1"

def print_label(record: dict) -> int:
       """
       Prints the label for the specified print job. A temporary file is created (and deleted) in the process

       :param record: The JSON of the print job
       :return: Returns True, if the label was printed. False otherwise
       """
       label_string = generate_label_string(record)
       tmp = tempfile.NamedTemporaryFile()
       filepath = tmp.name
       print('Generated tempfile at ' + filepath)
       with open(filepath, 'w') as tmp_file:
              tmp_file.write(label_string)

       return_status = os.system('/usr/bin/lp -d ' + config.LABEL_PRINTER + ' ' + filepath)
       return return_status == 0

async def check_if_medication_printer_available() -> str:
       """
       Tests if the printer is present on the Repetier server and online
       :return: Returns a result string for output of the REST-API
       """
       async with websockets.connect(
              'ws://' + config.REPETIER_ADDRESS + '/socket?apikey=' + config.REPETIER_API_KEY) as websocket:
              printer_json = {"action": "listPrinter", "data": {}, "callback_id": -1}
              await websocket.send(json.dumps(printer_json).encode())
              response = json.loads(await websocket.recv())
              for entry in response['data']:
                     if entry['slug'] != config.MEDICATION_PRINTER:
                            continue
                     if not entry['active']:
                            return config.MEDICATION_PRINTER + ' not active'
                     if entry['online'] != 1:
                            return config.MEDICATION_PRINTER + ' not online'
                     return  config.MEDICATION_PRINTER + ' ready to print'
              return 'Printer with slug ' + config.MEDICATION_PRINTER + ' not installed'



async def get_model_id(log_id: str) -> int:
       """
       Checks if a G-Code for the specified logistics ID (from IDMedics) is present on the Repetier server.
       :param log_id: The logistics ID
       :return: Returns the internal Repetier server ID of the G-Code and -1 of not present
       """
       async with websockets.connect(
               'ws://' + config.REPETIER_ADDRESS + '/socket?apikey=' + config.REPETIER_API_KEY) as websocket:
              models_json = {"action": "listModels", "data": {}, "printer": "MedicationPrinter",
                             "callback_id": -1}
              await websocket.send(json.dumps(models_json).encode())

              response = json.loads(await websocket.recv())
              for entry in response['data']['data']:
                     name = entry['name']
                     if name == log_id:
                            return entry['id']

              return -1

async def print_dose(record: dict) -> str:
       """
       Starts the medication printing for the record
       :param record: The record from the print job database
       :return: Returns 'Done' if printing was started and a string containing the error message otherwise
       """
       printer_str = await check_if_medication_printer_available()
       if printer_str != config.MEDICATION_PRINTER + ' ready to print':
              print(printer_str)
              return printer_str
       model_id = await get_model_id(record['logisticsID'])
       if model_id == -1:
              error_string = ('G-Code file with the name ' + record['logisticsID']
                      +  ' is not stored for printer "' + config.MEDICATION_PRINTER + '"')
              print(error_string)
              return error_string
       async with websockets.connect('ws://' + config.REPETIER_ADDRESS + '/socket?apikey=' + config.REPETIER_API_KEY) as websocket:
              print_json = {"action": "copyModel", "data": {"id":model_id}, "printer": config.MEDICATION_PRINTER,
                            "callback_id": record['id']}
              await websocket.send(json.dumps(print_json).encode())

              response = json.loads(await websocket.recv())
              if not response['data']['ok']:
                     error_string = 'Could not print job with logistics ID "' + record['logisticsID'] + '" on printer "' + config.MEDICATION_PRINTER + '"'
                     if 'error' in response['data']:
                            error_string += ', reason was: ' + response['data']['error']
                     print(error_string)
                     return error_string
              return 'Done'
