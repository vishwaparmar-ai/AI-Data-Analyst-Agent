from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from backend.schemas.user import UserCreate,UserLogin,UserResponse,Token
from backend.database.dependency import get_db
from backend.models.user import User
from backend.utils.security import hash_password,verify_password
from backend.utils.jwt import create_access_token


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register(user:UserCreate,db: Session = Depends(get_db)):
    existing_email = db.query(User).filter(user.email == User.email).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    existing_username = db.query(User).filter(user.username == User.username).first()

    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@router.post(
    "/login",
    response_model=Token
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    if not verify_password(
        user.password,
        db_user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    access_token = create_access_token(
        {
            "sub": str(db_user.id),
            "email": db_user.email,
            "username": db_user.username
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
