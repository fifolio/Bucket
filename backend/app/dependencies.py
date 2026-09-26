from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.supabase import supabase

security = HTTPBearer()

# Pass the authenticated user's JWT to PostgreSQL for row-level security (RLS) policies
def get_user_supabase(token: str):
    client = supabase
    client.postgrest.auth(token)
    return client

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = supabase.auth.get_user(token)
    if not user.user:
        raise HTTPException(
            status_code=401, 
            detail="Invalid authentication credentials"
        )
    return {
        "user": user.user,
        "token": token,
    }