from getInformation import *
from Encryption import *
from re import sub
import base64, pandas, csv, os, numpy, qrcode, image, re

#---- Checks if user is organizer with random generated password sent 2 days before the event ----
def checkifuser(username, password):
    data = getJsonInformation()
    if data.get("Server"):
        conn = getServerInformation(True)
        if (data.get("PGSQL")):
            cursor = conn.cursor()
        else:
            cursor = conn.cursor(buffered=True)
        information1 = "SELECT username, dict FROM account"
        cursor.execute(information1)
        conn.commit()
        records = cursor.fetchall()
        for row in records:
            if row[0] == username and password == dataDecryption(row[1]):
                cursor.close()
                return True
        cursor.close()
    else:
        
        with open('organizerPassword.txt', 'r') as f:
            text = f.read()
        if username == "Organizer" and password == dataDecrpytion(text):
            return True
    return False

#---- Save/Grab Attendee information ----
def customCollection():
    data = getJsonInformation()
    queryString = "("
    valueString = "VALUES ("
    for x in range(len(data.get("Columns"))):
        if data.get("PGSQL"):
            if x == len(data.get("Columns")) -1:
                queryString = queryString + '"' + data.get("Columns")[x] + '", "CheckedIn") '
                valueString = valueString + "%s, %s) "
            else:
                queryString = queryString + '"' + data.get("Columns")[x] +'", ' 
                valueString = valueString + "%s, "
        else:
            if x == len(data.get("Columns")) -1:
                queryString = queryString + "`" + data.get("Columns")[x] + "`, `CheckedIn`) "
                valueString = valueString + "%s, %s) "
            else:
                queryString = queryString + "`" + data.get("Columns")[x] +"`, " 
                valueString = valueString + "%s, "
    return queryString, valueString

def useAttendeeInformation():
    data = getJsonInformation()
    queryString, valueString = customCollection()
    if ".csv" in data.get("FileName"):
        AttendeeList = pandas.read_csv(data.get("FileName"), usecols=data.get("Columns"))
        Attendeedata = AttendeeList.values.tolist()
        biglist = []
        for x in Attendeedata:
            newlist = []
            for y in range(len(x)):
                if x[y] is numpy.nan:
                    newlist = []
                    continue
                else:
                    if y != data.get("UniqueColumnNumber") or y != data.get("CheckedInColumnNumber"):
                        newlist.append(dataEncryption(str(x[y])))
                    else:
                        sendEmail("Hackathon ID Number", "The following is your ID Number: " + str(x[y]) + " Please make sure you store this number and present during checkin.", x[data.get("EmailColumnNumber")])
                        newlist.append(str(x[y]))
                newlist.append("Not Checked In")
                if data.get("Server"):
                    conn = getServerInformation(False)
                    if (data.get("PGSQL")):
                        cursor = conn.cursor()
                    else:
                        cursor = conn.cursor(buffered=True)
                    results = ("INSERT INTO " + data.get("AttendeeTableName") + queryString + valueString)
                    results_data = tuple(newlist)
                    cursor.execute(results, results_data)
                    conn.commit()
            biglist.append(newlist)
        df = pandas.DataFrame(biglist)
        columnList = data.get("Columns")
        columnList.append(["Not Checked In"])
        df.columns = columnList
        df.to_csv(data.get("EncryptedFileName"))
        os.remove(data.get("FileName"))
    else:
        AttendeeList = pandas.read_excel(data.get("FileName"), index_col=None, na_values=['NA'], usecols=data.get("Columns"), engine="openpyxl")
        Attendeedata = AttendeeList.values.tolist()
        biglist = []
        for x in Attendeedata:
            newlist = []
            for y in range(len(x)):
                if y != data.get("UniqueColumnNumber"):
                    newlist.append(dataEncryption(str(x[y])))
                else:
                    QRCodeGenerator(x[y], x[data.get("EmailColumnNumber")])
                    newlist.append(str(x[y]))
            newlist.append("Not Checked In")
            if data.get("Server"):
                conn = getServerInformation(False)
                if (data.get("PGSQL")):
                    cursor = conn.cursor()
                else:
                    cursor = conn.cursor(buffered=True)
                results = ("INSERT INTO " + data.get("AttendeeTableName") + queryString + valueString)
                results_data = tuple(newlist)
                cursor.execute(results, results_data)
                conn.commit()
            biglist.append(newlist)
        df = pandas.DataFrame(biglist)
        columnList = data.get("Columns")
        columnList.append(["Not Checked In"])
        df.columns = columnList
        writer = pandas.ExcelWriter(data.get("EncryptedFileName"), engine="xlsxwriter")
        df.to_excel(writer, index=False)
        writer.save()
        os.remove(data.get("FileName"))

