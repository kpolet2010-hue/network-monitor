from fastapi import FastAPI
from pydantic import BaseModel
from database import engine
from models import Base
from scapy.all import sniff, IP
import threading
from database import SessionLocal
from models import Packet
from sqlalchemy.orm import Session
from fastapi import Depends
from scapy.all import AsyncSniffer

sniffer = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def handle_packet(pkt):
    if IP in pkt:
        db = SessionLocal()
        try:
            db_packet = Packet(
                source_ip=pkt[IP].src,
                destination_ip=pkt[IP].dst,
                protocol=str(pkt[IP].proto)
            )
            db.add(db_packet)
            db.commit()
        finally:
            db.close()

app = FastAPI()

Base.metadata.create_all(bind=engine)

class PacketRequest(BaseModel):
    source_ip: str
    destination_ip: str
    protocol: str


@app.get("/packets")
def get_packets(db: Session = Depends(get_db)):
    return db.query(Packet).all()


@app.get("/")
def root():
    return {"message": "Database connected"}

@app.post("/packet")
def create_packet(packet: PacketRequest):
    return {
        "message": "packet received",
        "data": packet
    }

@app.post("/start-capture")
def start_capture():
    global sniffer
    if sniffer is None or not sniffer.running:
        sniffer = AsyncSniffer(prn=handle_packet, store=False)
        sniffer.start()
        return {"message": "capture started"}
    return {"message": "capture already running"}

@app.post("/stop-capture")
def stop_capture():
    global sniffer
    if sniffer is not None and sniffer.running:
        sniffer.stop()
        return {"message": "capture stopped"}
    return {"message": "no capture running"}
