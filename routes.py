from flask import request,jsonify
from models import Student, Store, StudentStoresRelation
from werkzeug.utils import secure_filename
import json
import os


def register_routes(app, db):
    @app.route('/login/',methods=['POST'])
    def login():
        data = request.get_json()
        student = Student.query.filter( Student.email == data['email']).first()
        print(data['email'])
        if not student:
            return jsonify({'error': 'There Is No Student With This Email'}), 400
            
        if student.password != data['password'] :
            return jsonify({"error": 'Wrong Password'}), 400
        return jsonify({'message':'Login Successfully','token':student.token})
    
    @app.route('/signup/',methods=['POST'])
    def signup():
        data = request.get_json()
        email = data['email']
        name = data ['name']
        student_id = data ['student_id']
        password = data['password']

        
        
        is_exist = Student.query.filter(Student.email == email).first()
        print(email)
        if is_exist:
            return jsonify({"error": "There Are Already Account With This Email"}),400 
        level,gender = False, False

        if 'level' in data:
            level = True
        if 'gender' in data:
            gender =True

        student = Student(
            email=email,
            name = name,
            student_id= student_id,
            password= password,
        )

        print("data['gender']",data['gender'])
        if level:
            student.level= data['level']
        if gender:
            student.gender= data['gender']

        student.generateToken()

        db.session.add(student)
        db.session.commit()

        return jsonify({'message':"User Created Successfully","token":student.token})
    
    @app.route("/getstudentdata/",methods=['GET'])
    def getStudentData():
        token = request.headers['Authorization']
        student = Student.query.filter(Student.token==token).first()
        if not student:
            return jsonify({'error': 'You Are Not Authorized'}), 400
        return jsonify(student.toMap())
    
    @app.route("/updatestudentdata/",methods=["PUT"])
    def updateStudentData():
        token = request.headers['Authorization']
        data = json.loads(request.form['data'])
        
        student = Student.query.filter(Student.token == token).first()
        email = data['email']
        name = data ['name']
        student_id = data ['student_id']
        password = data['password']
        
        is_exist_student = Student.query.filter(Student.email == email).first()
        if is_exist_student:
            if is_exist_student.token != token:
                return jsonify({"error":"This Email Is Used"}), 400
        
        level,gender = False, False
        try:
            if 'level' in data:
                level = True
            if 'gender' in data:
                gender =True

    
            if 'profile_pic_path' in request.files:
                
                if student.profile_pic and student.profile_pic != 'DEFAULT_PROFILE_IMAGE.png':
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'],"profile_pics",student.profile_pic))

                    profile_pic = request.files['profile_pic_path']
                    profile_pic_name = secure_filename(profile_pic.filename)
                    profile_pic_path = os.path.join(app.config['UPLOAD_FOLDER'],"profile_pics",profile_pic_name)
                    print(profile_pic_name)
                    profile_pic.save(profile_pic_path)
                    student.profile_pic = profile_pic_name
                
                elif not student.profile_pic and student.profile_pic != 'DEFAULT_PROFILE_IMAGE.png':
                    profile_pic = request.files['profile_pic_path']
                    profile_pic_name = secure_filename(profile_pic.filename)
                    profile_pic_path = os.path.join(app.config['UPLOAD_FOLDER'],"profile_pics",profile_pic_name)
                    profile_pic.save(profile_pic_path)
                    student.profile_pic = profile_pic_name

            
            elif 'profile_pic_path' in data:
                if student.profile_pic and data['profile_pic_path'] == "DELETE" :
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'],"profile_pics",student.profile_pic))
                    student.profile_pic = None


            student.email= email 
            student.name = name 
            student.student_id= student_id 
            student.password= password 
            if level:
                student.level= data['level']
            if gender:
                student.gender= data['gender']
            db.session.commit()
        except Exception as e:
            return jsonify({'error':str(e)}),400
        return jsonify({"message": "Student Updated Successfully"})
    
    @app.route("/deletestudentaccount/",methods= ['DELETE'])
    def deleteStudentAccount():
        token = request.headers['Authorization'].split()[-1]
        student = Student.query.filter(Student.token== token).first()
        if not student:
            return jsonify({'error':"You Are Not Authorized"})
        if student.profile_pic:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'],"profile_pics",student.profile_pic))
        
        db.session.delete(student)  
        db.session.commit()  
        return jsonify({"message": "Student Deleted Successfully"})