#---- Grab all Attendee information that is stored ----
def grablist(IDNum):
    data = getJsonInformation()
    if IDNum:
        if (data.get("PGSQL")):
            information1 = 'SELECT "' + data.get("Columns")[data.get("UniqueColumnNumber")] + '" FROM ' + data.get("AttendeeTableName")
        else:
            information1 = 'SELECT `' + data.get("Columns")[data.get("UniqueColumnNumber")] + '` FROM ' + data.get("AttendeeTableName")
    else:
        information1 = "SELECT * FROM " + data.get("AttendeeTableName")
    return information1

def AttendeeListGrab():
    data = getJsonInformation()
    if data.get("Server"):
        conn = getServerInformation(False)
        if (data.get("PGSQL")):
            cursor = conn.cursor()
        else:
            cursor = conn.cursor(buffered=True)
        cursor.execute(grablist(False))
        conn.commit()
        records = cursor.fetchall()
        return records
    else:
        if ".csv" in data.get("FileName"):
            AttendeeList = pandas.read_csv(data.get("EncryptedFileName"), usecols=data.get("Columns"))
            Attendeedata = AttendeeList.values.tolist()
        else:
            AttendeeList = pandas.read_excel(data.get("EncryptedFileName"), index_col=None, na_values=['NA'], usecols=data.get("Columns"))
            Attendeedata = AttendeeList.values.tolist()
        return Attendeedata

#---- Check in Attendee ----
def checkAttendee(IDNumber):
    biglist = []
    data = getJsonInformation()
    AttendeeData = AttendeeListGrab()
    if data.get("Server"):
        conn = getServerInformation(False)
        if (data.get("PGSQL")):
            cursor = conn.cursor()
        else:
            cursor = conn.cursor(buffered=True)
        cursor.execute(grablist(True))
        conn.commit()
        records = cursor.fetchall()
        for row in records:    
            if row[data.get("UniqueColumnNumber")] == IDNumber:
                #if "Not Checked In" not in row:
                 #   return False
                if data.get("PGSQL"):
                    results1 = "UPDATE " + data.get("AttendeeTableName") + ' set "CheckedIn" = %s WHERE "' + data.get("Columns")[data.get("UniqueColumnNumber")] + '" = %s;'
                else:
                    results1 = "UPDATE " + data.get("AttendeeTableName") + " set `CheckedIn` = %s WHERE `" + data.get("Columns")[data.get("UniqueColumnNumber")] + "` = %s;"
                cursor.execute(results1, ("Checked In", IDNumber))
                conn.commit()
                return True
    else: 
        for x in AttendeeData:
            if IDNumber == int(x[data.get("UniqueColumnNumber")]):
                with open('Checkedin.txt', 'r') as f:
                    text = f.read()
                if str(IDNumber) in text:
                    return False
                with open("Checkedin.txt", "w") as f:
                    text = text + str(IDNumber) + "\n"
                    f.write(text)
                return True
    return False

