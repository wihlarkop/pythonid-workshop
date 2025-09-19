"""
Simple Authentication API
FastAPI application with login and logout endpoints using dummy user data
"""

from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException, status

from auth import authenticate_user, create_session, revoke_session, verify_session_token
from database import db
from models import (
    APIResponse,
    Employee,
    EmployeeCreate,
    EmployeeList,
    EmployeeRole,
    EmployeeUpdate,
    LoginRequest,
    LoginResponse,
    LogoutResponse,
    UserProfile
)

# Create FastAPI app
app = FastAPI(
    title="Simple Authentication API",
    description="A basic authentication API with login/logout functionality using dummy data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# Authentication dependency
async def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    """Get current authenticated user from session token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.split(" ")[1]
    return verify_session_token(token)


# Authentication Endpoints

@app.post("/auth/login", response_model=LoginResponse)
async def login(login_request: LoginRequest):
    """Login with username and password"""
    user = authenticate_user(login_request.username, login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    session_token = create_session(user)

    return LoginResponse(
        success=True,
        message="Login successful",
        session_token=session_token,
        user={
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "full_name": user["full_name"]
        }
    )


@app.post("/auth/logout", response_model=LogoutResponse)
async def logout(authorization: Optional[str] = Header(None)):
    """Logout and revoke session token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header"
        )

    token = authorization.split(" ")[1]
    success = revoke_session(token)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to logout - invalid session"
        )

    return LogoutResponse(
        success=True,
        message="Logout successful"
    )


@app.get("/auth/profile", response_model=UserProfile)
async def get_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""
    return UserProfile(
        id=current_user["user_id"],
        username=current_user["username"],
        email=current_user["email"],
        full_name=current_user["full_name"],
        login_time=current_user["login_time"]
    )


# Employee CRUD Endpoints (Requires Authentication)

@app.post("/employees", response_model=Employee, status_code=status.HTTP_201_CREATED)
async def create_employee(
    employee: EmployeeCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new employee (requires authentication)

    - **name**: Employee full name
    - **role**: Employee role (Developer, Manager, etc.)
    - **email**: Employee email address
    """
    try:
        new_employee = db.create_employee(employee)
        return new_employee
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create employee: {str(e)}"
        )


@app.get("/employees", response_model=EmployeeList)
async def get_all_employees(current_user: dict = Depends(get_current_user)):
    """
    Retrieve all employees (requires authentication)

    Returns a list of all employees in the system
    """
    employees = db.get_all_employees()
    return EmployeeList(employees=employees, total=len(employees))


@app.get("/employees/{employee_id}", response_model=Employee)
async def get_employee(
    employee_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Retrieve a specific employee by ID (requires authentication)

    - **employee_id**: The ID of the employee to retrieve
    """
    employee = db.get_employee(employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found"
        )
    return employee


@app.put("/employees/{employee_id}", response_model=Employee)
async def update_employee(
    employee_id: int,
    employee_update: EmployeeUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update an existing employee (requires authentication)

    - **employee_id**: The ID of the employee to update
    - **name**: New employee name (optional)
    - **role**: New employee role (optional)
    - **email**: New employee email (optional)
    """
    if not db.employee_exists(employee_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found"
        )

    updated_employee = db.update_employee(employee_id, employee_update)
    if not updated_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update employee"
        )

    return updated_employee


@app.delete("/employees/{employee_id}", response_model=APIResponse)
async def delete_employee(
    employee_id: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete an employee (requires authentication)

    - **employee_id**: The ID of the employee to delete
    """
    if not db.employee_exists(employee_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found"
        )

    success = db.delete_employee(employee_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete employee"
        )

    return APIResponse(
        success=True,
        message=f"Employee with ID {employee_id} deleted successfully"
    )


# Additional utility endpoints

@app.get("/employees/role/{role}", response_model=EmployeeList)
async def get_employees_by_role(
    role: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get all employees with a specific role (requires authentication)

    - **role**: The role to filter by
    """
    all_employees = db.get_all_employees()
    filtered_employees = [emp for emp in all_employees if emp.role.value == role]

    return EmployeeList(employees=filtered_employees, total=len(filtered_employees))


@app.get("/stats", response_model=dict)
async def get_employee_stats(current_user: dict = Depends(get_current_user)):
    """
    Get employee statistics (requires authentication)

    Returns statistics about employees by role
    """
    employees = db.get_all_employees()

    # Count by role
    role_counts = {}
    for emp in employees:
        role = emp.role.value
        role_counts[role] = role_counts.get(role, 0) + 1

    return {
        "total_employees": len(employees),
        "employees_by_role": role_counts,
        "available_roles": [role.value for role in EmployeeRole] if employees else []
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
