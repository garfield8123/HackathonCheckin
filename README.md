# **Hackathon Check-in**

An easy way to checkin all attendees in an efficient manner.

## **Project Directory**

- [HTML](/HTML)

  - Directory where all HTML files are kept
  - Note: TPL (Template File) can handle HTML Code.
- [Scripts](/Scripts)

  - Directory where all the script files are kept
- [images](/images)

  - Directory where all the Images are kept
- [qrCode](/qrCode)
  - Directory where all the QRCode images are saved
- [app.py](app.py)

  - Main file running the server and accessible directories
- [Encryption.py](Encryption.py)

  - Python file handling the encryption and decrpytion of user sensitive information (Hidden by public: As this Encrypts all user data)
- [UserInfo.py](UserInfo.py)

  - Python file handling the uploading and accessing of User Information

- [getInformation.py](getInformation.py)
  - Gets all the information needed to setup the server and create the secure files

## **Information.json**

- What to write in the JSON file?
  - The date of the event in the following format
  - The website domain hosting the program
  - Email password for sending the credentials (Make sure dual Authentication and an app password available: [Here](https://support.google.com/accounts/answer/185833?hl=en)

- infomration.json should look:
  - {"webserver": "localhost:5000", "Columns": ["`Order #`", "`First Name`", "`Last Name`", "`Email`"], "UniqueColumnNumber": 0, "FirstNameColumnNumber": 1, "LastNameColumnNumber": 2, "EmailColumnNumber": 3, "OrganizerdatabaseAddress": "username@localhost", "OrganizerdatabasePassword": "password", "Organizerdatabase": "Organizer", "AttendeedatabaseAddress": "username@localhost", "AttendeedatabasePassword": "password", "Attendeedatabase": "Attendee", "AttendeeTableName": "Attendee", "FileName": "2019AttendeeList.xlsx", "EncryptedFileName": "2019AttendeeList.xlsx", "site": "https://trivalleyhacks.com", "Date": "2021-12-19 12:00:00.0000", "email": "trivalleyhacks@gmail.com", "EmailPassword": "password", "Server": false, "PGSQL": false}

- System requirements: 
  - Cloud Hosting

    - Postgre SQL (powered by Heroku Cloud)
    - Heroku

  - Local/Real Machine

    - Python3 environment
    - apache2/web server

    - Optional
      - MYSQL/Postgre SQL database


## ** Security of Users**
- Passwords Stored
  - Look like this:
  - In addition, data stored is obfuscated in the encryption
  - Adds a layer of complexity for user stored data

## **Required Setup**
- Local/Real Machine
  - python3
  - Apache or some type of web server
  - pip3 install -r requirements.txt or pip install -r requirements.txt

- Cloud hosting
  - Python3 
  - Apache or some type of web server

## **Optional Setup**
- Local/Real Machine
  - MYSQL/PGSQL Database to store Attendee and Organizer data
  - pip3 install mysql-connector or pip3 install pgsql (More information: [MYSQL here](https://pypi.org/project/mysql-connector/) [PGSQL here](https://pypi.org/project/psycopg/)

- Cloud hosting
  - MYSQL/PGSQL database to store Attendee and Organizer data
  - Add mysql or pgsql in requirements.txt (More information: [MYSQL here](https://pypi.org/project/mysql-connector/) [PGSQL here](https://pypi.org/project/psycopg/)

## **How to run the program?**
- Local Real/Machine
  - Run the following command: pip3 install -r requirements.txt (Some modules may not install fully so make sure to check)
  - Fille out the information.json file appropriately and run python3 Encryption.py (This will encrypt all passwords stored in the information.json file)

## **How to Setup? (Recommended Way)**

- Cloud Hosting

  - Create an account with Heroku: [Here](https://signup.heroku.com/login)
  - Create a new app
  - Connect to Github and find the repository
  - Enable Automatic Deploys
  - Go to Overview Tab within the created app and configure Add-Ons
  - Find the Add-On called Heroku Postgres
  - Then create the table by using the following file: [Here](/account.pgsql) can be done with PgAdmin4, which can be downloaded: [Here](https://www.pgadmin.org/download/)

  *Extra things you can do*

  - Click on Heroku database, then go to the Dataclips tab and create a new Dataclip with (SELECT * FROM "tableName")
  - Go to the billing page on the Account Settings and add a credit/debit card to get 1000 hours for free every Month

- Local/Real Machine

  - Install a Python3 environment: [Here](https://www.python.org/downloads/)
  - Install Mysql Editor (MYSQL, which can be installed: [Here](https://dev.mysql.com/downloads/mysql/) or Postgre Sql Editor (PgAdmin4, which can be installed: [Here](ttps://www.pgadmin.org/download/)
  - Then follow the similiar steps to creating a table in the Cloud
  - Install Xampp: [Here](https://www.apachefriends.org/download.html) (This has a web server within in it as well as databse servers)

# **If you have any Questions or Concerns please don't hesitate to create discussions**
