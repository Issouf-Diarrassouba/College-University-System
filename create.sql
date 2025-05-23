-- Active: 1682192381449@@instructor-1.cq4bugepeexy.us-east-1.rds.amazonaws.com@3306@university

use university;

SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS gradrequests;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS phdthesis;
DROP TABLE IF EXISTS recommendationletters;
DROP TABLE IF EXISTS c_catalogue;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS GREadvanced;
DROP TABLE IF EXISTS form1; 
DROP TABLE IF EXISTS c_history; 
DROP TABLE IF EXISTS phdthesis; 
DROP TABLE IF EXISTS studentapplicationreviews;
DROP TABLE IF EXISTS c_schedule;
DROP TABLE IF EXISTS transcript;
drop table if exists faculty; 
drop table if exists alumni;

DROP TABLE IF EXISTS studentapplication; 
DROP TABLE IF EXISTS advising_form;

CREATE TABLE users (
    uid int(8) NOT NULL, 
    email varchar(50),
    password varchar(20), 
    firstname varchar(50),
    lastname varchar(50), 
    address varchar (250), 
    type varchar(50), 
    status varchar(70), 
    ssn int (9), 
    UNIQUE (ssn), 
    UNIQUE(email),
    PRIMARY KEY (uid)
);

CREATE TABLE students (
    uid int(8) NOT NULL,
    advisor_id int(8),  -- Allow NULL values for advisor_id
    enrolledas VARCHAR(50),
    suspended integer,
    advising_status int(1),
    form_status int(1),
    FOREIGN KEY (advisor_id) REFERENCES users(uid), 
    PRIMARY KEY(uid)
);

CREATE TABLE advising_form(
    uid int(8) NOT NULL,
    cid int(8) NOT NULL,
    Foreign Key (uid) REFERENCES users(uid), 
    Foreign Key (cid) REFERENCES c_catalogue(cid)
);

create table faculty(
    uid int(8), 
    advisor boolean,
    grad_sec boolean, 
    cac boolean, 
    reviewer boolean, 
    registrar boolean,
    Foreign Key (uid) REFERENCES users(uid)
);

CREATE TABLE studentapplication (
  firstname varchar(30), 
  lastname varchar(30),
  studentUID int(8),
  gender varchar(30),
  addressline1 varchar(255),
  zipcode varchar(255),
  status varchar(255),
  datesubmitted varchar(255),
  semester varchar(255),
  appYear varchar(255),
  areasofinterest varchar(255),
  experience varchar(255),
  transcript varchar(255),
  priordegrees varchar(255),
  gpa varchar(255),
  major varchar(255),
  gradyear int,
  university varchar(255), 
  recommendedadvisor varchar(255),
  decision varchar(255), 
  degreeType varchar(255),
  GREVerbal varchar(255),
  GREAdvanced varchar(255),
  GRESubject varchar(255),
  GREQuantitative varchar(255),
  GREYear varchar(255),
  TOEFLscore varchar(90),
  TOEFLdate timestamp,
  FOREIGN KEY (studentUID) REFERENCES users(uid)
);

CREATE TABLE recommendationletters (
  studentUID int(8),
  rating int,
  generic boolean,
  credible boolean,
  sender varchar(255),
  title varchar(255),
  affiliation varchar(255),
  senderemail varchar(255),
  letter varchar(400),
  letterID int NOT NULL AUTO_INCREMENT,
  FOREIGN KEY (studentUID) REFERENCES users (uid),
  PRIMARY KEY (letterID)
);


CREATE TABLE studentapplicationreviews (
  workerID int(8),
  studentUID int(8),
  rating int,
  deficiencycourses varchar(255),
  reasonsforreject varchar(255),
  comments varchar(40),
  FOREIGN KEY (workerID) REFERENCES users (uid),
  FOREIGN KEY (studentUID) REFERENCES users (uid)
);

CREATE TABLE transcript (
  studentUID int(8),
  recieved varchar(50),
  sender varchar(255),
  title varchar(255),
  affiliation varchar(255),
  senderemail varchar(255),
  letter varchar(400),
  letterIDs int NOT NULL AUTO_INCREMENT,
  FOREIGN KEY (studentUID) REFERENCES users (uid),
  PRIMARY KEY (letterIDs)

);

