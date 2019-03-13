CREATE TABLE users(
  dci_number CHAR(10) NOT NULL,
  pwd_hash VARCHAR(256) NOT NULL,
  PRIMARY KEY (dci_number)
);