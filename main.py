from fastapi import FastAPI,HTTPException,status

app=FastAPI()
users=[
 {
    "id":1,"name":"John","email":"john@gmail.com"
 },
 {
     "id":2,"name":"Allie","email":"allie@gmail.com"
 }
]

@app.get("/")
async def home():
    return{
        "message": "SAAS Backend is Running "
    }

@app.get("/users")
async def get_users():
    return{
        "Users": users
    }

@app.get("/users/search")
async def search_users(name: str =None,limit:int=10):
    results=users

    if name:
        results=[u for u in users if name.lower() in u["name"].lower() ]

    return{
        "users": results[:limit],
        "count":len(results[:limit])
    }

@app.get("/users/{user_id}")
async def get_user(user_id:int):
    for user in users:
        if user["id"]==user_id:

            return{
        "user": user
                }
        
    raise HTTPException(status_code=404,detail="User Not Found")

@app.post("/users",status_code=status.HTTP_201_CREATED)
async def create_users(user :dict):
    for existing in users:
        if existing["email"]==user.get("email"):
            raise HTTPException(status_code=404,detail="Email already Exists")
    users.append(user)
    return{
        "Message": "User Created",
        "user": user
    }