INSERT INTO transcript VALUES (12312312, '', 'University Of Tulane', 'Registrar Office', 'Previous College', 'tulane@tulane.university', '', NULL);
INSERT INTO recommendationletters VALUES (12312312, NULL, NULL, NULL,'University Of Tulane', 'Registrar Office', 'Previous College', 'tulane@tulane.university', '', NULL);
INSERT INTO recommendationletters VALUES (12312312, NULL, NULL, NULL,'Professor Khalid', 'Department OF Science', 'Tulane University', 'Khalid@tulane.university', '', NULL);
INSERT INTO recommendationletters VALUES (12312312, NULL, NULL, NULL,'Daisy Simons', 'Department of Health', 'Therapists', 'Therapists@tulane.university', '', NULL);


create table phdthesis(
    uid     int(8) not null,
    thesis      VARCHAR(255),
    approved    int(1),
    Foreign Key (uid) REFERENCES users(uid)
);

create table c_schedule(
    cid    int(8) not null,
    day      VARCHAR(50),
    time    VARCHAR(50),
    Foreign Key (cid) REFERENCES course_catalogue(cid)
);

create table gradrequests(
    advisee_id int(8) not null,
    advisor_id  int(8) not null,
    approved  int(1), 
    Foreign Key (advisee_id) REFERENCES students(uid),
    Foreign Key (advisor_id) REFERENCES users(uid)
);

create table c_catalogue(
    cid int(8) PRIMARY KEY,
    dept VARCHAR(10),
    cnum INT(4),
    title VARCHAR(20),
    sem VARCHAR(20),
    year VARCHAR(4),
    cred INT(8),
    prone VARCHAR(9),
    prtwo VARCHAR(9),
    cap INT(8),
    loc VARCHAR(50),
    snum int(8)

);

 
create table c_history(
    uid int(8), 
    cid int(8),
    fgrade VARCHAR(8), 
    sem VARCHAR(4), 
    year VARCHAR(4),
    snum int(8), -- the course instructors id
    foreign key(cid) references c_catalogue(cid)
); 

create table form1(
    uid int(8),
    cid int(8), 
    Foreign Key (uid) REFERENCES users(uid), 
    Foreign Key (cid) REFERENCES c_catalogue(cid)
);

create table alumni(
    uid int(8), 
    enrolledas VARCHAR(50), 
    gradYear int(4), 
    gradSem varchar(1),
    Foreign Key (uid) REFERENCES users(uid)
);


INSERT INTO c_catalogue
VALUES (1, 'CSCI', 6221, "SW Paradigms", "F", "2023", 3, null, null,50,"GEL",88888888);
INSERT INTO c_catalogue
VALUES (2,'CSCI',6461,"Computer Architecture", "F", "2023", 3, null, null, 50, "TOMP",50505050);
INSERT INTO c_catalogue
VALUES (3,'CSCI',6212,"Algorithms","F","2023",3,null,null,50,"GEL",91217439);
INSERT INTO c_catalogue
VALUES (4,'CSCI',6220,"Machine Learning","F","2023",3,null,null,50,"TOMP",88888888);
INSERT INTO c_catalogue
VALUES (5,'CSCI',6232,"Networks 1","F","2023",3,null,null,50,"SEH",88888888);
INSERT INTO c_catalogue
VALUES (6,'CSCI',6233,"Networks 2","F","2023",3,"CSCI 6232",null,50,"SEH",88888888);
INSERT INTO c_catalogue
VALUES (7,'CSCI',6241,"Database 1","F","2023",3,null,null,50,"SEH",88888888);
INSERT INTO c_catalogue
VALUES (8,'CSCI',6242,"Database 2","F","2023",3,"CSCI 6241",null,50,"SEH",88888888);
INSERT INTO c_catalogue
VALUES (9,'CSCI',6246,"Compilers","F","2023",3,"CSCI 6461","CSCI 6212",50,"TOMP",88888888);
INSERT INTO c_catalogue
VALUES (10,'CSCI',6260,"Multimedia","F","2023",3,null,null,50,"SEH",88888888);
INSERT INTO c_catalogue
VALUES (11,'CSCI',6251,"Cloud Computing","F","2023",3,"CSCI 6461",null,50,"SEH",88888888);
INSERT INTO c_catalogue
VALUES (12,'CSCI',6254,"SW Engineering","F","2023",3,"CSCI 6221",null,50,"SEH",88888888);
INSERT INTO c_catalogue
VALUES (13,'CSCI',6262,"Graphics 1","F","2023",3,null,null,50,"SEH",88888888);
INSERT INTO c_catalogue
VALUES (14,'CSCI',6283,"Security 1","F","2023",3,"CSCI 6212",null,50,"SEH",88888888);
INSERT INTO c_catalogue
VALUES (15,'CSCI',6284,"Cryptography","F","2023",3,"CSCI 6212",null,50,"SEH",88888888);
INSERT INTO c_catalogue
VALUES (16,'CSCI',6286,"Network Security","F","2023",3,"CSCI 6283","CSCI 6232",50,"SEH",88888888);
INSERT INTO c_catalogue
VALUES (17,'CSCI',6325,"Algorithms 2","F","2023",3,"CSCI 6212",null,50,"SEH",88888888);
INSERT INTO c_catalogue
VALUES (18,'CSCI',6339,"Embedded Systems","F","2023",3,"CSCI 6461","CSCI 6212",50,"SEH",88888888);
INSERT INTO c_catalogue
VALUES (19,'CSCI',6384,"Cryptography 2","F","2023",3,"CSCI 6241",null,50,"TOMP",88888888);
INSERT INTO c_catalogue
VALUES (20,'ECE',6241,"Communication Theory","F","2023",3,null,null,50,"TOMP",88888888);
INSERT INTO c_catalogue
VALUES (21,'ECE',6242,"Information Theory","F","2023",3,null,null,50,"GEL",88888888);
INSERT INTO c_catalogue
VALUES (22,'MATH',6210,"Logic","F","2023",3,null,null,50,"GEL",88888888);


