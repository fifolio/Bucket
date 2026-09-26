
from app.supabase import supabase
from app.models.auth import LoginRequest
from fastapi import APIRouter, HTTPException
from fastapi import HTTPException

auth = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@auth.post("/login")
def login(credentials: LoginRequest):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        return {"access_token": response.session.access_token}
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
