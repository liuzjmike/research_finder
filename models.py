from app import db

class People(db.Model):
    __tablename__ = 'people'
    netid = db.Column('netid', db.String(10), primary_key=True, nullable=False)
    first_name = db.Column('first_name', db.String(20), nullable=False)
    last_name = db.Column('last_name', db.String(20), nullable=False)
    email = db.Column('email', db.String(30))
    db.UniqueConstraint('first_name', 'last_name', 'email', name='name_email')

class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column('id', db.String(10), primary_key=True, nullable=False)
    name = db.Column('name', db.String(40), nullable=False, unique=True)

class Faculty(db.Model):
    __tablename__ = 'faculty'
    netid = db.Column('netid', db.String(10),
                      db.ForeignKey('people.netid'),
                      primary_key=True,
                      nullable=False)
    title = db.Column('title',
                      db.Enum('Professor',
                              'Associate Professor',
                              'Assistant Professor',
                              'Lecturer',
                              name='title'),
                      nullable=False)
    opening = db.Column('opening', db.Integer, nullable=False)
    db.CheckConstraint('opening >= 0', name='opening')

class Student(db.Model):
    __tablename__ = 'student'
    netid = db.Column('netid', db.String(10),
                      db.ForeignKey('people.netid'),
                      primary_key=True,
                      nullable=False)
    status = db.Column('status',
                       db.Enum('Undergraduate',
                               'Master',
                               'PhD',
                               'Post-Doc',
                               name='status'),
                       nullable=False)
    start_year = db.Column('start_year', db.Integer, nullable=False)
    db.CheckConstraint('start_year >= 1838', name='start_year')

class Member(db.Model):
    __tablename__ = 'member'
    netid = db.Column('netid', db.String(10),
                      db.ForeignKey('people.netid'),
                      primary_key=True,
                      nullable=False)
    dept_id = db.Column('dept_id', db.String(10),
                        db.ForeignKey('department.id'),
                        primary_key=True,
                        nullable=False)

class Inerest(db.Model):
    __tablename__ = 'interest'
    netid = db.Column('netid', db.String(10),
                      db.ForeignKey('people.netid'),
                      primary_key=True,
                      nullable=False)
    field = db.Column('field', db.String(40),
                      primary_key=True,
                      nullable=False)
