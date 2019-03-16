CREATE TABLE P_CHARACTER(
  dci_number CHAR(10) NOT NULL,
  character_name VARCHAR(30) NOT NULL,
  race VARCHAR(30),
  class VARCHAR(30),
  background VARCHAR(30),
  level INT CHECK(level >= 0 AND level <=20),
  PRIMARY KEY(dci_number, character_name)
);