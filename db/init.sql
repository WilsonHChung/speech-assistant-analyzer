CREATE DATABASE speech_app;
use speech_app;

CREATE TABLE user (
  name varchar(100),
  password varchar(100),
  speech_id int
);

CREATE TABLE speech (
  speech_id int,
  file_name varchar(100),
  time_of_speech int,
  hesitations int,
  language varchar(100)
);

CREATE TABLE speech_to_text (
  stutter_word varchar(100),
  hesitation_id int
);


