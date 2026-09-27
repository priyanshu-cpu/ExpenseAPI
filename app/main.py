from fastapi import FastAPI
from app.routers.users import router as user_router
from app.routers.categories import router as category_router
from app.routers.expenses import router as expense_router



app = FastAPI()


app.include_router(user_router, tags=["auth"])
app.include_router(category_router, tags=["category"])
app.include_router(expense_router, tags=["expenses"])