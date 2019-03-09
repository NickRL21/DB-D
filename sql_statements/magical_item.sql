CREATE TABLE MAGICAL_ITEM(
  dci_number INT NOT NULL,
  character_name VARCHAR(30),
  p_name VARCHAR(30),
  quantity VARCHAR(30),
  date_acquired DATE,
  PRIMARY KEY (dci_number, character_name, p_name)
);

