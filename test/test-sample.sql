--Professor got promoted
UPDATE PROFESSOR
SET title = 'Professor'
WHERE netid='avm10';

--Professor adds an interest
--INSERT INTO INTEREST VALUES('avm10', 'Machine Learning');

--Professor removes an interest
DELETE FROM INTEREST
WHERE netid = 'avm10' AND field = 'Differential Privacy';

--Browse all departments
SELECT name FROM Department;

--Browse all fields
SELECT DISTINCT field FROM INTEREST;

--Find the fields of interests for a specific person according to their netid
SELECT field FROM INTEREST WHERE netid = 'avm10';

--As a professor, find the netid of students from specific status and start_year who are interested in his fields of interests
SELECT DISTINCT Student.netid FROM Student, Interest as I1, Interest as I2, Professor WHERE status = 'Undergraduate' AND start_year = 2015 AND student.netid = i1.netid AND i2.netid = 'avm10' AND i1.field = i2.field;

--As a student, find the netid of professors who have interests in ML
SELECT DISTINCT Professor.netid FROM Professor, INTEREST WHERE field = 'Machine Learning' AND PROFESSOR.netid = INTEREST.netid;

--As a professor, find the netid of students who have interests in ML
SELECT DISTINCT Student.netid FROM Student, INTEREST WHERE field = 'Machine Learning' AND Student.netid = INTEREST.netid;

--Find the name of professors in a certain department and their emails
SELECT DISTINCT first_name, last_name, email FROM People, Professor, Member WHERE People.netid = Professor.netid AND Professor.netid = Member.netid AND Member.dept_id = 'COMPSCI';

--Find the name of students in a specific department and their emails.
SELECT DISTINCT first_name, last_name, email FROM People, Student, Member WHERE People.netid = Student.netid AND Student.netid = Member.netid AND Member.dept_id = 'COMPSCI';


