drop table PLAYER

CREATE TABLE PLAYER(
  dci_number INT NOT NULL,
  p_name VARCHAR(30),
  PRIMARY KEY (dci_number)
);

INSERT INTO PLAYER
VALUES (1234, 'nick');

INSERT INTO PLAYER
VALUES (1235, 'coby');

INSERT INTO PLAYER
VALUES (1236, 'greg');

INSERT INTO PLAYER
VALUES (1237, 'olivia');




SELECT * FROM PLAYER;