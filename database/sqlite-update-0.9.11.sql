BEGIN;

ALTER TABLE Confutatis_User RENAME TO Confutatis_UserOld;

CREATE TABLE Confutatis_User (
        login TEXT NOT NULL PRIMARY KEY,
        lang TEXT NULL,
        password TEXT NULL,
        email TEXT NULL
);

INSERT INTO Confutatis_User(login, password, email) SELECT login, password, email FROM Confutatis_UserOld;
DROP TABLE Confutatis_UserOld;

UPDATE Confutatis_Version SET version='0.9.11';

COMMIT;

