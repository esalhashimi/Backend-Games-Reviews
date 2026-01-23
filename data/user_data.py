from models.user import UserModel

def create_test_users():
    user = UserModel(username="isa", email="isa@gmail.com")
    user.set_password("1234")

    return [user]

user_list = create_test_users()