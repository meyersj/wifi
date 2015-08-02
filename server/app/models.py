from app import db


class Manuf(db.Model):
    __tablename__ = 'manuf'
    manuf_id = db.Column(db.Integer, primary_key=True)
    prefix = db.Column(db.String)
    shortm = db.Column(db.String)
    longm = db.Column(db.String)


class Stream(db.Model):
    __tablename__ = 'stream'
    data_id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String)
    sensor = db.Column(db.String)
    arrival = db.Column(db.Numeric, nullable=False)
    mac = db.Column(db.String, nullable=False)
    manuf = db.Column(db.String)
    subtype = db.Column(db.String)
    seq = db.Column(db.Integer)
    signal = db.Column(db.Integer)
    
    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)
        prefix = kwargs["mac"][0:8].upper()
        manuf = Manuf.query.filter_by(prefix=prefix.upper()).first()
        if manuf:
            self.manuf = manuf.shortm
        
    


