\COPY People(netid, first_name, last_name, email, website, resume, password) FROM 'data/People.dat' WITH DELIMITER ',' NULL '' CSV
\COPY Department(id, name) FROM 'data/Department.dat' WITH DELIMITER ',' NULL '' CSV
\COPY Faculty(netid, title, opening) FROM 'data/Faculty.dat' WITH DELIMITER ',' NULL '' CSV
\COPY Student(netid, status, start_year) FROM 'data/Student.dat' WITH DELIMITER ',' NULL '' CSV
\COPY Member(netid, dept_id) FROM 'data/Member.dat' WITH DELIMITER ',' NULL '' CSV
\COPY Interest(netid, field) FROM 'data/Interest.dat' WITH DELIMITER ',' NULL '' CSV
