from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class ForgotResopnse(BaseModel):
    email: EmailStr

@app.post("/forgot_password")
def forgot_password(depends = get_db):
    email = verify_reset_tokens(req.token)
    user = db.query(User).filter(User.email==first)