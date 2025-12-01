
# from jaii import Fullname



# def mydeco(fun):
#     def wrap():
#         print("Start")
#         fun()
#         print("end")
#     return wrap


# def sayhello():
#     print("Hello world")


# sayhello = mydeco(sayhello)
# sayhello()
def deco(myfun):
    def a():
        print("Start")
        myfun()
        print("stop")
    # print(a)
    return a

def sayhello():
    print("helloworld")


container_sayhello = deco(sayhello)




container_sayhello()






















# from fastapi import FastAPI
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# app = FastAPI()

# templates 
