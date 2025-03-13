from app import db 

class Student(db.Model):
    __tabelname__ ='student'

    name= db.Column(db.String, nullable=False)
    gender = db.Column(db.Integer)  
    email = db.Column(db.String, nullable=False, uniqe=True)
    student_id = db.Column(db.Integer, primary=True)
    level = db.Column (db.Integer, nullable=True)
    password = db.Column(db.String,nullable=False)
    confirmPassword = db.Column(db.String,nullable=False)

    username = db.Column(db.String,nullable = False)
    password = db.Column(db.String,nullable = False)
    role = db.Column(db.String)
    

    def __repr__(self):
        return f"Person('{self.name}', '{self.age}')"
    
    def get_id(self):
        return self.user_id
    