############################################################################################################################
            # stores
############################################################################################################################
    @app.route('/stores/', methods=['GET'])
    def get_stores():
        stores = Store.query.all()
        return jsonify([store.toMap() for store in stores])

    @app.route('/stores/<int:store_id>/', methods=['GET'])
    def get_store(store_id):
        store = Store.query.filter_by(store_id=store_id).first()
        if not store:
            return jsonify({'error': 'Store not found'}), 404
        return jsonify(store.toMap())

    @app.route('/stores/', methods=['POST'])
    def create_store():
        data = json.loads(request.form['data'])
        store = Store(
            store_name=data['store_name'],
            store_review=data['store_review'],
            store_location_longitude=data['store_location_longitude'],
            store_location_latitude=data['store_location_latitude']
        )
        if 'store_img' in request.files:
            store_img = request.files['store_img']
            store_img_name = secure_filename(store_img.filename)
            store_img_path = os.path.join(app.config['UPLOAD_FOLDER'],"store_imgs",store_img_name)
            store_img.save(store_img_path)
            store.store_image = store_img_path
        else:
            return jsonify({"error":"Error In Store Image"}), 400
        db.session.add(store)
        db.session.commit()
        return jsonify({'message': 'Store created successfully'}), 200

    @app.route('/stores/<int:store_id>/', methods=['PUT'])
    def update_store(store_id):
        data = request.get_json()
        store = Store.query.filter_by(store_id=store_id).first()
        if not store:
            return jsonify({'error': 'Store not found'}), 404

        store.store_name = data.get('store_name', store.store_name)
        store.store_image = data.get('store_image', store.store_image)
        store.store_review = data.get('store_review', store.store_review)
        store.store_location_longitude = data.get('store_location_longitude', store.store_location_longitude)
        store.store_location_latitude = data.get('store_location_latitude', store.store_location_latitude)

        db.session.commit()
        return jsonify({'message': 'Store updated successfully', 'store': store.toMap()})

    @app.route('/stores/<int:store_id>/', methods=['DELETE'])
    def delete_store(store_id):
        store = Store.query.filter_by(store_id=store_id).first()
        if not store:
            return jsonify({'error': 'Store not found'}), 404

        if store.store_image:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'],"profile_pics", store.store_image))

        db.session.delete(store)
        db.session.commit()
        return jsonify({'message': 'Store deleted successfully'})
    

    @app.route('/stores/addtofavo/',methods=['POST'])
    def addtofavo():
        data = request.get_json()
        studentid = data['userid']
        storeid = data['storeid']
        is_exist = StudentStoresRelation.query.filter(StudentStoresRelation.studentid == studentid,StudentStoresRelation.storeid == storeid).first()
        if is_exist:
            return jsonify({"error": "This Relation Is Already Exist"}),400
        studentStoreRelation = StudentStoresRelation(
            studentid,
            storeid
        )
        db.session.add(studentStoreRelation)
        db.session.commit()
        return jsonify({"message": "Added successfully to The Favo."}),200

    @app.route('/stores/removefromfavo/',methods=['POST'])
    def removefromfavo():
        data = request.get_json()
        studentid = data['userid']
        storeid = data['storeid']
        relation = StudentStoresRelation.query.filter(StudentStoresRelation.studentid == studentid,StudentStoresRelation.storeid == storeid).first()
        if not relation:
            return jsonify({"error": "This Relation Is Not Exist"}),400
        
        db.session.delete(relation)
        db.session.commit()
        return jsonify({"message": "Removed Successfully From The Favo."}),200
        

        


    

    
    
    # @app.route('/hello/i/',methods=['POST'])
    # def helloi():
    #     data = request.get_json()
    #     created_data = {'name':data['name'],'age':data['age'],'user_id':data['user_id']}
    #     return jsonify(created_data)
 
        # token = request.headers.get('Authorization')
#
 
 
    # @app.route('/addUser/',methods=['POST'])
    # def addUser():
    #     data = request.get_json()
    #     name, age = data['name'],int(data['age'])
    #     user = User(name=name, age=age)

    #     db.session.add(user)
    #     db.session.commit()

    #     return 'hi'
    # @app.route('/delete/<user_id>')
    # def deleteUser(user_id):
    #     User.query.filter(User.user_id == user_id).delete()

    #     db.session.commit()
    #     return 'deleted successfully'