INSERT INTO c_schedule VALUES ( 1, 'M', "1500-1730" );
INSERT INTO c_schedule VALUES ( 2, 'T', "1500-1730" );
INSERT INTO c_schedule VALUES ( 3, 'W', "1500-1730" );
INSERT INTO c_schedule VALUES ( 4, 'M', "1800-2030" );
INSERT INTO c_schedule VALUES ( 5, 'T', "1800-2030" );
INSERT INTO c_schedule VALUES ( 6, 'W', "1800-2030" );
INSERT INTO c_schedule VALUES ( 7, 'W', "1800-2030" );
INSERT INTO c_schedule VALUES ( 8, 'R', "1800-2030" );
INSERT INTO c_schedule VALUES ( 9, 'T', "1500-1730" );
INSERT INTO c_schedule VALUES ( 10, 'M', "1800-2030" );
INSERT INTO c_schedule VALUES ( 11, 'M', "1530-1800" );
INSERT INTO c_schedule VALUES ( 12, 'R', "1800-2030" );
INSERT INTO c_schedule VALUES ( 13, 'W', "1800-2030" );
INSERT INTO c_schedule VALUES ( 14, 'T', "1800-2030" );
INSERT INTO c_schedule VALUES ( 15, 'M', "1800-2030" );
INSERT INTO c_schedule VALUES ( 16, 'W', "1800-2030" );
INSERT INTO c_schedule VALUES ( 17, 'W', "1500-1730" );
INSERT INTO c_schedule VALUES ( 18, 'M', "1800-2030" );
INSERT INTO c_schedule VALUES ( 19, 'T', "1800-2030" );
INSERT INTO c_schedule VALUES ( 20, 'W', "1800-2030" );
INSERT INTO c_schedule VALUES ( 21, 'R', "1600-1830" );
INSERT INTO c_schedule VALUES ( 22, 'T', "1600-1830" );

--some dummy data to fix ads
insert into users values(109999999, 'ryanreynolds@gwu.edu', 'adminpass', 'Ryan', 'Reynolds', "yo mama's house", 'Systems Administrator', null, 987654321);
insert into users values(88833888, 'drpepper@gwu.edu', 'adminpass', 'dr', 'pepper', 'ur mom st', 'Faculty',null, 123456789 );
insert into users values (77733377, 'advisor@gwu.edu', 'adminpass', 'Faculty', 'Advisor', 'ur mom ave', 'Faculty', null, 333333333 ); 
insert into faculty values(77733377, true, false,  false, false, false );
insert into faculty values(88833888, false, true,  false, false, false );
insert into faculty values(109999999, true, true,  true, true, true );
insert into users values(89062222, 'advisor2@gwu.edu', 'adminpass', 'Faculty2', 'Advisor2', 'ur mom ave2', 'Faculty', null, 647382916 ); 
insert into users values (55355555, 'talia@gwu.edu', 'adminpass','Talia', 'Novack', '2115 F. St. NW', 'Student', 'Admitted', 999999999);
insert into users values (55555585, 'coffee@gwu.edu', 'adminpass','Coffee', 'Coffee', '2115 F. St. NW', 'Student', 'Admitted', 999099999);
insert into students values(55555585, 77733377, 'PhD', 0,0,0);
insert into students values(55355555, 77733377, 'Masters', 0,0,0);
insert into c_history values(55355555,1, 'A', 'F', 2023, 0); 
insert into c_history values(55355555,2, 'A', 'F', 2023, 0);
insert into c_history values(55355555,3, 'A', 'F', 2023, 0);
insert into c_history values(55355555,4, 'A', 'F', 2023, 0);
insert into c_history values(55555555,5, 'A', 'F', 2023, 0);
insert into phdthesis values(55555585, 'test thesis', 1);

