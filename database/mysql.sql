DROP TABLE IF EXISTS Confutatis_Version;

CREATE TABLE Confutatis_Version (
	version VARCHAR(255) NOT NULL
);
INSERT INTO Confutatis_Version (version) VALUES('0.9.11');



DROP TABLE IF EXISTS Confutatis_User;

CREATE TABLE Confutatis_User (
	login VARCHAR(32) NOT NULL PRIMARY KEY,
	lang VARCHAR(32) NULL, 
	password VARCHAR(32) NULL,
	email VARCHAR(64) NULL
);



DROP TABLE IF EXISTS Confutatis_Permission;

CREATE TABLE Confutatis_Permission (
	login VARCHAR(32) NOT NULL,
	permission VARCHAR(32) NOT NULL
);

CREATE INDEX confutatis_permission_index_login ON Confutatis_Permission (login);


DROP TABLE IF EXISTS Confutatis_Session;

CREATE TABLE Confutatis_Session (
	sessionid VARCHAR(128) NOT NULL PRIMARY KEY,
	login VARCHAR(32) NOT NULL,
	time DATETIME NOT NULL
);

CREATE INDEX confutatis_session_index_login ON Confutatis_Session (login);


DROP TABLE IF EXISTS Confutatis_Filter;

CREATE TABLE Confutatis_Filter (
	id BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
	login VARCHAR(32) NOT NULL,
	name VARCHAR(64) NOT NULL,
	comment VARCHAR(255) NULL,
	formula VARCHAR(255) NOT NULL
);

CREATE UNIQUE INDEX confutatis_filter_index_login_name ON Confutatis_Filter (login, name);


DROP TABLE IF EXISTS Confutatis_Filter_Criterion;

CREATE TABLE Confutatis_Filter_Criterion (
	id BIGINT UNSIGNED NOT NULL,
	name VARCHAR(16) NOT NULL,
	path VARCHAR(255) NOT NULL,
	operator VARCHAR(8) NULL,
	value VARCHAR(255) NULL
);

CREATE INDEX confutatis_filter_criterion_index_id ON Confutatis_Filter_Criterion (id);


DROP TABLE IF EXISTS Confutatis_User_Configuration;
CREATE TABLE Confutatis_User_Configuration (
	login VARCHAR(32) NOT NULL,
	view  VARCHAR(32) NOT NULL,
	name  VARCHAR(255) NOT NULL,
	value VARCHAR(255) NULL
);

CREATE INDEX confutatis_user_configuration_index ON Confutatis_User_Configuration (name, login, view);
