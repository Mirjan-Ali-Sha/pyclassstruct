<<<<<<< HEAD
"""
Sample Python script with multiple related functions for testing PyStruct.

This file contains functions that work together, which PyStruct should 
detect and group into classes.
"""

# Global configuration
DATABASE_URL = "postgresql://localhost/mydb"
MAX_RETRIES = 3
TIMEOUT = 30

# User management functions
def create_user(username, email, password):
    """Create a new user in the database."""
    user_data = validate_user_data(username, email)
    hashed = hash_password(password)
    return save_to_database("users", {**user_data, "password": hashed})


def delete_user(user_id):
    """Delete a user by ID."""
    user = get_user(user_id)
    if user:
        return delete_from_database("users", user_id)
    return False


def update_user(user_id, **kwargs):
    """Update user information."""
    user = get_user(user_id)
    if not user:
        return None
    return update_in_database("users", user_id, kwargs)


def get_user(user_id):
    """Get a user by ID."""
    return query_database("users", {"id": user_id})


def validate_user_data(username, email):
    """Validate user data before saving."""
    if not username or len(username) < 3:
        raise ValueError("Username must be at least 3 characters")
    if not validate_email(email):
        raise ValueError("Invalid email address")
    return {"username": username, "email": email}


# Database functions
def connect_database():
    """Connect to the database."""
    print(f"Connecting to {DATABASE_URL}...")
    return {"connection": True}


def query_database(table, filters):
    """Query the database."""
    conn = connect_database()
    print(f"Querying {table} with filters: {filters}")
    return {"id": 1, "name": "test"}


def save_to_database(table, data):
    """Save data to the database."""
    conn = connect_database()
    print(f"Saving to {table}: {data}")
    return {"id": 1, **data}


def delete_from_database(table, record_id):
    """Delete a record from the database."""
    conn = connect_database()
    print(f"Deleting from {table}: {record_id}")
    return True


def update_in_database(table, record_id, data):
    """Update a record in the database."""
    conn = connect_database()
    print(f"Updating {table} {record_id}: {data}")
    return {**data, "id": record_id}


# Utility functions
def hash_password(password):
    """Hash a password securely."""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()


def validate_email(email):
    """Validate an email address."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def format_date(date_obj):
    """Format a date object to string."""
    return date_obj.strftime("%Y-%m-%d")


def generate_id():
    """Generate a unique ID."""
    import uuid
    return str(uuid.uuid4())
=======
"""
Sample Python script with multiple related functions for testing PyStruct.

This file contains functions that work together, which PyStruct should 
detect and group into classes.
"""

# Global configuration
DATABASE_URL = "postgresql://localhost/mydb"
MAX_RETRIES = 3
TIMEOUT = 30

# User management functions
def create_user(username, email, password):
    """Create a new user in the database."""
    user_data = validate_user_data(username, email)
    hashed = hash_password(password)
    return save_to_database("users", {**user_data, "password": hashed})


def delete_user(user_id):
    """Delete a user by ID."""
    user = get_user(user_id)
    if user:
        return delete_from_database("users", user_id)
    return False


def update_user(user_id, **kwargs):
    """Update user information."""
    user = get_user(user_id)
    if not user:
        return None
    return update_in_database("users", user_id, kwargs)


def get_user(user_id):
    """Get a user by ID."""
    return query_database("users", {"id": user_id})


def validate_user_data(username, email):
    """Validate user data before saving."""
    if not username or len(username) < 3:
        raise ValueError("Username must be at least 3 characters")
    if not validate_email(email):
        raise ValueError("Invalid email address")
    return {"username": username, "email": email}


# Database functions
def connect_database():
    """Connect to the database."""
    print(f"Connecting to {DATABASE_URL}...")
    return {"connection": True}


def query_database(table, filters):
    """Query the database."""
    conn = connect_database()
    print(f"Querying {table} with filters: {filters}")
    return {"id": 1, "name": "test"}


def save_to_database(table, data):
    """Save data to the database."""
    conn = connect_database()
    print(f"Saving to {table}: {data}")
    return {"id": 1, **data}


def delete_from_database(table, record_id):
    """Delete a record from the database."""
    conn = connect_database()
    print(f"Deleting from {table}: {record_id}")
    return True


def update_in_database(table, record_id, data):
    """Update a record in the database."""
    conn = connect_database()
    print(f"Updating {table} {record_id}: {data}")
    return {**data, "id": record_id}


# Utility functions
def hash_password(password):
    """Hash a password securely."""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()


def validate_email(email):
    """Validate an email address."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def format_date(date_obj):
    """Format a date object to string."""
    return date_obj.strftime("%Y-%m-%d")


def generate_id():
    """Generate a unique ID."""
    import uuid
    return str(uuid.uuid4())
>>>>>>> 12342d4e14c9bffcf018c29ac3a8c2b4ba50b1a9
