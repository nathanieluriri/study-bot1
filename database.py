


def db_login_signup(proceed, user_name, password, first_name='None', last_name='None', learning_rate='None', understanding_rate='None'):
    import bcrypt
    from pymongo import MongoClient
    from pymodm import connect, MongoModel, fields
    from bson import ObjectId
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    MONGO_URI = os.getenv('MONGO_URI')

    connect(MONGO_URI)

    class User(MongoModel):
        user_name = fields.CharField(mongo_name="User Name")
        first_name = fields.CharField(mongo_name="First Name")
        last_name = fields.CharField(mongo_name="Last Name") 
        password = fields.CharField(mongo_name="Password")
        learning_rate = fields.CharField(mongo_name="Learning Speed")
        understanding_rate = fields.CharField(mongo_name="Understanding Speed")


    def signup(user, passw, first_name=None, last_name=None, learning_rate=None, understanding_rate=None):
        hashed_passw = bcrypt.hashpw(passw.encode('utf-8'), bcrypt.gensalt())
        new_user = User(user_name=user, password=hashed_passw, first_name=first_name, last_name=last_name, learning_rate=learning_rate, understanding_rate=understanding_rate)
        if first_name !='None' and last_name!='None' and learning_rate !='None' and understanding_rate !='None':
            new_user.save()
        return new_user

    def login(user, passw):
        users = User.objects.all()
        for u in users:
            if user == u.user_name:
                checkP = u.password
                checkP = checkP[2:-1]
                checkP = bytes(checkP, 'utf-8')
                if bcrypt.checkpw(passw.encode('utf-8'), checkP):
                    return u
        return None


    def start(process, user_name, password, first_name=None, last_name=None, learning_rate=None, understanding_rate=None):
        if process == 1:
            return signup(user_name, password, first_name, last_name, learning_rate, understanding_rate)
        elif process == 2:
            return login(user_name, password)
        else:
            raise ValueError("Invalid process")

    return start(proceed, user_name, password, first_name, last_name, learning_rate, understanding_rate)

# db_login_signup(1, "test user", "password",first_name="Test",last_name="Test",learning_rate="2",understanding_rate="4")

print(db_login_signup(2, "test user", "password"))