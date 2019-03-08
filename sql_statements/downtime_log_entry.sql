CREATE TABLE DOWNTIME_LOG_ENTRY(
  D_log_ID  INT NOT NULL,
  player_DCI  INT NOT NULL,
  character_name  VARCHAR(30),
  date  DATE  NOT NULL,
  delta_downtime  INT,
  delta_gold  DOUBLE DEFAULT'0.00',
  delta_TCP_T1 INT,
  delta_TCP_T2 INT,
  delta_TCP_T3 INT,
  delta_TCP_T4 INT,
  delta_ACP INT,
  delta_Renown  INT,
  PRIMARY KEY (D_log_ID, player_DCI, character_name)
  FOREIGN KEY (player_DCI) REFERENCES Player(dci_number),
  FOREIGN KEY (character_name) REFERENCES P_character(name)
);

-- TEST DATA:

insert into DOWNTIME_LOG_ENTRY values (1,1422314756,'Garreth','2017-5-12',0,0,0,0,-5,0,0,-5);
insert into DOWNTIME_LOG_ENTRY values (2,1422314756,'Garreth','2018-8-2',0,0,0,0,-10,0,0,-10);
insert into DOWNTIME_LOG_ENTRY values (1,1422314756,'Thorun','2016-3-17',0,0,0,0,-5,0,0,-5);
insert into DOWNTIME_LOG_ENTRY values (2,1422314756,'Thorun','2017-8-10',0,0,0,0,-10,0,0,-10);