def checkAttendeeFirstName(FirstName, LastName, Email):
    data = getJsonInformation()
    AttendeeData = AttendeeListGrab()
    if data.get("Server"):
        conn = getServerInformation(False)
        if (data.get("PGSQL")):
            cursor = conn.cursor()
        else:
            cursor = conn.cursor(buffered=True)
        cursor.execute(grablist(False))
        conn.commit()
        records = cursor.fetchall()
        for row in records:
            if FirstName == dataDecryption(row[data.get("FirstNameColumnNumber")]) and LastName == dataDecryption(row[data.get("LastNameColumnNumber")]) and Email == dataDecryption(row[data.get("EmailColumnNumber")]):
                if (data.get("PGSQL")):
                    results1 = "UPDATE " + data.get("AttendeeTableName") + ' set "CheckedIn" = %s WHERE "' + data.get("Columns")[data.get("UniqueColumnNumber")] + '" = %s;'
                else: 
                    results1 = "UPDATE " + data.get("AttendeeTableName") + " set `CheckedIn` = %s WHERE `" + data.get("Columns")[data.get("UniqueColumnNumber")] + "` = %s;"
                cursor.execute(results1, ("Checked In", row[data.get("UniqueColumnNumber")]))
                conn.commit()
                return True
    else: 
        for x in AttendeeData:
            if FirstName == dataDecryption(x[data.get("FirstNameColumnNumber")]) and LastName == dataDecryption(x[data.get("LastNameColumnNumber")]) and Email == dataDecryption(x[data.get("EmailColumnNumber")]):
                with open('Checkedin.txt', 'r') as f:
                    text = f.read()
                if (str(x[data.get("UniqueColumnNumber")]) in text):
                    return False
                with open("Checkedin.txt", "w") as f:
                    text = text + str(x[data.get("UniqueColumnNumber")]) + "\n"
                    f.write(text)
                return True
    return False

#---- Check out Attendee ----
def checkoutAttendee(IDNumber):
    data = getJsonInformation()
    AttendeeData = AttendeeListGrab()
    if data.get("Server"):
        conn = getServerInformation(False)
        if (data.get("PGSQL")):
            cursor = conn.cursor()
        else:
            cursor = conn.cursor(buffered=True)
        cursor.execute(grablist(True))
        conn.commit()
        records = cursor.fetchall()
        for row in records:
            if row[data.get("UniqueColumnNumber")] in IDNumber:
                if data.get("PGSQL"):
                    results1 = "UPDATE " + data.get("AttendeeTableName") + ' set "CheckedIn" = %s WHERE "' + data.get("Columns")[data.get("UniqueColumnNumber")] + '" = %s;'
                else:
                    results1 = "UPDATE " + data.get("AttendeeTableName") + " set `CheckedIn` = %s WHERE `" + data.get("Columns")[data.get("UniqueColumnNumber")] + "` = %s;"
                cursor.execute(results1, ("Not Checked In", IDNumber))
                conn.commit()
                return True
    else:
        for x in AttendeeData:
            if IDNumber == int(x[data.get("UniqueColumnNumber")]):
                with open('Checkedin.txt', 'r') as f:
                    text = f.read()
                with open("Checkedin.txt", "w") as f:
                    text = text.replace(str(IDNumber),"")
                    f.write(text)
                return True
    return False

def checkoutAttendeeFirstName(FirstName, LastName, Email):
    data = getJsonInformation()
    AttendeeData = AttendeeListGrab()
    if data.get("Server"):
        conn = getServerInformation(False)
        if (data.get("PGSQL")):
            cursor = conn.cursor()
        else:
            cursor = conn.cursor(buffered=True)
        cursor.execute(grablist(False))
        conn.commit()
        records = cursor.fetchall()
        for row in records:
            if FirstName == dataDecryption(row[data.get("FirstNameColumnNumber")]) and LastName == dataDecryption(row[data.get("LastNameColumnNumber")]) and Email == dataDecryption(row[data.get("EmailColumnNumber")]):
                if (data.get("PGSQL")):
                    results1 = "UPDATE " + data.get("AttendeeTableName") + ' set "CheckedIn" = %s WHERE "' + data.get("Columns")[data.get("UniqueColumnNumber")] + '" = %s;'
                else: 
                    results1 = "UPDATE " + data.get("AttendeeTableName") + " set `CheckedIn` = %s WHERE `" + data.get("Columns")[data.get("UniqueColumnNumber")] + "` = %s;"
                cursor.execute(results1, ("Not Checked In", row[data.get("UniqueColumnNumber")]))
                conn.commit()
                return True
    else: 
        for x in AttendeeData:
            if FirstName == dataDecryption(x[data.get("FirstNameColumnNumber")]) and LastName == dataDecryption(x[data.get("LastNameColumnNumber")]) and Email == dataDecryption(x[data.get("EmailColumnNumber")]):
                with open('Checkedin.txt', 'r') as f:
                    text = f.read()
                with open("Checkedin.txt", "w") as f:
                    text = text.replace(str(x[data.get("UniqueColumnNumber")]),"")
                    f.write(text)
                return True
    return False

