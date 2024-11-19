from app.schemas.user import UserCreate, UserOut, UserLogin, Token
from fastapi import APIRouter, HTTPException, Depends
from app.utils.dependencies import get_current_user
from app.utils.jwt import create_access_token
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.hashing import Hash
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Registration endpoint
@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username or email already exists
    print(f"the user : {user}")
    existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if existing_user:
        print("Username or email already exists")
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    # Create new user
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=Hash.bcrypt(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Login endpoint
@router.post("/login", response_model=Token)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not Hash.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create JWT token
    access_token = create_access_token({"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Dashboard endpoint
@router.get("/dashboard")
def get_dashboard(user: User = Depends(get_current_user)):
    return {
        "user": user.username,
        "total_chatbots": 0,
        "creation_dates": []
    }