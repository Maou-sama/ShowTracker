#!/usr/bin/python
import MySQLdb
import hashlib
import binascii
import base64
import os

defaultHost = "127.0.0.1";
defaultUserName = "root";
defaultPassword = "";
defaultDB = "showtrackerdb";
defaultPort = 3306;

DATABASE = None



def connectDB ():
	database = MySQLdb.connect(host = defaultHost,
                     user = defaultUserName,  
                     passwd = defaultPassword,
                     db = defaultDB,
                     port = defaultPort)
	return database
	
def changeDefaultDBConnection(port, username = None, password = None, host = None):
	global defaultPort 
	global defaultHost
	global defaultUserName
	global defaultPassword
	defaultPort = port
	if(host):
		defaultHost = host
	if(username):
		defaultUserName = username
	if(password):
		defaultPassword = password

	
def initiateDB ():
	initalDBConn = MySQLdb.connect(host = defaultHost,
                     user = defaultUserName,  
                     passwd = defaultPassword,
					 port = defaultPort)
					 
	initalDBConn.query("CREATE DATABASE showtrackerdb;")
	initalDBConn.commit();
	initalDBConn.close()
	database = connectDB()
	database.query("""CREATE TABLE Login_Info
					(User_ID INT NOT NULL UNIQUE AUTO_INCREMENT, 
                    Email VARCHAR(254) NOT NULL UNIQUE, 
					Password_Hash VARCHAR(75) NOT NULL, 
                    Salt Varchar(25) NOT NULL
                    );""")
	database.query("""CREATE TABLE Watch_Records(
                    User_ID INT	NOT NULL, 
                    Record_ID INT	NOT NULL UNIQUE	AUTO_INCREMENT, 
                    Name VARCHAR(200) NOT NULL, 
                    Video_Type VARCHAR(1), 
                    Date_Watched DATE, 
                    Platform VARCHAR(100), 
                    PRIMARY KEY(RECORD_ID), 
                    FOREIGN KEY (User_ID) REFERENCES Login_Info(User_ID)
                    );""")
	database.query("""CREATE TABLE Movies (
                    Record_ID INT	NOT NULL	UNIQUE, 
                    Director VARCHAR(255), 
                    Year_Published SMALLINT, 
                    PRIMARY KEY(Record_ID), 
                    FOREIGN KEY (Record_ID) REFERENCES Watch_Records(Record_ID)
                    );""")
	database.query("""CREATE TABLE TV_shows(
                    Record_ID INT	NOT NULL	UNIQUE, 
                    Season_Number TINYINT, 
                    Year_Published SMALLINT, 
                    Recent_Episode_Watched SMALLINT, 
                    PRIMARY KEY(Record_ID), 
                    Foreign KEY (RECORD_ID) REFERENCES Watch_Records(RECORD_ID)
					);""")
	database.query("""CREATE TABLE Other(
                    Record_ID INT	NOT NULL	UNIQUE, 
                    Video_Author VARCHAR(255), 
                    PRIMARY KEY(Record_ID), 
                    Foreign KEY (RECORD_ID) REFERENCES Watch_Records(RECORD_ID)
                    );""")
	database.commit()
	database.close()

def insertNewLogin(email, password):
	DATABASE = connectDB()
	cursor = DATABASE.cursor()
	cursor.execute("""SELECT * FROM Login_info 
					WHERE Email = %s ;""", (email,))
	if(cursor.fetchone()):
		cursor.close()
		DATABASE.close()
		return -1
	
	salt = os.urandom(18)
	
	hasher = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100001)
	
	hash = binascii.hexlify(hasher)
	
	
	cursor.execute("""INSERT INTO Login_info (Email, Password_Hash, Salt)
					VALUES ( %s, %s, %s );""", (email, hash.decode(), base64.b64encode(salt).decode()))
	
	DATABASE.commit()
	cursor.close()
	DATABASE.close()
	
	return checkLogin(email, password)

def checkLogin(email, password):
	DATABASE = connectDB()
	cursor = DATABASE.cursor()
	cursor.execute("""SELECT Email, Password_Hash, Salt FROM Login_info 
					WHERE Email = %s ;""", (email,))
	result = cursor.fetchone()
	if(result == None):
		cursor.close()
		DATABASE.close()
		return -1
	
	saltStr = result[2]
	
	salt = base64.b64decode(saltStr.encode('utf-8'))
	
	hasher = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100001)
	
	hash = binascii.hexlify(hasher).decode()
	
	if(hash != result[1]):
		return -1
	
	cursor.close()
	DATABASE.close()
	return result[0]

	
