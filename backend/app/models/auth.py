from supabase_auth import BaseModel

# input model for login
class LoginRequest(BaseModel):
    email: str
    password: str