from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, create_engine, Session, select
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from models import User, UserCreate, UserResponse
from database import create_database, get_session, engine

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup
    print("🚀 Starting up...")

    # Create database if it doesn't exist
    create_database()

    # Create tables
    SQLModel.metadata.create_all(engine)
    print("✅ Database and tables created successfully!")

    yield

    # Shutdown
    print("🔄 Shutting down...")


# Initialize FastAPI app
app = FastAPI(
    title="User Management API",
    description="A FastAPI application for managing users with PostgreSQL",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to User Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "create_user": "POST /users/",
            "get_users": "GET /users/",
            "get_user": "GET /users/{user_id}"
        }
    }


@app.post("/users/", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, session: Session = Depends(get_session)):
    """Create a new user"""
    try:
        # Check if email already exists
        existing_user = session.exec(
            select(User).where(User.email == user.email)
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        # Check if username already exists
        existing_username = session.exec(
            select(User).where(User.username == user.username)
        ).first()

        if existing_username:
            raise HTTPException(
                status_code=400,
                detail="Username already taken"
            )

        # Create new user
        db_user = User.model_validate(user)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return UserResponse.model_validate(db_user)

    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create user: {str(e)}"
        )


@app.get("/users/", response_model=list[UserResponse])
async def get_users(
        skip: int = 0,
        limit: int = 100,
        session: Session = Depends(get_session)
):
    """Get all users with optional pagination"""
    try:
        users = session.exec(
            select(User).offset(skip).limit(limit)
        ).all()

        return [UserResponse.model_validate(user) for user in users]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch users: {str(e)}"
        )


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, session: Session = Depends(get_session)):
    """Get a specific user by ID"""
    try:
        user = session.get(User, user_id)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return UserResponse.model_validate(user)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch user: {str(e)}"
        )


@app.get("/users/email/{email}", response_model=UserResponse)
async def get_user_by_email(email: str, session: Session = Depends(get_session)):
    """Get a user by email address"""
    try:
        user = session.exec(
            select(User).where(User.email == email)
        ).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return UserResponse.model_validate(user)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch user: {str(e)}"
        )


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, session: Session = Depends(get_session)):
    """Delete a user by ID"""
    try:
        user = session.get(User, user_id)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        session.delete(user)
        session.commit()

        return {"message": "User deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete user: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )