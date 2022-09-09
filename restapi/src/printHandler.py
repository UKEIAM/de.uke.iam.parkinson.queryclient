import tempfile, os
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

       return_status = os.system('/usr/bin/lp -d labelprinter ' + filepath)
       return return_status == 0