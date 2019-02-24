CREATE TABLE Player(
  dci_number INT NOT NULL,
  name VARCHAR(30),
  PRIMARY KEY (dci_number)
);

INSERT INTO Player
VALUES (1234, 'nick');

INSERT INTO Player
VALUES (1235, 'coby');

INSERT INTO Player
VALUES (1236, 'greg');

INSERT INTO Player
VALUES (1237, 'olivia');




SELECT * FROM Player;