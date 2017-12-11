CREATE TABLE People(netid VARCHAR(10) NOT NULL PRIMARY KEY,
                    first_name VARCHAR(20) NOT NULL,
                    last_name VARCHAR(20) NOT NULL,
                    email VARCHAR(30) NOT NULL,
                    website VARCHAR(50),
                    resume VARCHAR(10), 
                    password VARCHAR (20) NOT NULL,
                    UNIQUE(first_name, last_name, email));

CREATE TABLE Department(id VARCHAR(10) NOT NULL PRIMARY KEY,
                        name VARCHAR(40) NOT NULL UNIQUE);

CREATE TYPE title AS ENUM ('Professor', 'Associate Professor', 'Assistant Professor', 'Lecturer');
CREATE TABLE Faculty(netid VARCHAR(10) NOT NULL PRIMARY KEY REFERENCES People(netid),
                     title title NOT NULL,
                     opening INTEGER NOT NULL CHECK(opening >= 0));

CREATE TYPE status AS ENUM ('Undergraduate', 'Master', 'PhD', 'Post-Doc');
CREATE TABLE Student(netid VARCHAR(10) NOT NULL PRIMARY KEY REFERENCES People(netid),
                     status status NOT NULL,
                     start_year INTEGER NOT NULL CHECK(start_year >= 1838));

CREATE TABLE Member(netid VARCHAR(10) NOT NULL REFERENCES People(netid),
                    dept_id VARCHAR(10) NOT NULL REFERENCES Department(id),
                    PRIMARY KEY(netid, dept_id));

CREATE TABLE Interest(netid VARCHAR(10) NOT NULL REFERENCES People(netid),
                      field VARCHAR(40) NOT NULL,
                      PRIMARY KEY(netid, field));
