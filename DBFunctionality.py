#!/usr/bin/python
import MySQLdb
import hashlib
import binascii
import base64
import os

defaultHost = "showtracker.cpjzd8tz0d4b.ap-northeast-1.rds.amazonaws.com";
defaultUserName = "master";
defaultPassword = "anonymous";
defaultDB = "showtracker";
defaultPort = 3306;

def connectDB ():
	database = MySQLdb.connect(host = defaultHost,
                     user = defaultUserName,
                     passwd = defaultPassword,
                     db = defaultDB)
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

def checkTable():
        database = connectDB()
        cursor = database.cursor()
        cursor.execute("""SELECT * FROM Login_Info;""")
        if(cursor.fetchone()):
                cursor.close()
                database.close()
                return -1
        else:
                return 0
def wipeDB():
        database = connectDB()
        database.query("""SET FOREIGN_KEY_CHECKS=0;""")
        database.query("""DROP TABLE IF EXISTS Login_Info;""")
        database.query("""DROP TABLE IF EXISTS Movies;""")
        database.query("""DROP TABLE IF EXISTS TV_Shows;""")
        database.query("""DROP TABLE IF EXISTS Other;""")
        database.query("""DROP TABLE IF EXISTS Watch_Records;""")
        database.commit()
        database.close()
        
def initiateDB():
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
                    Database_ID INT,
                    Director VARCHAR(255), 
                    Year_Published SMALLINT, 
                    PRIMARY KEY(Record_ID), 
                    FOREIGN KEY (Record_ID) REFERENCES Watch_Records(Record_ID)
                    );""")
	database.query("""CREATE TABLE TV_Shows(
                    Record_ID INT	NOT NULL	UNIQUE,
                    Database_ID INT,
                    Episode_Count SMALLINT, 
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
	database = connectDB()
	cursor = database.cursor()
	cursor.execute("""SELECT * FROM Login_Info 
					WHERE Email = %s ;""", (email,))
	if(cursor.fetchone()):
		cursor.close()
		database.close()
		return -1
	
	salt = os.urandom(18)
	
	hasher = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100001)
	
	hash = binascii.hexlify(hasher)
	
	
	cursor.execute("""INSERT INTO Login_Info (Email, Password_Hash, Salt)
					VALUES ( %s, %s, %s );""", (email, hash.decode(), base64.b64encode(salt).decode()))
	
	database.commit()
	cursor.close()
	database.close()
	
	return checkLogin(email, password)

def checkLogin(email, password):
	database = connectDB()
	cursor = database.cursor()
	cursor.execute("""SELECT Email, Password_Hash, Salt FROM Login_Info 
					WHERE Email = %s ;""", (email,))
	result = cursor.fetchone()
	if(result == None):
		cursor.close()
		database.close()
		return -1
	
	saltStr = result[2]
	
	salt = base64.b64decode(saltStr.encode('utf-8'))
	
	hasher = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100001)
	
	hash = binascii.hexlify(hasher).decode()
	
	if(hash != result[1]):
		return -1
	
	cursor.close()
	database.close()
	return result[0]

def getUserID(email):
        database = connectDB()
        cursor = database.cursor()
        cursor.execute("""SELECT User_ID FROM Login_Info WHERE Email = %s;""", (email,))

        result = cursor.fetchone()
        cursor.close()
        database.close()
        return result[0]
	
def insertNewRecord(userID, videoName, platformName, videoType, cursor):	
	cursor.execute("""INSERT INTO Watch_Records (User_ID, Name, Video_Type, Date_Watched, Platform)
                VALUES (%s, %s, %s, CURDATE(), %s);""", (userID, videoName, videoType, platformName))

def insertNewMovie(userID, database_id, videoName, platformName, director, year):
	database = connectDB()
	cursor = database.cursor()
	insertNewRecord(userID, videoName, platformName, "M", cursor)
	cursor.execute("""INSERT INTO Movies (Record_ID, Database_ID, Director, Year_Published)
                    VALUES (LAST_INSERT_ID(), %s, %s, %s);""", (database_id, director, year))
	database.commit()
	cursor.close()
	database.close()

