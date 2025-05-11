import requests
import json
from datetime import datetime
import os


name = "Anshika Rathore"
reg_no = "0827AL221027"
email = "anshikarathore220101@acropolis.in"

def main():
    
    print("Step 1: Generating webhook...")
    webhook_response = generate_webhook(name, reg_no, email)
    
    if webhook_response:
        webhook_url = webhook_response.get('webhook')
        access_token = webhook_response.get('accessToken')
        
        print(f"Webhook URL: {webhook_url}")
        print(f"Access Token: {access_token}")
        
       
        sql_query = read_sql_file("solution.sql")
        print(f"\nStep 2: SQL Solution:\n{sql_query}")
        
       
        print("\nStep 3: Submitting solution...")
        submit_response = submit_solution(webhook_url, access_token, sql_query)
        
        print(f"\nSubmission Response: {submit_response}")
    else:
        print("Failed to generate webhook. Please check your request parameters.")

def generate_webhook(name, reg_no, email):
    """Generate webhook by sending POST request to the API"""
    url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
    
    payload = {
        "name": name,
        "regNo": reg_no,
        "email": email
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error generating webhook: {e}")
        return None

def read_sql_file(filename):
    """Read SQL query from a file"""
    try:
        with open(filename, 'r') as file:
            
            lines = file.readlines()
            
            sql_query = ''.join([line for line in lines if not line.strip().startswith('--')])
            return sql_query
    except FileNotFoundError:
        print(f"Error: SQL file '{filename}' not found!")
        print("Make sure 'solution.sql' is in the same directory as this Python script.")
        
        return get_hardcoded_sql_solution()

def get_hardcoded_sql_solution():
    """Return the SQL solution as a fallback if file reading fails"""
    return """SELECT 
    p.AMOUNT AS SALARY,
    CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS NAME,
    TIMESTAMPDIFF(YEAR, e.DOB, CURRENT_DATE()) AS AGE,
    d.DEPARTMENT_NAME
FROM 
    PAYMENTS p
JOIN 
    EMPLOYEE e ON p.EMP_ID = e.EMP_ID
JOIN 
    DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
WHERE 
    DAY(p.PAYMENT_TIME) != 1
ORDER BY 
    p.AMOUNT DESC
LIMIT 1;"""

def submit_solution(webhook_url, access_token, sql_query):
    """Submit the SQL solution to the webhook URL"""
    headers = {
        "Authorization": access_token,
        "Content-Type": "application/json"
    }
    
    payload = {
        "finalQuery": sql_query
    }
    
    try:
        response = requests.post(webhook_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error submitting solution: {e}")
        return None

if __name__ == "__main__":
    main()