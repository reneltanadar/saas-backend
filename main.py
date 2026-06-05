from fastapi import FastAPI

app=FastAPI()
users=[]

@app.get("/")
async def home():
    return{
        "message": "Hello "
    }

@app.get("/users")
async def get_users():
    return{
        "Users": users
    }

@app.post("/users")
async def create_users(user :dict):
    users.append(user)
    return{
        "Message": "User Created",
        "user": user
    }