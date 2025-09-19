"""
In-memory database for Employee API
Simple storage that can be easily replaced with SQLAlchemy later
"""

from typing import Dict, List, Optional
from models import Employee, EmployeeCreate, EmployeeUpdate
import threading

class EmployeeDatabase:
    """In-memory employee database with thread safety"""
    
    def __init__(self):
        self._employees: Dict[int, Employee] = {}
        self._next_id = 1
        self._lock = threading.Lock()
        
        # Add some sample data
        self._init_sample_data()
    
    def _init_sample_data(self):
        """Initialize with some sample employees"""
        sample_employees = [
            EmployeeCreate(name="John Doe", role="Developer", email="john.doe@company.com"),
            EmployeeCreate(name="Jane Smith", role="Manager", email="jane.smith@company.com"),
            EmployeeCreate(name="Bob Wilson", role="Designer", email="bob.wilson@company.com"),
        ]
        
        for emp_data in sample_employees:
            self.create_employee(emp_data)
    
    def create_employee(self, employee_data: EmployeeCreate) -> Employee:
        """Create a new employee"""
        with self._lock:
            employee = Employee(
                id=self._next_id,
                name=employee_data.name,
                role=employee_data.role,
                email=employee_data.email
            )
            self._employees[self._next_id] = employee
            self._next_id += 1
            return employee
    
    def get_employee(self, employee_id: int) -> Optional[Employee]:
        """Get employee by ID"""
        return self._employees.get(employee_id)
    
    def get_all_employees(self) -> List[Employee]:
        """Get all employees"""
        return list(self._employees.values())
    
    def update_employee(self, employee_id: int, employee_data: EmployeeUpdate) -> Optional[Employee]:
        """Update an existing employee"""
        with self._lock:
            if employee_id not in self._employees:
                return None
            
            current_employee = self._employees[employee_id]
            
            # Update only provided fields
            update_data = employee_data.model_dump(exclude_unset=True)
            
            updated_employee = Employee(
                id=employee_id,
                name=update_data.get('name', current_employee.name),
                role=update_data.get('role', current_employee.role),
                email=update_data.get('email', current_employee.email)
            )
            
            self._employees[employee_id] = updated_employee
            return updated_employee
    
    def delete_employee(self, employee_id: int) -> bool:
        """Delete an employee"""
        with self._lock:
            if employee_id in self._employees:
                del self._employees[employee_id]
                return True
            return False
    
    def employee_exists(self, employee_id: int) -> bool:
        """Check if employee exists"""
        return employee_id in self._employees
    
    def get_employee_count(self) -> int:
        """Get total number of employees"""
        return len(self._employees)

# Global database instance
db = EmployeeDatabase()