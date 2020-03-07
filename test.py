

# import functools
# user = {"username": "Andy", "access_level": "guest"}
#
#
#
#
# def make_secure(func):
#     @functools.wraps(func)
#     def secure_function(*args, **kwargs):
#         # print("User info: ", user["username"])
#         if user["access_level"] == "admin":
#             return func(*args, **kwargs)
#         else:
#             return "No admin permissions for {}.".format(user["username"])
#             # return "No admin permissions for {}.".format(user["username"])
#
#     return secure_function
#
# # get_admin_password = secure_function(get_admin_password)
# # get_admin_password = make_secure(get_admin_password)
#
# @make_secure
# def get_admin_password(panel):
#     if panel == "admin":
#         return "1234"
#     elif panel == "billing":
#         return "super_secure_password"
#
#
# user = {"username": "Andy", "access_level": "admin"}
# print(get_admin_password("billing"))
# print(get_admin_password.__name__)








#
# def search(sequence, expected, finder):
#
#     for elem in sequence:
#         if finder(elem) == expected:
#             return elem
#
#     raise RuntimeError(f"Could not find an element with {expected}.")
#
# friends = [
#     {"name": "Rolf Smith", "age": 24}
#
# ]
#
# def get_friend_name(friend):
#     return friend["name"]
#
#
# print(search(friends, "Rolf Smith", get_friend_name))






# import alien_invasion
#

#
# x = 10
# f = open("high_score.txt", 'w')
# f.write(str(x))
# f.close()
#
# r = open("high_score.txt", 'r')
# y = r.read()
# print(y, type(y))
# print(int(y))




# import os
# print(os.path.dirname("/Users/chingandywu/chinganwu/Python/alien_invasion/bullet.py"))



# class Alien:
#     def __init__(self, x, y):
#         self.x_value = x
#         self.y_value = y
#     def __str__(self):
#         return "x:{}, y:{}".format(self.x_value, self.y_value)
# #
# # a = Alien(100, 75)
# # print(a)
# print(Alien(10, 78).x_value)
