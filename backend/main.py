from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import timedelta
from typing import List
import models, schemas, auth
from database import engine, get_db

# Создание таблиц
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PainKiller API",
    description="Backend API for PainKiller application",
    version="1.0.0"
)

# Настройка CORS
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:5175",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5175",
    "http://127.0.0.1:3000",
    "*"  # Временно разрешаем все origins для отладки
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"\n--- Incoming request ---")
    print(f"Method: {request.method}")
    print(f"URL: {request.url}")
    print(f"Headers: {request.headers}")
    try:
        body = await request.body()
        if body:
            print(f"Body: {body.decode()}")
    except:
        pass
    response = await call_next(request)
    return response

@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    print(f"\n=== Register attempt ===")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        print(f"Username {user.username} already exists")
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        print(f"Email {user.email} already exists")
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(f"User {user.username} successfully registered")
    return db_user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        print(f"\n=== Login attempt ===")
        print(f"Username: {form_data.username}")
        user = auth.authenticate_user(db, form_data.username, form_data.password)
        if not user:
            print(f"Authentication failed for user: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        print(f"Authentication successful for user: {form_data.username}")
        access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        print(f"Access token created for user: {form_data.username}")
        response_data = {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }
        print(f"Returning response: {response_data}")
        return response_data
    except Exception as e:
        print(f"Login error: {str(e)}")
        print(f"Full error details: {e.__class__.__name__}")
        raise

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    print(f"\n=== Get current user ===")
    print(f"User: {current_user.username}")
    return current_user

@app.post("/pains", response_model=schemas.Pain)
def create_pain(pain: schemas.PainCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    print(f"\n=== Create pain ===")
    print(f"User: {current_user.username}")
    print(f"Pain data: {pain.dict()}")
    db_pain = models.Pain(**pain.dict(), user_id=current_user.id)
    db.add(db_pain)
    db.commit()
    db.refresh(db_pain)
    return db_pain

@app.get("/pains")
def read_pains(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    print(f"\n=== Get pains ===")
    print(f"Skip: {skip}, Limit: {limit}")
    try:
        pains = db.query(models.Pain).join(
            models.User, models.Pain.user_id == models.User.id
        ).outerjoin(models.Vote).group_by(
            models.Pain.id,
            models.User.id,
            models.User.username,
            models.User.email
        ).add_columns(
            models.User.username.label("username"),
            models.User.email.label("email"),
            func.count(models.Vote.id).label("votes_count")
        ).order_by(func.count(models.Vote.id).desc()).offset(skip).limit(limit).all()
        
        result = []
        for pain, username, email, votes_count in pains:
            pain_dict = {
                "id": pain.id,
                "title": pain.title,
                "description": pain.description,
                "created_at": pain.created_at,
                "user_id": pain.user_id,
                "votes_count": votes_count,
                "creator": {
                    "username": username,
                    "email": email,
                    "id": pain.user_id
                }
            }
            print(f"Pain entry: {pain_dict}")
            result.append(pain_dict)
        print(f"Found {len(result)} pains")
        return result
    except Exception as e:
        print(f"Error in read_pains: {str(e)}")
        print(f"Full error details: {e.__class__.__name__}")
        return []

@app.post("/votes", response_model=schemas.Vote)
def create_vote(vote: schemas.VoteBase, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    print(f"\n=== Create vote ===")
    print(f"User: {current_user.username}")
    print(f"Pain ID: {vote.pain_id}")
    db_vote = db.query(models.Vote).filter_by(
        pain_id=vote.pain_id, user_id=current_user.id
    ).first()
    if db_vote:
        print(f"User already voted for pain {vote.pain_id}")
        raise HTTPException(status_code=400, detail="Already voted")
    
    db_vote = models.Vote(**vote.dict(), user_id=current_user.id)
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    print(f"Vote created successfully")
    return db_vote

@app.get("/votes/check/{pain_id}")
def check_vote(pain_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    print(f"\n=== Check vote ===")
    print(f"User: {current_user.username}")
    print(f"Pain ID: {pain_id}")
    vote = db.query(models.Vote).filter_by(
        pain_id=pain_id, user_id=current_user.id
    ).first()
    has_voted = vote is not None
    print(f"Has voted: {has_voted}")
    return {"has_voted": has_voted}

@app.get("/")
async def root():
    return {"message": "Welcome to PainKiller API"}

if __name__ == "__main__":
    import uvicorn
    print("\n=== Starting server on port 8001 ===")
    uvicorn.run(app, host="0.0.0.0", port=8001) 