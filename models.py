from app import db 

class Student(db.Model):
    __tabelname__ ='student'

    name= db.Column(db.String, nullable=False)
    gender = db.Column(db.Integer)  
    email = db.Column(db.String, nullable=False, unique=True)
    student_id = db.Column(db.Integer, primary_key=True,unique= True)
    password = db.Column(db.String,nullable=False)
    level = db.Column (db.Integer, nullable=True)

    username = db.Column(db.String,nullable = False)
    password = db.Column(db.String,nullable = False)
    role = db.Column(db.String)
        
    def get_id(self):
        return self.user_id
    

