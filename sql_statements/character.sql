CREATE TABLE character(
  dci_number INT NOT NULL,
  name VARCHAR(30) NOT NULL,
  race VARCHAR(30),
  class VARCHAR(30),
  background VARCHAR(30),
  level INT CHECK(level >= 0 AND level <=20),
  PRIMARY KEY(dci_number, name)
);

INSERT INTO character
VALUES ('1234', 'fred', 'human', 'archer', 'none', 10);

SELECT * FROM character;