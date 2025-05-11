

import requests
import json

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
        
       
        last_digit = int(reg_no[-1])
        is_odd = last_digit % 2 != 0
        
        print(f"\nStep 2: Last digit of registration number is {last_digit}")
        print(f"Question type: {'Odd (Question 1)' if is_odd else 'Even (Question 2)'}")
        
       
        sql_query = solve_sql_problem(is_odd)
        print(f"\nStep 3: SQL Solution:\n{sql_query}")
        
        
        print("\nStep 4: Submitting solution...")
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

def solve_sql_problem(is_odd):
    """Solve the SQL problem based on whether reg_no is odd or even"""
    if is_odd:
       
        return """SELECT 
    u.user_id,
    u.name,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_spent
FROM 
    users u
JOIN 
    orders o ON u.user_id = o.user_id
WHERE 
    o.order_date >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
GROUP BY 
    u.user_id, u.name
HAVING 
    COUNT(o.order_id) > 5
ORDER BY 
    total_spent DESC
LIMIT 10;"""
    else:
       
        return """SELECT 
    p.product_id,
    p.product_name,
    SUM(oi.quantity) AS total_quantity_sold,
    SUM(oi.quantity * oi.unit_price) AS total_revenue
FROM 
    products p
JOIN 
    order_items oi ON p.product_id = oi.product_id
JOIN 
    orders o ON oi.order_id = o.order_id
WHERE 
    o.order_date BETWEEN '2023-01-01' AND '2023-12-31'
    AND p.category = 'Electronics'
GROUP BY 
    p.product_id, p.product_name
ORDER BY 
    total_revenue DESC
LIMIT 5;"""

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