insert into users values (36475863, 'alum@gwu.edu', 'adminpass', 'alumni', 'person', 'seh', 'Alumni', 'Admitted', 999889999);
insert into alumni values(36475863, 'PhD', 2023, 'S');

insert into users values (36478863, 'alum2@gwu.edu', 'adminpass', 'alumni2', 'person', 'seh basement', 'Alumni', 'Admitted', 999880999);
insert into alumni values(36478863, 'Masters', 2022, 'F');


--dummy data from the spec 
--narahari 
insert into users values(50505050, 'bn@mcu.edu', 'adminpass', 'Professor', 'Narahari', 'a house', 'Faculty', null, 068983937);
insert into faculty values(50505050, true, false, false, true, false); 

--choi 
insert into users values(91217439, 'choi@mcu.edu', 'adminpass', 'Professor', 'Choi', 'a home', 'Faculty', null, 587132839 );
insert into faculty values(91217439, false, false, false, false, false); 

--parmer
insert into users values(51515151, 'parmer@mcu.edu', 'adminpass', 'Professor', 'Parmer', 'Elliot', 'Faculty', null, 836760235);
insert into faculty values(51515151, true, false, false, false, false);

--CAC????
insert into users values(30253003, 'elvis@mcu.edu', 'adminpass', 'Elvis', 'Presley', 'Graceland', 'Faculty', null, 102995910); 
insert into faculty VALUES(30253003, false, false, true, false, false);


---REGS STARTING DATA
--billie holiday
insert into users values(88888888, 'billie@mcu.edu', 'adminpass', 'Billie', 'Holiday', 'Ill be seeing you', 'Student', 'Admitted', 295741305 );
insert into students values(88888888, NULL, 'Masters', 0, 1, 1);
insert into c_history values(88888888, 2, 'IP', 'F', 2023,50505050); 

insert into c_history values(88888888, 3, 'IP', 'F', 2023,91217439); 
--Diana Krall
insert into users values(99999999, 'diana@mcu.edu', 'adminpass', 'Diana', 'Krall', 'SEH 4th Floor', 'Student', 'Admitted',  688205810);
insert into students values(99999999, NULL, 'Masters', 0,0,0);

--APPS STARTING DATA
--John Lennon  
insert into users values(12312312, 'johnlennon@mcu.edu', 'adminpass', 'John', 'Lennon', "Yoko's House", 'Applicant', 'Application, Transcript and Recomendation Letters Complete',  111111111);
INSERT INTO studentapplication VALUES ('John', 'Lennon', 12312312, 'male', 'MilkyWay Avenue', '20054', 'Application, Transcript and Recommendation Letters Complete', '2022-11-11', 'fall', '2023', 'Computer Science and Economics', 'Working at Wall Street', '', 'Bachelors (BS)', '2.4', 'Computer Science', 2018, 'Tufts University', '', '', 'Masters', '', '', '', '', '', 60, '2019');
--ringo starr
insert into users values(66666666, 'ringo@mcu.edu', 'adminpass', 'Ringo', 'Starr', 'Drums Avenue', 'Applicant', 'Not Started',  222111111);

INSERT INTO transcript VALUES (12312312, '', 'University Of Tulane', 'Registrar Office', 'Previous College', 'tulane@tulane.university', '', NULL);

INSERT INTO recommendationletters VALUES (12312312, NULL, NULL, NULL, 'University Of Tulane', 'Registrar Office', 'Previous College', 'tulane@tulane.university', '', NULL);

INSERT INTO recommendationletters VALUES (12312312, NULL, NULL, NULL,'Professor Khalid', 'Department OF Science', 'Tulane University', 'Khalid@tulane.university', '', NULL);
INSERT INTO recommendationletters VALUES (12312312, NULL, NULL, NULL,'Daisy Simons', 'Department of Health', 'Therapists', 'Therapists@tulane.university', '', NULL);
--ADS STARTING DATA 
--paul
insert into users values(55555555, 'paul@mcu.edu', 'adminpass', 'Paul', 'McCartney', 'Penny Lane', 'Student', 'Admitted', 491936718 ); 
insert into students values(55555555,50505050, 'Masters', 0, 1,1);
insert into c_history values(55555555, 1, 'A', 'S', 2023, 0); 
insert into c_history values(55555555, 3, 'A', 'S', 2022, 91217439); 

