from flask import request,jsonify
from models import Student


def register_routes(app, db):
    @app.route('/hello/',methods=['GET'])
    def hello():
        return jsonify({'user_id':5000,'name':'Demo','age':100})
       
    # @app.route('/hello/i/',methods=['POST'])
    # def helloi():
    #     data = request.get_json()
    #     created_data = {'name':data['name'],'age':data['age'],'user_id':data['user_id']}
    #     return jsonify(created_data)
    
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