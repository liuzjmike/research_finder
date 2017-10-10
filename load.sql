\COPY People(netid, first_name, last_name, email) FROM 'data/People.dat' WITH DELIMITER ',' NULL '' CSV
\COPY Department(id, name) FROM 'data/Department.dat' WITH DELIMITER ',' NULL '' CSV
\COPY Professor(netid, title, opening) FROM 'data/Professor.dat' WITH DELIMITER ',' NULL '' CSV
\COPY Student(netid, status, start_year) FROM 'data/Student.dat' WITH DELIMITER ',' NULL '' CSV
\COPY Member(netid, dept_name) FROM 'data/Member.dat' WITH DELIMITER ',' NULL '' CSV
# \COPY Field(field) FROM 'data/Field.dat' WITH DELIMITER ',' NULL '' CSV
\COPY Interest(netid, field) FROM 'data/Interest.dat' WITH DELIMITER ',' NULL '' CSV
