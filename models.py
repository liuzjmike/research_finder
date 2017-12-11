from app import db


class People(db.Model):
    __tablename__ = 'people'
    netid = db.Column('netid', db.String(10), primary_key=True, nullable=False)
    first_name = db.Column('first_name', db.String(20), nullable=False)
    last_name = db.Column('last_name', db.String(20), nullable=False)
    email = db.Column('email', db.String(30))
    website = db.Column('website', db.String(50))
    resume = db.Column('resume', db.String(10))
    password = db.Column('password', db.String(20), nullable=False)
    db.UniqueConstraint('first_name', 'last_name', 'email', name='name_email')
    interests = db.relationship('Interest')
    departments = db.relationship('Member')

    @classmethod
    def insert(cls, netid, first_name, last_name, email, website, resume, password):
        try:
            person = cls(netid=netid, first_name=first_name, last_name=last_name,
                         email=email, website=website, resume=resume, password=password)
            db.session.add(person)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def contains(cls, netid):
        user = db.session.query(cls).filter(cls.netid == netid)
        return db.session.query(user.exists()).scalar()

    @classmethod
    def get(cls, netid):
        row = db.session.query(cls).filter(cls.netid == netid)
        if db.session.query(row.exists()).scalar():
            return row.one()
        return None

    @classmethod
    def authenticate(cls, netid, password):
        user = cls.get(netid)
        return user and user.password == password

    @classmethod
    def edit(cls, netid, first_name, last_name, email, website, resume, password):
        try:
            cls.query.filter_by(netid=netid).update(
                dict(first_name=first_name, last_name=last_name,
                     email=email, website=website, resume=resume, password=password))
            db.session.commit()
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
    person = db.relationship('People')

    @classmethod
    def insert(cls, netid, title, opening):
        try:
            faculty = cls(netid=netid, title=title, opening=opening)
            db.session.add(faculty)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def get(cls, netid):
        row = db.session.query(cls).filter(cls.netid == netid)
        if db.session.query(row.exists()).scalar():
            return row.one()
        return None

    @classmethod
    def edit(cls, netid, title, opening):
        try:
            cls.query.filter_by(netid=netid).update(
                dict(title=title, opening=opening))
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

    @classmethod
    def insert(cls, netid, status, start_year):
        try:
            student = cls(netid=netid, status=status, start_year=start_year)
            db.session.add(student)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def get(cls, netid):
        row = db.session.query(cls).filter(cls.netid == netid)
        if db.session.query(row.exists()).scalar():
            return row.one()
        return None

    @classmethod
    def edit(cls, netid, status, start_year):
        try:
            cls.query.filter_by(netid=netid).update(
                dict(status=status, start_year=start_year))
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

    @classmethod
    def insert(cls, netid, dept_id):
        try:
            db.session.add(cls(netid=netid, dept_id=dept_id))
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

    @classmethod
    def insert(cls, netid, interests):
        if interests:
            try:
                db.session.add_all([cls(netid=netid, field=interest)
                                    for interest in interests])
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e

    @classmethod
    def edit(cls, netid, interests):
        try:
            cls.query.filter_by(netid=netid).delete()
            if interests:
                db.session.add_all([cls(netid=netid, field=interest)
                                    for interest in interests])
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