def insertNewRecord(userID, videoName, platformName, videoType, cursor):	
	cursor.execute("""INSERT INTO Watch_Records (User_ID, Name, Video_Type, Date_Watched, Platform)
                VALUES (%s, %s, %s, NOW(), %s);""", (userID, videoName, videoType, platformName))
	cursor.close()

def insertNewMovie(userID, videoName, platformName, director, year):
	database = connectDB()
	cursor = database.cursor()
	insertNewRecord(userID, videoName, platformName, "M", cursor)
	cursor.execute("""INSERT INTO Movies (Record_ID, Director, Year_Published)
                    VALUES (LAST_INSERT_ID(), %s, %s);""", (director, year))
	database.commit()
	cursor.close()
	database.close()

def insertNewTVshow(userID, videoName, platformName, yearPublished, season, lastEpisodeWatched, anime = None):
	database = connectDB()
	cursor = database.cursor()
	if anime is None or anime is False:
		insertNewRecord(userID, videoName, platformName, "T", cursor)
	else:
		insertNewRecord(userID, videoName, platformName, "A", cursor)
	cursor.execute("""INSERT INTO TV_shows (Record_ID, Year_Published, Season_Number, Recent_Episode_Watched)
					VALUES (LAST_INSERT_ID(), %s, %s, %s);""", (yearPublished, season, lastEpisodeWatched))
	database.commit()
	cursor.close()
	database.close()

def insertNewOther(userID, videoName, platformName, videoAuthor):
	database = connectDB()
	cursor = database.cursor()
	insertNewRecord(userID, videoName, platformName, "O", cursor)
	cursor.execute("""INSERT INTO INTO Other (Record_ID, Video_Author)
                    VALUES (LAST_INSERT_ID(), %s);""", (videoAuthor,))
	database.commit()
	cursor.close()
	database.close()

def updateRecord(userID, recordID):
	database = connectDB()
	cursor = database.cursor()
	cursor.execute("""UPDATE Watch_Records 
                    SET Date_Watched = NOW() 
                    WHERE Record_ID = %s AND User_ID = %s;""", (recordID, userID))
	database.commit()
	cursor.close()
	database.close()
	
def updateTVshow(userID, recordID, lastEpisodeWatched, season = None):
	database = connectDB()
	cursor = database.cursor()
	cursor.execute("""UPDATE Watch_Records 
                    SET Date_Watched = NOW() 
                    WHERE Record_ID = %s AND User_ID = %s;""", (recordID, userID))
	if season is None:
		cursor.execute("""UPDATE TV_shows 
						SET Recent_Episode_Watched = %s 
						WHERE Record_ID = %s""", (lastEpisodeWatched, recordID))
	else:
		cursor.execute("""UPDATE TV_shows 
						SET Recent_Episode_Watched = %s,
							Season_Number = %s
						WHERE Record_ID = %s""", (lastEpisodeWatched, season, recordID))
	database.commit()
	cursor.close()
	database.close()
	
def deleteRecord(userID, recordID):
	database = connectDB()
	cursor = database.cursor()
	cursor.execute("""SELECT Video_Type FROM Watch_Records
					WHERE Record_ID = %s AND User_ID = %s ;""", (recordID, userID))
	result = cursor.fetchone()
	
	if(result[0] == 'M'):
		cursor.execute("""DELETE FROM Movies 
                        WHERE Record_ID = %s ;""", (recordID,))
	elif(result[0] == 'T' or result[0] == 'A'):
		cursor.execute("""DELETE FROM Movies 
                        WHERE Record_ID = %s ;""", (recordID,))
	else:
		cursor.execute("""DELETE FROM Movies 
                        WHERE Record_ID = %s ;""", (recordID,))
	cursor.execute("""DELETE FROM Watch_Records 
                    WHERE Record_ID = %s AND User_ID = %s ;""", (recordID, userID))
	database.commit()
	cursor.close()
	database.close()
	
