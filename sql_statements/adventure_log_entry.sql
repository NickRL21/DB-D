-- ADVENTURE_LOG_ENTRY
CREATE TABLE ADVENTURE_LOG_ENTRY(
  A_log_id  INT NOT NULL,
  player_DCI INT NOT NULL,
  character_name VARCHAR(30),
  advanture_name CHAR,
  date DATE NOT NULL,
  delta_downtime  INT,
  delta_TCP_T1 INT,
  delta_TCP_T2 INT,
  delta_TCP_T3 INT,
  delta_TCP_T4 INT,
  delta_gold DOUBLE DEFAULT 0.0,
  delta_ACP INT,
  PRIMARY KEY (A_log_id, player_DCI, character_name)
  FOREIGN KEY (player_DCI) REFERENCES Player(dci_number),
  FOREIGN KEY (character_name) REFERENCES character(name)
);

-- TEST DATA:

insert into ADVENTURE_LOG_ENTRY values (1,1422314756,'Thorun','Dragon Heist',2017-6-23,5,2,0,0,0,10,2);
insert into ADVENTURE_LOG_ENTRY values (2,1422314756,'Thorun','Tales From The Yawning Portal',2017-8-10,5,2,0,0,0,10,2);
insert into ADVENTURE_LOG_ENTRY values (1,1422314756,'Dorn','Curse Of Strahd',2018-1-23,5,2,0,0,0,10,2);
insert into ADVENTURE_LOG_ENTRY values (2,1422314756,'Dorn','Princes Of The Apocolypse',2018-4-22,5,2,0,0,0,10,2);
