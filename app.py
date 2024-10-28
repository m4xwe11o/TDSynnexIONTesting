import http.client
import urllib.parse
import os
import json
import ssl
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
from customer_service import list_customers
from customer_service import get_customer_details
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Base URL for API
auth_url = "ion.tdsynnex.com"

# Disable SSL verification for http.client
ssl_context = ssl._create_unverified_context()

def save_to_env(key, value):
    """
    Save a key-value pair to the .env file.
    """
    env_file_path = ".env"
    with open(env_file_path, "r") as file:
        lines = file.readlines()
    
    # Update if key exists, else append
    updated = False
    with open(env_file_path, "w") as file:
        for line in lines:
            if line.startswith(f"{key}="):
                file.write(f"{key}={value}\n")
                updated = True
            else:
                file.write(line)
        if not updated:
            file.write(f"{key}={value}\n")
    logger.debug(f"Saved {key} to .env with value: {value}")

def request_oauth_token():
    """
    Request a new OAuth token using the refresh token and save it to .env.
    """
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'accept': "application/json"
    }
    form_data = {
        'grant_type': "refresh_token",
        'refresh_token': os.getenv("REFRESH_TOKEN")
    }
    encoded_form_data = urllib.parse.urlencode(form_data)
    
    try:
        logger.debug("Requesting new OAuth token with refresh token.")
        conn = http.client.HTTPSConnection(auth_url, context=ssl_context)
        conn.request("POST", "/oauth/token", headers=headers, body=encoded_form_data)
        response = conn.getresponse()
        data = response.read().decode("utf-8")
        
        if response.status == 200:
            token_data = json.loads(data)
            access_token = token_data.get("access_token")
            if access_token:
                save_to_env("ACCESS_TOKEN", access_token)
                logger.info("New access token received and saved to .env.")
            return access_token
        else:
            logger.error(f"Failed to retrieve token: {response.status} - {data}")
            return None
    except Exception as e:
        logger.error(f"Error during token request: {e}")
        return None

def validate_access_token():
    """
    Validate the access token to ensure it is still valid.
    """
    access_token = os.getenv("ACCESS_TOKEN")
    if not access_token:
        logger.debug("No access token available in .env for validation.")
        return False
    
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'accept': "application/json"
    }
    form_data = {
        'access_token': access_token
    }
    encoded_form_data = urllib.parse.urlencode(form_data)

    try:
        logger.debug("Validating existing access token.")
        conn = http.client.HTTPSConnection(auth_url, context=ssl_context)
        conn.request("POST", "/oauth/validateAccess", headers=headers, body=encoded_form_data)
        response = conn.getresponse()
        data = response.read().decode("utf-8")
        
        if response.status == 200:
            logger.info("Access token is valid.")
            return True
        else:
            logger.warning(f"Access token is invalid: {response.status} - {data}")
            return False
    except Exception as e:
        logger.error(f"Error during token validation: {e}")
        return False

@app.route("/get-refresh-token", methods=["GET"])
def get_refresh_token():
    """
    Return the current REFRESH_TOKEN value if it exists.
    """
    refresh_token = os.getenv("REFRESH_TOKEN", "")
    return jsonify({"refresh_token": refresh_token})

@app.route("/update-refresh-token", methods=["POST"])
def update_refresh_token():
    """
    Update the REFRESH_TOKEN value.
    """
    new_refresh_token = request.json.get("refresh_token", "")
    if new_refresh_token:
        save_to_env("REFRESH_TOKEN", new_refresh_token)
        return jsonify({"message": "REFRESH_TOKEN updated successfully", "refresh_token": new_refresh_token})
    else:
        return jsonify({"error": "No REFRESH_TOKEN provided"}), 400

@app.route("/get-token", methods=["POST"])
def get_token():
    """
    Handle access token request and validation.
    """
    logger.debug("Received request to obtain access token.")
    access_token = os.getenv("ACCESS_TOKEN")
    
    if not access_token:
        logger.info("ACCESS_TOKEN is empty; requesting a new token.")
        access_token = request_oauth_token()
        if access_token:
            logger.info("New access token obtained and returned.")
            return jsonify({"access_token": access_token, "status": "New token requested and saved"})
        else:
            logger.error("Failed to obtain a new access token.")
            return jsonify({"error": "Failed to obtain a new access token"}), 500
    else:
        logger.info("ACCESS_TOKEN exists; proceeding to validate the token.")
        if validate_access_token():
            logger.info("ACCESS_TOKEN is valid; returning existing token.")
            return jsonify({"access_token": access_token, "status": "Token is valid"})
        else:
            logger.warning("ACCESS_TOKEN is invalid; requesting a new token.")
            access_token = request_oauth_token()
            if access_token:
                logger.info("Invalid token replaced with a new token.")
                return jsonify({"access_token": access_token, "status": "Invalid token, new token requested and saved"})
            else:
                logger.error("Failed to obtain a new access token after invalid token detected.")
                return jsonify({"error": "Failed to obtain a new access token"}), 500

# Route to list customers with only mandatory parameters
@app.route("/list-customers", methods=["POST"])
def list_customers_route():
    """
    Endpoint to list customers with the mandatory filters: accountId and pageSize,
    and returns customerName, customerOrganization, and accountNumber for each customer.
    """
    page_size = 100

    try:
        page_size = int(page_size)
    except ValueError:
        logger.warning("Invalid pageSize provided; defaulting to 100.")
        page_size = 100

    result = list_customers(pageSize=page_size)
    return jsonify(result)

@app.route("/get-customer-details/<customer_id>", methods=["GET"])
def get_customer_details_route(customer_id):
    """
    Endpoint to retrieve details of a specific customer.
    """
    result = get_customer_details(customer_id)
    return jsonify(result)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
