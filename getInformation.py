from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from Encryption import dataDecryption
import json, smtplib, imghdr, ssl

def getJsonInformation():
    #---- Grbas all information from the information.json file ----
    with open("information.json") as secretinformation:
        data = json.load(secretinformation)
    return data

def getServerInformation(organizer):
    data = getJsonInformation()
    if not organizer: 
        if data.get("PGSQL"):
            #---- If the server is PGSQL make sure to run pip install pgsql or pip3 install pgsql to install the proper packages ----
            import psycopg2
            conn = psycopg2.connect(user=data.get("AttendeedatabaseAddress")[0:data.get('AttendeedatabaseAddress').find("@")], password= dataDecryption(data.get("AttendeedatabasePassword")), host=data.get("AttendeedatabaseAddress")[data.get("AttendeedatabaseAddress").find("@")+1:len(data.get("AttendeedatabaseAddress"))], database=data.get("Attendeedatabase"))
        else:
            #---- If the server is MYSQL make sure to run pip install mysql or pip3 install mysql to install the proper packages ----
            import mysql.connector
            conn = mysql.connector.connect(user=data.get("AttendeedatabaseAddress")[0:data.get('AttendeedatabaseAddress').find("@")], password= dataDecryption(data.get("AttendeedatabasePassword")), host=data.get("AttendeedatabaseAddress")[data.get("AttendeedatabaseAddress").find("@")+1:len(data.get("AttendeedatabaseAddress"))], database=data.get("Attendeedatabase"), auth_plugin='mysql_native_password')
    else:
        if data.get("PGSQL"):
            import psycopg2
            conn = psycopg2.connect(user=data.get("OrganizerdatabaseAddress")[0:data.get('OrganizerdatabaseAddress').find("@")], password= dataDecryption(data.get("OrganizerdatabasePassword")), host=data.get("OrganizerdatabaseAddress")[data.get("OrganizerdatabaseAddress").find("@")+1:len(data.get("AttendeedatabaseAddress"))], database=data.get("Organizerdatabase"))
        else:
            import mysql.connector
            conn = mysql.connector.connect(user=data.get("OrganizerdatabaseAddress")[0:data.get('OrganizerdatabaseAddress').find("@")], password= dataDecryption(data.get("OrganizerdatabasePassword")), host=data.get("OrganizerdatabaseAddress")[data.get("OrganizerdatabaseAddress").find("@")+1:len(data.get("AttendeedatabaseAddress"))], database=data.get("Organizerdatabase"), auth_plugin='mysql_native_password')
    #---- If any errors happen feel free to contact me about this issue ----
    return conn

def sendEmail(subject, message, Email):
    data = getJsonInformation()
    server = smtplib.SMTP("smtp.gmail.com", 587 )  ## This will start our email server
    server.starttls(context=ssl.create_default_context())         ## Starting the server
    #---- Gets the credentials for the gmail login ----
    server.login(data.get("email"), dataDecryption(data.get("EmailPassword")))
    mimeMessage = MIMEMultipart()
    #---- Send a message witha certain subject ----
    mimeMessage['to'] = Email
    mimeMessage['subject'] = subject
    mimeMessage.attach(MIMEText(message, 'plain'))
    server.sendmail(data.get("email"), Email, mimeMessage.as_string())
    server.quit()


def sendEmailAttachment(Subject, Message, Email, FileName):
    data = getJsonInformation()
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls(context=ssl.create_default_context())
    server.login(data.get("email"),  dataDecryption(data.get("EmailPassword")))
    newMessage = EmailMessage()
    newMessage['Subject'] = Subject
    newMessage['From'] = data.get("email")
    newMessage['To'] = Email
    newMessage.set_content(Message)
    #---- Open the file and write it as image data as the QR code is an image ----
    with open(FileName, 'rb') as f:
        image_data = f.read()
        image_type = imghdr.what(f.name)
        image_name = f.name
    #---- Adds the attachment and sends the attachment as an image ----
    newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)
    server.send_message(newMessage)
    
