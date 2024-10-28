# customer_service.py
import http.client
import urllib.parse
import os
import json
import ssl
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Disable SSL verification for http.client
ssl_context = ssl._create_unverified_context()

# Base URL and account information for API
auth_url = "ion.tdsynnex.com"
account_id = "17044"  # Set to your mandatory account ID

def list_customers(pageSize=10):
    """
    List customers with mandatory filters: accountId and pageSize,
    and extract customerName, customerOrganization, and accountNumber.
    """
    access_token = os.getenv("ACCESS_TOKEN")
    if not access_token:
        logger.error("No ACCESS_TOKEN found in .env. Please obtain a token first.")
        return {"error": "No access token found."}

    # Prepare headers with the access token
    headers = {
        'Authorization': f"Bearer {access_token}",
        'accept': "application/json"
    }

    # Mandatory query parameters
    filters = {
        "pageSize": pageSize
    }

    # Encode query parameters
    query_params = urllib.parse.urlencode(filters)
    endpoint = f"/api/v3/accounts/{account_id}/customers?{query_params}"

    try:
        # Make the GET request
        logger.debug("Requesting customer list with mandatory filters: %s", filters)
        conn = http.client.HTTPSConnection(auth_url, context=ssl_context)
        conn.request("GET", endpoint, headers=headers)
        
        # Get and process the response
        response = conn.getresponse()
        data = response.read().decode("utf-8")
        
        if response.status == 200:
            logger.info("Successfully retrieved customer data.")
            customers = json.loads(data).get("customers", [])

            # Extract required fields for each customer
            customer_data = []
            for customer in customers:
                name_field = customer.get("name", "")
                account_number = name_field.split("/customers/")[-1] if "/customers/" in name_field else None
                
                customer_data.append({
                    "customerName": customer.get("customerName", "N/A"),
                    "customerOrganization": customer.get("customerOrganization", "N/A"),
                    "accountNumber": account_number
                })

            return customer_data  # Return the list of processed customer data

        else:
            logger.error("Error retrieving customers: %s - %s", response.status, data)
            return {"error": f"{response.status} - {data}"}

    except Exception as e:
        logger.error("Exception occurred while retrieving customers: %s", e)
        return {"error": str(e)}

def get_customer_details(customer_id):
    """
    Retrieve details for a specific customer using account_id and customer_id.
    """
    access_token = os.getenv("ACCESS_TOKEN")
    if not access_token:
        logger.error("No ACCESS_TOKEN found in .env. Please obtain a token first.")
        return {"error": "No access token found."}

    headers = {
        'Authorization': f"Bearer {access_token}",
        'accept': "application/json"
    }

    endpoint = f"/api/v3/accounts/{account_id}/customers/{customer_id}"

    try:
        # Make the GET request
        logger.debug("Requesting details for customer ID: %s", customer_id)
        conn = http.client.HTTPSConnection(auth_url, context=ssl_context)
        conn.request("GET", endpoint, headers=headers)
        
        # Get and process the response
        response = conn.getresponse()
        data = response.read().decode("utf-8")
        
        if response.status == 200:
            logger.info("Successfully retrieved customer details.")
            customer_details = json.loads(data)
            return customer_details
        else:
            logger.error("Error retrieving customer details: %s - %s", response.status, data)
            return {"error": f"{response.status} - {data}"}

    except Exception as e:
        logger.error("Exception occurred while retrieving customer details: %s", e)
        return {"error": str(e)}