def insertNewTVshow(userID, database_id, videoName, platformName, yearPublished, ep_count, lastEpisodeWatched, anime = None):
	database = connectDB()
	cursor = database.cursor()
	if anime is None or anime is False:
		insertNewRecord(userID, videoName, platformName, "T", cursor)
	else:
		insertNewRecord(userID, videoName, platformName, "A", cursor)
	cursor.execute("""INSERT INTO TV_Shows (Record_ID, Database_ID, Year_Published, Episode_Count, Recent_Episode_Watched)
					VALUES (LAST_INSERT_ID(), %s, %s, %s, %s);""", (database_id, yearPublished, ep_count, lastEpisodeWatched))
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
                    SET Date_Watched = CURDATE() 
                    WHERE Record_ID = %s AND User_ID = %s;""", (recordID, userID))
	database.commit()
	cursor.close()
	database.close()
	
def updateTVShow(userID, recordID, lastEpisodeWatched):
	database = connectDB()
	cursor = database.cursor()
	cursor.execute("""SELECT Episode_Count FROM TV_Shows
					WHERE Record_ID = %s ;""", (recordID,))
	result = cursor.fetchone()

	if(lastEpisodeWatched <= result[0]):
                cursor.execute("""UPDATE Watch_Records 
                                SET Date_Watched = CURDATE() 
                                WHERE Record_ID = %s AND User_ID = %s;""", (recordID, userID))
                cursor.execute("""UPDATE TV_Shows 
                                SET Recent_Episode_Watched = %s 
                                WHERE Record_ID = %s""", (lastEpisodeWatched, recordID))
                
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
		cursor.execute("""DELETE FROM TV_Shows 
                        WHERE Record_ID = %s ;""", (recordID,))
	else:
		cursor.execute("""DELETE FROM other 
                        WHERE Record_ID = %s ;""", (recordID,))
		
	cursor.execute("""DELETE FROM Watch_Records 
                    WHERE Record_ID = %s AND User_ID = %s ;""", (recordID, userID))
	database.commit()
	cursor.close()
	database.close()
	
def getAllUserRecords(userID, addSeasonEpisodeNumber = False, desending = True, sortedColumn = None):
	database = connectDB()
	cursor = database.cursor()
	
	if(addSeasonEpisodeNumber):
		query = """SELECT User_ID, Watch_Records.Record_ID, Video_Type, Date_Watched, Platform, Episode_Count, Recent_Episode_Watched 
            FROM Watch_Records LEFT JOIN TV_Shows 
            ON Watch_Records.Record_ID = TV_Shows.Record_ID 
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
	database = connectDB()
	cursor = database.cursor()
	
	query = """SELECT * FROM Watch_Records LEFT JOIN Movies 
			ON Watch_Records.Record_ID = Movies.Record_ID
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
	result = cursor.fetchall()
	return result
	
def getAllUserTVRecords(userID, desending = True, sortedColumn = None):
	database = connectDB()
	cursor = database.cursor()

	query = """SELECT *, concat('width:',round(( Recent_Episode_Watched/Episode_Count * 100 ),2),'%%') as Percentage
                FROM Watch_Records LEFT JOIN TV_Shows ON Watch_Records.Record_ID = TV_Shows.Record_ID WHERE Video_Type = 'T' AND User_ID = %s """
	
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

def getAllUserAnimeRecords(userID, desending = True, sortedColumn = None):
	database = connectDB()
	cursor = database.cursor()
	
	query = """SELECT *, concat('width:',round(( recent_episode_watched/episode_count * 100 ),2),'%%') AS style
                FROM Watch_Records LEFT JOIN TV_Shows ON Watch_Records.Record_ID = TV_Shows.Record_ID WHERE Video_Type = 'A' AND User_ID = %s """
	
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
	database = connectDB()
	cursor = database.cursor()
	
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
	database = connectDB()
	cursor = database.cursor()
	
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
	database = connectDB()
	cursor = database.cursor()
	
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
	
