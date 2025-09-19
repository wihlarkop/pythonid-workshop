"""
Pydantic models for Authentication API and Employee Management
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class LoginRequest(BaseModel):
    """Login request model"""
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin",
                "password": "admin123"
            }
        }


class LoginResponse(BaseModel):
    """Login response model"""
    success: bool
    message: str
    session_token: str
    user: dict

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Login successful",
                "session_token": "abc123...",
                "user": {
                    "id": 1,
                    "username": "admin",
                    "email": "admin@example.com",
                    "full_name": "Admin User"
                }
            }
        }


class LogoutResponse(BaseModel):
    """Logout response model"""
    success: bool
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Logout successful"
            }
        }


class UserProfile(BaseModel):
    """User profile model"""
    id: int
    username: str
    email: str
    full_name: str
    login_time: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "admin",
                "email": "admin@example.com",
                "full_name": "Admin User",
                "login_time": "2024-01-15T10:30:00"
            }
        }


class APIResponse(BaseModel):
    """Generic API response model"""
    success: bool
    message: str
    data: Optional[dict] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operation successful",
                "data": {}
            }
        }


# Employee Management Models

class EmployeeRole(str, Enum):
    """Employee role enumeration"""
    DEVELOPER = "Developer"
    MANAGER = "Manager"
    DESIGNER = "Designer"
    ANALYST = "Analyst"
    TESTER = "Tester"


class EmployeeCreate(BaseModel):
    """Employee creation model"""
    name: str
    role: EmployeeRole
    email: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "role": "Developer",
                "email": "john.doe@company.com"
            }
        }


class EmployeeUpdate(BaseModel):
    """Employee update model (all fields optional)"""
    name: Optional[str] = None
    role: Optional[EmployeeRole] = None
    email: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Jane Smith",
                "role": "Manager",
                "email": "jane.smith@company.com"
            }
        }


class Employee(BaseModel):
    """Employee model"""
    id: int
    name: str
    role: EmployeeRole
    email: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "role": "Developer",
                "email": "john.doe@company.com"
            }
        }


class EmployeeList(BaseModel):
    """Employee list response model"""
    employees: List[Employee]
    total: int

    class Config:
        json_schema_extra = {
            "example": {
                "employees": [
                    {
                        "id": 1,
                        "name": "John Doe",
                        "role": "Developer",
                        "email": "john.doe@company.com"
                    }
                ],
                "total": 1
            }
        }