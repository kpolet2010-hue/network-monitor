from sqlalchemy import Column, Integer, String
from database import Base

class Packet(Base):
    __tablename__ = "packets"

    id = Column(Integer, primary_key=True, index=True)
    source_ip = Column(String)
    destination_ip = Column(String)
    protocol = Column(String)
