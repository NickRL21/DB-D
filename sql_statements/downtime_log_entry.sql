CREATE TABLE DOWNTIME_LOG_ENTRY(
  D_log_ID  INT NOT NULL,
  player_DCI  CHAR(10) NOT NULL,
  character_name  VARCHAR(30),
  dt_date  DATE  NOT NULL,
  delta_downtime  INT,
  delta_gold  FLOAT DEFAULT'0.00',
  delta_TCP_T1 INT,
  delta_TCP_T2 INT,
  delta_TCP_T3 INT,
  delta_TCP_T4 INT,
  delta_ACP INT,
  delta_Renown  INT,
  PRIMARY KEY (D_log_ID, player_DCI, character_name),
  FOREIGN KEY (player_DCI) REFERENCES Player(dci_number),
  FOREIGN KEY (player_dci, character_name) REFERENCES P_CHARACTER(dci_number,p_name)
);