from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)


engine = create_engine('sqlite:///auditions.db', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    character_name = Column(String)
    auditions = relationship("Audition", back_populates="role")

    def __repr__(self):
        return f"<Role(id={self.id}, character_name='{self.character_name}')>"

    @property
    def auditions(self):
        return session.query(Audition).filter_by(role_id=self.id).all()

    @property
    def actors(self):
        return [audition.actor for audition in self.auditions]

    @property
    def locations(self):
        return [audition.location for audition in self.auditions]

    @property
    def lead(self):
        hired_auditions = [
            audition for audition in self.auditions if audition.hired]
        if hired_auditions:
            return hired_auditions[0]
        else:
            return 'No actor has been hired for this role'

    @property
    def understudy(self):
        hired_auditions = [
            audition for audition in self.auditions if audition.hired]
        if len(hired_auditions) >= 2:
            return hired_auditions[1]
        else:
            return 'No actor has been hired for understudy for this role'


class Audition(Base):
    __tablename__ = 'auditions'

    id = Column(Integer, primary_key=True)
    actor = Column(String)
    location = Column(String)
    hired = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship("Role", back_populates="auditions")

    role = relationship("Role", back_populates="auditions")

    def __repr__(self):
        return f"<Audition(id={self.id}, actor='{self.actor}', location='{self.location}', hired={self.hired}, role_id={self.role_id})>"

    def call_back(self):
        self.hired = True


Base.metadata.create_all(engine)
