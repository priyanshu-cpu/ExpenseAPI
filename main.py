from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.database import Base, engine
from routers.expenses import router as expense_router
from routers.categories import router as category_router
from routers.users import router as user_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(engine)

# @app.get("/")
# def home():
#     return{
#         "message" : "Home Page"
#     }


app.include_router(expense_router, tags=["Expenses"])
app.include_router(category_router, tags=["Categories"])
app.include_router(user_router, tags=["Users"])