def getAllUserRecords(userID, addSeasonEpisodeNumber = False, desending = True, sortedColumn = None):
	DATABASE = connectDB()
	cursor = DATABASE.cursor()
	
	if(addSeasonEpisodeNumber):
		query = """SELECT User_ID, Watch_Records.Record_ID, Video_Type, Date_Watched, Platform, Season_Number, Recent_Episode_Watched 
            FROM Watch_Records LEFT JOIN TV_shows 
            ON Watch_Records.Record_ID = TV_shows.Record_ID 
            WHERE User_ID = %s """;
	else:
		query = """SELECT * FROM Watch_Records 
				WHERE User_ID = %s """
				
	if(sortedColumn == None):
		query = query + "ORDER BY Date_Watched "
	else:
		query = query + "ORDER BY " + sortedColumn + " "
		
	if(desending):
		query = query + "DESC ;"
	else:
		query = query + "ASC ;"
	
	cursor.execute(query, (userID,))
	return cursor

def getAllUserMovieRecords(userID, desending = True, sortedColumn = None):
	DATABASE = connectDB()
	cursor = DATABASE.cursor()
	
	query = """SELECT * FROM Watch_Records LEFT JOIN Movies 
			ON Watch_Records.Record_ID = Movies.Record_ID;
			WHERE Video_Type = 'M' AND User_ID = %s """
	if(sortedColumn == None):
		query = query + "ORDER BY Date_Watched "
	else:
		query = query + "ORDER BY " + sortedColumn + " "
		
	if(desending):
		query = query + "DESC ;"
	else:
		query = query + "ASC ;"
	
	cursor.execute(query, (userID,))
	return cursor
	
def getAllUserTVRecords(userID, desending = True, sortedColumn = None):
	DATABASE = connectDB()
	cursor = DATABASE.cursor()
	
	query = """SELECT * FROM Watch_Records LEFT JOIN TV_shows 
            ON Watch_Records.Record_ID = TV_shows.Record_ID 
            WHERE (Video_Type = 'T' OR Video_Type = 'A') AND User_ID = %s """
	
	if(sortedColumn == None):
		query = query + "ORDER BY Date_Watched "
	else:
		query = query + "ORDER BY " + sortedColumn + " "
		
	if(desending):
		query = query + "DESC ;"
	else:
		query = query + "ASC ;"
	
	cursor.execute(query, (userID,))
	return cursor

def getAllOtherTVRecords(userID, desending = True, sortedColumn = None):
	DATABASE = connectDB()
	cursor = DATABASE.cursor()
	
	query = """SELECT * FROM Watch_Records LEFT JOIN Other 
            ON Watch_Records.Record_ID = Other.Record_ID 
            WHERE Video_Type = 'O' AND User_ID = %s """
	
	if(sortedColumn == None):
		query = query + "ORDER BY Date_Watched "
	else:
		query = query + "ORDER BY " + sortedColumn + " "
		
	if(desending):
		query = query + "DESC ;"
	else:
		query = query + "ASC ;"
	
	cursor.execute(query, (userID,))
	return cursor	

def searchByName(userID, target, desending = True, sortedColumn = None):
	DATABASE = connectDB()
	cursor = DATABASE.cursor()
	
	query = """SELECT * FROM Watch_Records 
            WHERE User_ID = %s AND Name LIKE %s """
	
	if(sortedColumn == None):
		query = query + "ORDER BY Date_Watched "
	else:
		query = query + "ORDER BY " + sortedColumn + " "
		
	if(desending):
		query = query + "DESC ;"
	else:
		query = query + "ASC ;"
	
	cursor.execute(query, (userID, "%" + target +"%"))
	return cursor
	
def searchByDate(userID,  year, month, day, comparison = 0, desending = True, sortedColumn = None):
	DATABASE = connectDB()
	cursor = DATABASE.cursor()
	
	query = """"SELECT * FROM Watch_Records 
			WHERE User_ID = :userID AND Date_Watched """
	
	if(comparison < 0):
		query = query + "< "
	elif(comparison > 0):
		query = query + "> "
	else:
		query = query + "= "
		
	query = query + " %s "
	
	if(sortedColumn == None):
		query = query + "ORDER BY Date_Watched "
	else:
		query = query + "ORDER BY " + sortedColumn + " "
		
	if(desending):
		query = query + "DESC ;"
	else:
		query = query + "ASC ;"
	
	date = year + "-" + month + "-" + day
	cursor.execute(query, (userID, "%" + target +"%"))
	return cursor	

def closeConnection():
	if(DATABASE != None):
		DATABASE.close()
	
	