#---- Generates a table for the attendee list that can be viewed on the website ----
def viewAttendeeList():
    data = getJsonInformation()
    AttendeeList = AttendeeListGrab()
    #print("attenlist", AttendeeList)
    TableContent = "<table><tr>"
    for x in data.get("Columns"):
        TableContent = TableContent + "<th>%s</th>" %(x)
    TableContent = TableContent +"<th>Checked in</th></tr>"
    try: 
        with open("Checkedin.txt", "r") as f:
            text = f.readlines()
    except IOError:
        text = ""
    for x in AttendeeList:
        TableContent = TableContent + "<tr>"
        for y in range(len(x)-1):
            if y != data.get("UniqueColumnNumber"):
                TableContent = TableContent + "<td>%s</td>" %(dataDecryption(x[y]))
            else:
                TableContent = TableContent + "<td>%s</td>" %(x[y])
        table = False
        if data.get("Server"):
            table = True
            if "Not" not in str(x[len(x)-1]):
                TableContent = TableContent + "<td>True</td>"
            else:
                table = False
        else:
            for textstring in text:
                table = True
                if float(x[data.get("UniqueColumnNumber")]) == float(textstring.replace("\n", "")):
                    TableContent = TableContent + "<td>True</td>"
                else:
                    table = False
        if not table:
            TableContent = TableContent + "<td>False</td>"
        TableContent = TableContent + "</tr>"
    TableContent = TableContent + "</table>"
    return {"TableContent": TableContent}

#---- Generates QR Code for Attendess to show Organizer for efficient check in ----
def QRCodeGenerator(IDNumber, Email):
    data = getJsonInformation()
    EncryptionString = dataEncryption(Str(IDNumber))
    dataqr = data.get("site") +"/qrcode/" + EncryptionString
    img = qrcode.make(dataqr)
    img.save("qrCode/" + re.sub(r"[^a-zA-Z0-9 ]","",EncryptionString) + ".png")
    sendEmailAttachment("ID Number and QR Code for Tri Valley Crypto Hacks Check in", "Your ID Number is " + str(IDNumber), Email, "qrCode/" + re.sub(r"[^a-zA-Z0-9 ]","",EncryptionString) +".png", )

#---- Removes all information on Attendees and Organizer Accounts ----
def removeEntries():
    data = getJsonInformation()
    if data.get("Server"):
        conn = getServerInformation(True)
        if (data.get("PGSQL")):
            cursor = conn.cursor()
        else:
            cursor = conn.cursor(buffered=True)
        #---- Will Delete all contents in the table account ----
        #---- Note this table stores the Organizer password needed to login into the webstie ----
        information1 = "DELETE FROM account"
        cursor.execute(information1)
        conn.commit()
        conn = getServerInformation(False)
        cursor = conn.cursor()
        #---- will Delete all contents in the table Attendee ----
        #---- Note this table stores the Attendee information ----
        information1 = "DELETE FROM Attendee"
        cursor.execute(information1)
        conn.commit()
    else:
        #---- Will delete the text file that stores the encrypted version of the Organizer password ----
        os.remove("organizerPassword.txt")
    for x in os.listdir("qrCode"):
        os.remove(os.path.join("qrCode", x))
    #---- Will delete the plain text file with the attendee information, encrypted attendee information, and all ID Numbers that have been checked in ----
   
    try: 
        os.remove(data.get("FileName"))
        os.remove(data.get("EncryptedFileName"))
        os.remove("Checkedin.txt")
    except IOError:
        print("File already exists")