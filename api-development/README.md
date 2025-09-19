# Employee Management API Workshop

A FastAPI application demonstrating CRUD operations for employee management with token authentication.

## 🎯 Workshop Overview

Learn to build REST APIs with FastAPI, including:
- CRUD operations (Create, Read, Update, Delete)
- Data validation with Pydantic v2
- Token-based authentication
- Interactive API documentation
- Error handling and status codes

## 🚀 Quick Start

```bash
# Navigate to project
cd pythonid-workshop

# Start the API server
uv run api-development/src/main.py

# API will be available at:
# - Main API: http://localhost:8000
# - Interactive docs: http://localhost:8000/docs
# - Alternative docs: http://localhost:8000/redoc
```

## 📁 Project Structure

```
api-development/
├── src/
│   ├── main.py         # FastAPI application with all endpoints
│   ├── models.py       # Pydantic data models
│   ├── database.py     # In-memory database operations
│   └── auth.py         # Authentication logic
└── README.md
```

## 🔐 Authentication

All endpoints (except `/` and `/health`) require authentication:

**Method 1: X-Token Header**
```bash
curl -H "X-Token: secret123" http://localhost:8000/employees
```

**Method 2: Authorization Header**
```bash
curl -H "Authorization: Bearer secret123" http://localhost:8000/employees
```

## 📊 Employee Data Model

```json
{
  "id": 1,
  "name": "John Doe",
  "role": "Developer",
  "email": "john.doe@company.com"
}
```

**Available Roles:**
- Developer
- Designer
- Manager
- Analyst
- Tester
- DevOps Engineer
- Product Manager
- HR
- Admin

## 🛠 API Endpoints

### Public Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |

### Protected Endpoints (Require Authentication)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/employees` | Get all employees |
| POST | `/employees` | Create new employee |
| GET | `/employees/{id}` | Get employee by ID |
| PUT | `/employees/{id}` | Update employee |
| DELETE | `/employees/{id}` | Delete employee |
| GET | `/employees/role/{role}` | Get employees by role |
| GET | `/stats` | Get employee statistics |

## 📝 Example Usage

### 1. Create Employee
```bash
curl -X POST "http://localhost:8000/employees" \
  -H "Content-Type: application/json" \
  -H "X-Token: secret123" \
  -d '{
    "name": "Alice Johnson",
    "role": "Developer",
    "email": "alice@company.com"
  }'
```

### 2. Get All Employees
```bash
curl -H "X-Token: secret123" http://localhost:8000/employees
```

### 3. Get Employee by ID
```bash
curl -H "X-Token: secret123" http://localhost:8000/employees/1
```

### 4. Update Employee
```bash
curl -X PUT "http://localhost:8000/employees/1" \
  -H "Content-Type: application/json" \
  -H "X-Token: secret123" \
  -d '{
    "name": "Alice Smith",
    "role": "Manager"
  }'
```

### 5. Delete Employee
```bash
curl -X DELETE "http://localhost:8000/employees/1" \
  -H "X-Token: secret123"
```

### 6. Get Statistics
```bash
curl -H "X-Token: secret123" http://localhost:8000/stats
```

## 🎓 Learning Objectives

### FastAPI Concepts
- **Application Setup**: Creating FastAPI app with metadata
- **Route Definitions**: HTTP methods and path parameters
- **Request/Response Models**: Pydantic validation
- **Dependency Injection**: Authentication dependencies
- **Error Handling**: HTTP exceptions and status codes
- **Documentation**: Automatic OpenAPI docs generation

### API Design Patterns
- **RESTful Design**: Resource-based URLs
- **HTTP Status Codes**: Proper response codes
- **Request Validation**: Input sanitization
- **Response Formatting**: Consistent API responses
- **Authentication**: Token-based security

### Data Management
- **CRUD Operations**: Complete data lifecycle
- **In-Memory Storage**: Simple database simulation
- **Thread Safety**: Concurrent request handling
- **Data Validation**: Pydantic model validation

## 🔧 Advanced Features

### Data Validation
- Email format validation
- String length constraints
- Enum-based role validation
- Optional field updates

### Error Handling
```json
{
  "detail": "Employee with ID 999 not found"
}
```

### Response Models
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {}
}
```

## 🧪 Testing the API

### Using the Interactive Docs
1. Go to http://localhost:8000/docs
2. Click "Authorize" and enter token: `secret123`
3. Try different endpoints directly in the browser

### Using curl
See example commands above

### Using Python requests
```python
import requests

headers = {"X-Token": "secret123"}
response = requests.get("http://localhost:8000/employees", headers=headers)
print(response.json())
```

## 💡 Workshop Exercises

### Exercise 1: Basic CRUD
1. Start the API server
2. Create 3 new employees with different roles
3. List all employees
4. Update one employee's information
5. Delete one employee

### Exercise 2: Error Handling
1. Try to access without authentication
2. Try to get a non-existent employee
3. Try to create an employee with invalid data
4. Try to update a non-existent employee

### Exercise 3: Filtering & Stats
1. Create employees with different roles
2. Filter employees by role
3. Check the statistics endpoint
4. Observe how the stats change

## 🚀 Extensions & Next Steps

### Easy Extensions
- Add more employee fields (department, salary, hire_date)
- Add search functionality (by name, email)
- Add pagination for large employee lists
- Add role-based permissions

### Advanced Extensions
- Replace in-memory storage with SQLAlchemy + SQLite
- Add JWT token authentication
- Add employee photo upload
- Add audit logging
- Add API rate limiting

### Database Migration
The current in-memory database can be easily replaced with SQLAlchemy:

```python
# Future: database.py with SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String)
    email = Column(String, unique=True, index=True)
```

## 📚 Key Technologies

- **FastAPI**: Modern, fast web framework for APIs
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running the application
- **OpenAPI**: Automatic API documentation generation

## 🎯 Workshop Outcomes

After completing this workshop, participants will understand:

1. **API Development**: Building REST APIs with FastAPI
2. **Data Modeling**: Using Pydantic for validation
3. **Authentication**: Implementing token-based auth
4. **Documentation**: Leveraging automatic API docs
5. **Testing**: Using interactive documentation for API testing
6. **Error Handling**: Proper HTTP status codes and responses

Perfect for learning modern Python API development! 🐍⚡

---

**Ready to build APIs with FastAPI! 🚀**