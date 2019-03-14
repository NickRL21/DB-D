CREATE TABLE ADVENTURE_LOG_ENTRY(
  A_log_id  INT NOT NULL,
  player_DCI CHAR(10) NOT NULL,
  character_name VARCHAR(30),
  adventure_name VARCHAR(30),
  a_date DATE NOT NULL,
  delta_downtime  INT,
  delta_TCP_T1 INT,
  delta_TCP_T2 INT,
  delta_TCP_T3 INT,
  delta_TCP_T4 INT,
  delta_gold FLOAT DEFAULT 0.0,
  delta_ACP INT,
  delta_renown INT,
  DM_DCI CHAR(10),
  PRIMARY KEY (A_log_id, player_DCI, character_name),
  FOREIGN KEY (player_DCI) REFERENCES PLAYER(dci_number),
  FOREIGN KEY (player_dci, character_name) REFERENCES P_CHARACTER(dci_number,p_name)
);

