CREATE TABLE MAGICAL_ITEM(
  dci_number CHAR(10) NOT NULL,
  character_name VARCHAR(30),
  item_name VARCHAR(30),
  quantity VARCHAR(30),
  date_acquired DATE,
  PRIMARY KEY (dci_number, character_name, item_name)
);