insert into c_history values(55555555, 2, 'A', '', 2023, 50505050); 
insert into c_history values(55555555, 5, 'A', 'S', 2023, 0); 
insert into c_history values(55555555, 6, 'A', 'S', 2023, 0); 

insert into c_history values(55555555, 7, 'B', 'S', 2023, 0); 
insert into c_history values(55555555, 9, 'B', 'S', 2023, 0); 
insert into c_history values(55555555, 13, 'B', 'S', 2023, 0); 
insert into c_history values(55555555, 14, 'B', 'S', 2023, 0); 
insert into c_history values(55555555, 8, 'B', 'S', 2023, 0); 

--george
insert into users values(66666667, 'george@mcu.edu', 'adminpass', 'George', 'Harrison', 'Strawberry Fields', 'Student', 'Admitted', 509250028 );
insert into students values(66666667, 51515151, 'Masters', 0, 1,1);
insert into c_history values(66666667, 21, 'C', 'F', 2023, 0);
insert into c_history values(66666667, 1, 'B', 'S', 2023, 0);
insert into c_history values(66666667, 2, 'B', 'S', 2023, 50505050);
insert into c_history values(66666667, 3, 'B', 'S', 2023, 91217439);
insert into c_history values(66666667, 5, 'B', 'S', 2023, 0);
insert into c_history values(66666667, 6, 'B', 'S', 2023, 0);
insert into c_history values(66666667, 7, 'B', 'S', 2023, 0);
insert into c_history values(66666667, 8, 'B', 'S', 2023, 0);
insert into c_history values(66666667, 14, 'B', 'S', 2023, 0);
insert into c_history values(66666667, 15, 'B', 'S', 2023, 0);

--ringo2
insert into users values(66666689, 'ringo2@mcu.edu','adminpass', 'Ringo2', 'Starr', 'Glass Onion Way', 'Student', 'Admitted',  831055135 ); 
insert into students values(66666689, 51515151, 'PhD', 0,1,1);
insert into phdthesis values(66666689, "Desmond has a barrow in the marketplace Molly is the singer in a bandDesmond says to Molly, 'Girl, I like your face'And Molly says this as she takes him by the handOb-la-di, ob-la-daLife goes on, brahLa, la, how the life goes onOb-la-di, ob-la-daLife goes on, brahLa, la, how the life goes onDesmond takes a trolley to the jeweler's storeBuys a 20 carat golden ring (ring)Takes it back to Molly waiting at the door And as he gives it to her, she begins to sing (sing)", 0);
insert into c_history values(66666689, 1, 'A','F', 2022, 0); 
insert into c_history values(66666689, 2, 'A','F', 2022, 50505050); 
insert into c_history values(66666689, 3, 'A','F', 2022, 91217439); 
insert into c_history values(66666689, 4, 'A','F', 2022, 0); 
insert into c_history values(66666689, 5, 'A','F', 2022, 0); 
insert into c_history values(66666689, 6, 'A','F', 2022, 0);
insert into c_history values(66666689, 7, 'A','F', 2022, 0); 
insert into c_history values(66666689, 8, 'A','F', 2022, 0); 
insert into c_history values(66666689, 9, 'A','F', 2022, 0); 
insert into c_history values(66666689, 10, 'A','F', 2022, 0); 
insert into c_history values(66666689, 11, 'A','F', 2022, 0); 
insert into c_history values(66666689, 12, 'A','S', 2023, 0); 

--eric clapton 
insert into users values(77777777, 'eric@mcu.edu', 'adminpass', 'Eric', 'Clapton', 'Tears in Heaven Blvd','Alumni', 'Admitted', 681782622);
insert into alumni values(77777777, 'Masters', 2014, 'S'); 
insert into c_history values(77777777, 1, 'B', 'S', 2013, 0); 
insert into c_history values(77777777, 3, 'B', 'S', 2012, 91217439); 

insert into c_history values(77777777, 2, 'B', 'F', 2012, 50505050); 
insert into c_history values(77777777, 5, 'B', 'S', 2014, 0); 
insert into c_history values(77777777, 6, 'B', 'S', 2014, 0); 

insert into c_history values(77777777, 7, 'B', 'S', 2014, 0); 
insert into c_history values(77777777, 8, 'B', 'S', 2014, 0);

insert into c_history values(77777777, 14, 'A', 'S', 2014, 0);
insert into c_history values(77777777, 15, 'A', 'S', 2014, 0);
insert into c_history values(77777777, 16, 'A', 'S', 2014, 0);



