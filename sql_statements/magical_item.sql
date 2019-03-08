CREATE TABLE Magical_item(
  dci_number INT NOT NULL,
  character_name VARCHAR(30),
  name VARCHAR(30),
  quantity VARCHAR(30),
  date_acquired INT,
  PRIMARY KEY (dci_number, character_name, name)
);

