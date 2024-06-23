from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """Модель пользователя"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True, nullable=False) # Telegram ID
    full_name = Column(String(20), nullable=False)

    weather = relationship('Weather', back_populates='user')


class Weather(Base):
    """Модель погоды"""
    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String(20), nullable=False)
    temp = Column(Float)
    pressure = Column(Integer)
    grnd_level = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    user = relationship('User', back_populates='weather')