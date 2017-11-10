from app import db

class People(db.Model):
    __tablename__ = 'people'
    netid = db.Column('netid', db.String(10), primary_key=True, nullable=False)
    first_name = db.Column('first_name', db.String(20), nullable=False)
    last_name = db.Column('last_name', db.String(20), nullable=False)
    email = db.Column('email', db.String(30))
    db.UniqueConstraint('first_name', 'last_name', 'email', name='name_email')

    def insert(netid, first_name, last_name, email):
        try:
            db.session.execute('INSERT INTO People (netid, first_name, last_name, email) VALUES (:netid, :first_name, :last_name, :email)')
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    def doesUserExist(netid):
        try:
            result = db.engine.execute('SELECT * FROM People WHERE (netid= :netid)')
            if len(result > 0):
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise e
    def validateUser(netid, password):
        try:
            result = db.engine.execute('SELECT * FROM People WHERE (netid= :netid AND password= :password)')
            if len(result > 0):
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise e

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

    def insert(netid, title, opening, personal_web):
        try:
            db.session.execute('INSERT INTO Faculty (netid, title, opening, personal_web) VALUES (:netid, :title, :opening, :personal_web)')
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

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

    def insert(netid, status, start_year):
        try:
            db.session.execute('INSERT INTO Student (netid, status, start_year) VALUES (:netid, :status, :start_year)')
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

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

    def insert(netid, dept_id):
        try:
            db.session.execute('INSERT INTO Member (netid, dept_id) VALUES (:netid, :dept_id)')
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

class Interest(db.Model):
    __tablename__ = 'interest'
    netid = db.Column('netid', db.String(10),
                      db.ForeignKey('people.netid'),
                      primary_key=True,
                      nullable=False)
    field = db.Column('field', db.String(40),
                      primary_key=True,
                      nullable=False)

    def insert(netid, interests):
        try:
            for interest in interests:
                db.session.execute('INSERT INTO Interest (netid, interest) VALUES (:netid, :interest)')
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
