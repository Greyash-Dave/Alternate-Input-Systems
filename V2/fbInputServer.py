# import socket
# import threading

# s = socket.socket()
# print("Flappy Server Created")

# s.bind(("localhost", 9999))

# s.listen(2)
# print("Waiting For Connection")

# data = None

# CONNECT = True

# # while CONNECT:
# #     try:
# #         fBirdJumpClick, playMode = "False", "False"
# #         c1, addr = s.accept()
# #         print("Connected To camInputClient", addr)
# #         input1 = c1.recv(15).decode()
# #         input1 = input.split(',')
# #         sockName, fBirdJumpClick, playMode = input1[0], input1[1], input1[2]
# #         print(fBirdJumpClick, playMode)
# #         c1.close()
# #     except Exception as e:
# #         print(e)

# #     try:
# #         c2, addr = s.accept()
# #         print("Connected To gameClient", addr)
# #         input2 = c2.recv(15).decode()
# #         input2 = input.split(',')
# #         c2.send(bytes(fBirdJumpClick+","+playMode, "utf-8"))
# #         c2.close()
# #     except Exception as e:
# #         print(e)

# # while CONNECT:

# #     fBirdJumpClick, playMode = "False", "False"
# #     c1, addr = s.accept()
# #     print("Connected To camInputClient", addr)
# #     input = c1.recv(15).decode()
# #     input = input.split(',')
# #     sockName, fBirdJumpClick, playMode = input[0], input[1], input[2]
# #     print(fBirdJumpClick, playMode)
# #     c1.close()

# #     c2, addr = s.accept()
# #     print("Connected To gameClient", addr)
# #     c2.send(bytes(input[1]+","+input[2], "utf-8"))
# #     print(fBirdJumpClick, playMode)
# #     c2.close()
    

# # while True:
# #     c2, addr = s.accept()
# #     print("Connected To FBG", addr)

# #     c2.send(bytes("False,False", "utf-8"))

# #     c2.close()

# while CONNECT:
#     try:
#         fBirdJumpClick, playMode = "False", "False"
#         c1, addr = s.accept()
#         # print("Connected To camInputClient", addr)
#         input1 = c1.recv(15).decode()
#         input1 = input.split(',')
#         # sockName, fBirdJumpClick, playMode = input1[0], input1[1], input1[2]
#         # print(fBirdJumpClick, playMode)
#         # c1.close()
#         c2, addr = s.accept()
#         # print("Connected To gameClient", addr)
#         # input2 = c2.recv(15).decode()
#         # input2 = input.split(',')
#         # c2.send(bytes(fBirdJumpClick+","+playMode, "utf-8"))
#         # c2.close()
#     except Exception as e:
#         print(e)

#     # if input1[0] == "camInputClient":
#     #     print("Connected To camInputClient", addr)
#     #     sockName, fBirdJumpClick, playMode = input1[0], input1[1], input1[2]
#     #     c2.send(bytes(fBirdJumpClick+","+playMode, "utf-8"))
#     # if input2[0] == "camInputClient":
#     #     print("Connected To camInputClient", addr)
#     #     sockName, fBirdJumpClick, playMode = input2[0], input2[1], input2[2]
#     #     c1.send(bytes(fBirdJumpClick+","+playMode, "utf-8"))
#     print("Connected To camInputClient", addr)
#     sockName, fBirdJumpClick, playMode = input1[0], input1[1], input1[2]
#     c2.send(bytes(fBirdJumpClick+","+playMode, "utf-8"))

#     c1.close()
#     c2.close()

#Threading server

# import socket
# import threading
# import queue

# lock = threading.Lock()

# s = socket.socket()
# print("Flappy Server Created")

# s.bind(("localhost", 9999))

# s.listen(2)
# print("Waiting For Connection")

# data = None

# CONNECT = True

# fBirdJumpClick, playMode = "False", "False"

# def client1(owner):
#     while CONNECT:
#         global fBirdJumpClick, playMode
#         fBirdJumpClick, playMode = "False", "False"
#         lock.acquire()
#         if owner.queue[0]=="Client1":
#             try:
#                 fBirdJumpClick, playMode = "False", "False"
#                 c1, addr = s.accept()
#                 print("Connected To camInputClient", addr)
#                 input1 = c1.recv(15).decode()
#                 input1 = input.split(',')
#                 sockName, fBirdJumpClick, playMode = input1[0], input1[1], input1[2]
#                 print(fBirdJumpClick, playMode)
#                 c1.close()
#             except Exception as e:
#                 print(e)
#                 client2(owner)
#             owner.queue[0] = "Client2"
#         lock.release()

# def client2(owner):
#     while CONNECT:
#         lock.acquire()
#         if owner.queue[0]=="Client2":
#             try:
#                 global fBirdJumpClick, playMode
#                 c2, addr = s.accept()
#                 print("Connected To gameClient", addr)
#                 c2.send(bytes(fBirdJumpClick+","+playMode, "utf-8"))
#                 c2.close()
#             except Exception as e:
#                 print(e)
#                 client1(owner)
#         owner.queue[0] = "Client1"
#         lock.release()

# owner = queue.Queue()
# owner.put("Client1")

# t1 = threading.Thread(target=client1, args=(owner, ))
# t2 = threading.Thread(target=client2, args=(owner, ))

# t1.start()
# t2.start()

# t1.join()
# t2.join()

import socket

s = socket.socket()
print("Flappy Server Created")

s.bind(("localhost", 9999))

s.listen(2)
print("Waiting For Connection")

data = None

CONNECT = True

fBirdJumpClick, playMode = "False", "False"

def client1(fBirdJumpClick, playMode):
    try:
        c1, addr = s.accept()
        print("Connected To camInputClient", addr)
        c1.timeout(20)
        input = c1.recv(15).decode()
        if input == "camInputClient":
            input1 = c1.recv(15).decode()
            input1 = input.split(',')
        fBirdJumpClick, playMode = input1[0], input1[1]
        print(fBirdJumpClick, playMode)
        client2(fBirdJumpClick, playMode)
        c1.close()
    except Exception as e:
        print(e)
        client2(fBirdJumpClick, playMode)
    return fBirdJumpClick, playMode

def client2(fBirdJumpClick, playMode):
    try:
        c2, addr = s.accept()
        try:
            c2.timeout(20)
            input = c2.recv(15).decode()
            if input == "camInputClient":
                fBirdJumpClick, playMode = client1(fBirdJumpClick, playMode)
        except:
            pass
        print("Connected To gameClient", addr)
        c2.send(bytes(fBirdJumpClick+","+playMode, "utf-8"))
        c2.close()
    except Exception as e:
        print(e)
        client1(fBirdJumpClick, playMode)
    return fBirdJumpClick, playMode

while CONNECT:
    fBirdJumpClick= "False"
    playMode = "False"
    fBirdJumpClick, playMode = client1(fBirdJumpClick, playMode)
    
