"""
Sample Python script with magic method patterns for testing PyClassStruct.

This file demonstrates how functions can be organized into classes with
proper __init__, __str__, __repr__, and other magic methods.
"""

# Product-related global state
product_cache = {}
DEFAULT_CURRENCY = "USD"

# Product initialization and setup
def init_product(product_id, name, price):
    """Initialize a new product."""
    product_data = {
        'id': product_id,
        'name': name,
        'price': price,
        'currency': DEFAULT_CURRENCY
    }
    product_cache[product_id] = product_data
    return product_data


def create_product(name, price, category=None):
    """Create a product with auto-generated ID."""
    product_id = generate_product_id()
    product = init_product(product_id, name, price)
    if category:
        product['category'] = category
    return product


def get_product(product_id):
    """Get a product by ID."""
    return product_cache.get(product_id)


def update_product(product_id, **kwargs):
    """Update product attributes."""
    product = get_product(product_id)
    if product:
        product.update(kwargs)
    return product


def delete_product(product_id):
    """Delete a product from cache."""
    if product_id in product_cache:
        del product_cache[product_id]
        return True
    return False


def product_to_string(product_id):
    """Convert product to string representation."""
    product = get_product(product_id)
    if product:
        return f"Product({product['name']}, ${product['price']})"
    return "Product(None)"


def product_to_repr(product_id):
    """Get detailed product representation."""
    product = get_product(product_id)
    if product:
        return f"Product(id={product['id']}, name='{product['name']}', price={product['price']})"
    return "Product()"


def compare_products(product_id1, product_id2):
    """Compare two products by price."""
    p1 = get_product(product_id1)
    p2 = get_product(product_id2)
    if p1 and p2:
        return p1['price'] - p2['price']
    return 0


def products_equal(product_id1, product_id2):
    """Check if two products are equal."""
    p1 = get_product(product_id1)
    p2 = get_product(product_id2)
    return p1 == p2


def product_hash(product_id):
    """Get hash of a product."""
    product = get_product(product_id)
    if product:
        return hash((product['id'], product['name']))
    return 0


def iter_products():
    """Iterate over all products."""
    return iter(product_cache.values())


def count_products():
    """Get the number of products."""
    return len(product_cache)


def contains_product(product_id):
    """Check if product exists."""
    return product_id in product_cache


def get_product_item(product_id, key):
    """Get a specific attribute of a product."""
    product = get_product(product_id)
    if product and key in product:
        return product[key]
    return None


def set_product_item(product_id, key, value):
    """Set a specific attribute of a product."""
    product = get_product(product_id)
    if product:
        product[key] = value


# Utility functions
def generate_product_id():
    """Generate a unique product ID."""
    import uuid
    return str(uuid.uuid4())[:8]


def format_price(price, currency=None):
    """Format price with currency."""
    curr = currency or DEFAULT_CURRENCY
    if curr == "USD":
        return f"${price:.2f}"
    elif curr == "EUR":
        return f"€{price:.2f}"
    return f"{price:.2f} {curr}"


def validate_product_data(name, price):
    """Validate product data."""
    if not name or len(name) < 2:
        raise ValueError("Product name must be at least 2 characters")
    if price < 0:
        raise ValueError("Price cannot be negative")
    return True


def product_enter(product_id):
    """Context manager enter."""
    print(f"Entering product context: {product_id}")
    return get_product(product_id)


def product_exit(product_id, exc_type, exc_val, exc_tb):
    """Context manager exit."""
    print(f"Exiting product context: {product_id}")
    return False


def call_product(product_id, action):
    """Make a product callable - perform an action."""
    actions = {
        'info': lambda p: product_to_string(p['id']),
        'price': lambda p: format_price(p['price']),
        'delete': lambda p: delete_product(p['id']),
    }
    product = get_product(product_id)
    if product and action in actions:
        return actions[action](product)
    return None
