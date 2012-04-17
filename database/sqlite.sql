
CREATE TABLE Confutatis_Version (
	version TEXT NOT NULL
);
INSERT INTO Confutatis_Version (version) VALUES('0.9.11');




CREATE TABLE Confutatis_User (
	login TEXT NOT NULL PRIMARY KEY,
	lang TEXT NULL,
	password TEXT NULL,
	email TEXT NULL
);




CREATE TABLE Confutatis_Permission (
	login TEXT NOT NULL,
	permission TEXT NOT NULL
);

CREATE INDEX confutatis_permission_index_login ON Confutatis_Permission (login);



CREATE TABLE Confutatis_Session (
	sessionid TEXT NOT NULL PRIMARY KEY,
	login TEXT NOT NULL,
	time DATETIME NOT NULL
);

CREATE INDEX confutatis_session_index_login ON Confutatis_Session (login);



CREATE TABLE Confutatis_Filter (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	login TEXT NOT NULL,
	name TEXT NOT NULL,
	comment TEXT NULL,
	formula TEXT NOT NULL
);

CREATE UNIQUE INDEX confutatis_filter_index_login_name ON Confutatis_Filter (login, name);



CREATE TABLE Confutatis_Filter_Criterion (
	id INTEGER NOT NULL,
	name TEXT NOT NULL,
	path TEXT NOT NULL,
	operator TEXT NULL,
	value TEXT NULL
);

CREATE INDEX confutatis_filter_criterion_index_id ON Confutatis_Filter_Criterion (id);


CREATE TABLE Confutatis_User_Configuration (
	login TEXT NOT NULL,
	view  TEXT NOT NULL,
	name  TEXT NOT NULL,
	value TEXT NULL
);

CREATE INDEX confutatis_user_configuration_index ON Confutatis_User_Configuration (name, login, view);
