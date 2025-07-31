# FastAPI PostgreSQL User Management API

A modern, production-ready FastAPI application for user management with PostgreSQL database integration.

## Features

- ✅ **Automatic Database Creation**: Creates database and tables if they don't exist
- ✅ **User Management**: Create, read, and delete users
- ✅ **Data Validation**: Email and username validation with Pydantic
- ✅ **Error Handling**: Comprehensive error handling and meaningful error messages
- ✅ **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- ✅ **CORS Support**: Cross-origin resource sharing enabled
- ✅ **Environment Configuration**: Configurable via environment variables
- ✅ **Database Sessions**: Proper session management with dependency injection

## Project Structure

```
fastapi-postgres-project/
├── main.py              # FastAPI application and routes
├── models.py            # SQLModel/Pydantic models
├── database.py          # Database configuration and utilities
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
├── test_api.py         # API testing script
├── docker-compose.yml   # PostgreSQL Docker setup
└── README.md           # Project documentation
```

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup PostgreSQL

**Option A: Using Docker (Recommended)**
```bash
docker-compose up -d
```

**Option B: Local PostgreSQL Installation**
- Install PostgreSQL on your system
- Update `.env` file with your PostgreSQL credentials

### 3. Configure Environment

Update the `.env` file with your database credentials:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/userinfo
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=userinfo
```

### 4. Run the Application

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Base URL: `http://localhost:8000`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint with API information |
| POST | `/users/` | Create a new user |
| GET | `/users/` | Get all users (with pagination) |
| GET | `/users/{user_id}` | Get user by ID |
| GET | `/users/email/{email}` | Get user by email |
| DELETE | `/users/{user_id}` | Delete user by ID |

### Example Usage

**Create a User:**
```bash
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "username": "testuser"}'
```

**Get All Users:**
```bash
curl "http://localhost:8000/users/"
```

**Get User by ID:**
```bash
curl "http://localhost:8000/users/1"
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Database Schema

### Users Table

| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT |
| email | VARCHAR | UNIQUE, NOT NULL, INDEX |
| username | VARCHAR(50) | UNIQUE, NOT NULL, INDEX |
| created_at | TIMESTAMP | DEFAULT NOW() |
| updated_at | TIMESTAMP | DEFAULT NOW() |

## Testing

Run the test script to verify API functionality:

```bash
python test_api.py
```

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid input data, duplicate email/username
- **404 Not Found**: User not found
- **422 Unprocessable Entity**: Validation errors
- **500 Internal Server Error**: Server-side errors

## Features Implemented

1. **Automatic Database Creation**: The application automatically creates the database and tables on startup
2. **Data Validation**: Email format validation and username constraints
3. **Unique Constraints**: Prevents duplicate emails and usernames
4. **Pagination**: Get users with skip and limit parameters
5. **Timestamps**: Automatic creation and update timestamps
6. **Error Handling**: Comprehensive error responses
7. **API Documentation**: Auto-generated OpenAPI documentation
8. **Environment Configuration**: Configurable database settings
9. **Session Management**: Proper database session handling
10. **CORS Support**: Cross-origin requests enabled

## Production Considerations

- Set `echo=False` in database engine for production
- Use proper password hashing for user authentication
- Implement rate limiting
- Add logging and monitoring
- Use connection pooling for better performance
- Add data migration system
- Implement proper authentication and authorization

## Dependencies

- **FastAPI**: Modern web framework for building APIs
- **SQLModel**: SQL database ORM built on SQLAlchemy and Pydantic
- **Psycopg2**: PostgreSQL adapter for Python
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running FastAPI applications
- **Python-dotenv**: Load environment variables from .env file