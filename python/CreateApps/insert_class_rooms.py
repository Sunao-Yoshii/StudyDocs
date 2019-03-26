# Importing SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound


# Connect Database
engine = create_engine('sqlite:///sample_db.sqlite3', echo=True)


# Create Schema.
Base = declarative_base()

class ClassRoomInfo(Base):
    __tablename__ = 'class_room_info'
    id = Column(Integer, primary_key = True, autoincrement = True)
    title = Column(String(512))
    limit = Column(Integer)
    joins = Column(Integer)

    def __repr__(self):
        return "<ClassRoomInfo(id='%s', title='%s', limit='%s', joins='%s')>" % (self.id, self.title, self.limit, self.joins)


Base.metadata.create_all(engine)


# Import same ClassRoom structures.
from class_rooms import ClassRoom
import pickle

# Loading class room informations.
def load_class_rooms():
    with open('backup.pickle', 'rb') as f:
        return pickle.load(f)

# Convert to entity.
def convert_to_entity(cr: ClassRoom) -> ClassRoomInfo:
    return ClassRoomInfo(title=cr.title, limit=cr.limit, joins=cr.joins)

# Database session start.
Session = sessionmaker(bind=engine)
session = Session()

# Backup class room datas as dmp
datasets = load_class_rooms()

# Isertion to database.
for cr in datasets:
    session.add(convert_to_entity(cr))

# Selection
id50 = session.query(ClassRoomInfo).filter_by(id=50).one()
print(f'ID 50 = {id50}')

# commit
session.commit()

# End of session.
session.close()
