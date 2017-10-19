CREATE DATABASE IF NOT EXISTS Logins;

USE Logins;

CREATE TABLE Login_Info(
	Email VARCHAR(254) NOT NULL UNIQUE,
	Password_Hash VARCHAR(75) NOT NULL,
	Salt Varchar(25) NOT NULL
);



CREATE DATABASE IF NOT EXISTS username_test;

USE username_test;

CREATE TABLE Watch_Records(
	Record_ID INT	NOT NULL	UNIQUE	AUTO_INCREMENT,
	Name VARCHAR(200) NOT NULL,
	Video_Type VARCHAR(1),
	Date_Watched DATE,
	Platform VARCHAR(100),
	PRIMARY KEY(RECORD_ID)
);

CREATE TABLE Movies (
	Record_ID INT	NOT NULL	UNIQUE,
	Director VARCHAR(255),
	Year_Published SMALLINT,
	PRIMARY KEY(Record_ID),
	FOREIGN KEY (Record_ID) REFERENCES Watch_Records(Record_ID)
);

CREATE TABLE TV_shows(
	Record_ID INT	NOT NULL	UNIQUE,
	Season_Number TINYINT,
	Year_Published SMALLINT,
	Recent_Episode_Watched SMALLINT,
	PRIMARY KEY(Record_ID),
	Foreign KEY (RECORD_ID) REFERENCES Watch_Records(RECORD_ID)
);

CREATE TABLE Other(
	Record_ID INT	NOT NULL	UNIQUE,
	Video_Author VARCHAR(255),
	/*URL VARCHAR(2083),*/
	PRIMARY KEY(Record_ID),
	Foreign KEY (RECORD_ID) REFERENCES Watch_Records(RECORD_ID)
);


