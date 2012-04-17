UPDATE Confutatis_Version SET version="0.9.1";

DROP TABLE IF EXISTS Confutatis_User_Configuration;
CREATE TABLE Confutatis_User_Configuration (
	login VARCHAR(32) NOT NULL,
	view  VARCHAR(32) NOT NULL,
	name  VARCHAR(255) NOT NULL,
	value VARCHAR(255) NULL
);

CREATE INDEX confutatis_user_configuration_index ON Confutatis_User_Configuration (name, login, view);
