from fastapi import FastAPI
from pydantic import BaseModel
from database import engine
from models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

class PacketRequest(BaseModel):
    source_ip: str
    destination_ip: str
    protocol: str

@app.get("/")
def root():
    return {"message": "Database connected"}

@app.post("/packet")
def create_packet(packet: PacketRequest):
    return {
        "message": "packet received",
        "data": packet
    }