# Employee CRUD REST API (AWS Lambda + API Gateway + DynamoDB)

This is a serverless REST API built using AWS services and Python.  
It performs full CRUD operations on an Employee database.

---

##  Features

- Create Employee
- Get All Employees
- Get Employee by ID
- Update Employee
- Delete Employee
- Health Check API

---

##  Architecture

API Gateway → AWS Lambda → DynamoDB

---

## 🔗 Base URL

https://wpn2rljsd7.execute-api.ap-south-1.amazonaws.com/production/



---

##  API Endpoints

### GET /status
Check API health

### GET /employees
Get all employees

### GET /employee?employeeid=1
Get employee by ID

### POST /employee
Create employee

### PATCH /employee
Update employee

### DELETE /employee
Delete employee

---

##  Example Requests

### Create Employee
```json
{
  "employeeid": "1",
  "name": "Yash",
  "role": "Developer"
}