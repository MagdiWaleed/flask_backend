from app import db 
import uuid
class Student(db.Model):
    __tabelname__ ='student'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name= db.Column(db.String, nullable=False)
    gender = db.Column(db.Integer)  
    email = db.Column(db.String, nullable=False)
    student_id = db.Column(db.Integer)
    password = db.Column(db.String,nullable=False)
    level = db.Column (db.Integer, nullable=True)
    profile_pic = db.Column(db.String, nullable=True)
    token = db.Column(db.String,nullable =False)
    
    def __repr__(self):
        return f'<naem:{self.name}>, <level:{self.level}>'

    def generateToken(self):
        self.token = str(uuid.uuid4())    

    def toMap(self):
        return {
            "name":self.name,
            "email":self.email,
            "password":self.password,
            "gender":self.gender,
            "level":self.level,
            "student_id":self.student_id,
            "profile_pic_path":self.profile_pic
        }

    

