-- CREATE DATABASE knights;
-- use knights;

-- CREATE TABLE favorite_colors (
--   name VARCHAR(20),
--   color VARCHAR(10)
-- );

-- INSERT INTO favorite_colors
--   (name, color)
-- VALUES
--   ('Lancelot', 'blue'),
--   ('Galahad', 'yellow');

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