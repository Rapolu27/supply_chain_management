from .exception import UserException, ProductException, SupplierException
import re
def validate_mobile_number(value):
    """Validate that the mobile number contains exactly 10 digits."""
    if not re.fullmatch(r'\d{10}', value):
        raise UserException("Mobile number must be exactly 10 digits.")

def validate_address_length(value):
    """Validate that the address is not too short."""
    if len(value.strip()) < 10:
        raise UserException("Address must be at least 10 characters long.")

def validate_username(value):
    """Ensure the username doesn't contain special characters."""
    if not re.match(r'^[a-zA-Z0-9_.-]+$', value):
        raise UserException("Username can only contain letters, numbers, underscores, periods, and hyphens.")

def validate_profile_picture(file):
    """Validate profile picture file size and format."""
    if file.size > 2 * 1024 * 1024:  # Limit size to 2 MB
        raise UserException("Profile picture file size must not exceed 2 MB.")
    if not file.content_type.startswith("image/"):
        raise UserException("Only image files are allowed for profile pictures.")

def validate_scm_user(scm_user):
    validate_username(scm_user.user.username)
    validate_mobile_number(scm_user.mobile)
    validate_address_length(scm_user.address)

def validate_quantity(value):
    """Validate that quantity is not less than 0."""
    if value < 0:
        raise ProductException("Quantity cannot be less than 0.")

def validate_unique_supplier_for_product(product, supplier, Product):
    if Product.objects.filter(name=product.name, supplier=supplier).exists():
        raise ProductException(f"The product '{product.name}' is already linked to supplier '{supplier.name}'.")

def validate_price(value):
    if value <0:
        raise ProductException("price should be greater than 0")

def validate_product(product, Product):
    validate_unique_supplier_for_product(product, product.supplier, Product)
    validate_price(product.price)
    validate_quantity(product.stock_quantity)

def validate_supplier_name(name, Supplier):
    """Ensure supplier name is unique."""
    if Supplier.objects.filter(name=name).exists():
        raise SupplierException(f"The supplier name '{name}' already exists.")

def validate_supplier_mobile(mobile):
    """Ensure the mobile number is valid."""
    if not re.match(r'^\d{10}$', mobile):
        raise SupplierException("Mobile number must be exactly 10 digits.")

def validate_active_supplier(supplier):
    """Ensure active suppliers have all required fields."""
    if supplier.active and (not supplier.address or not supplier.email):
        raise SupplierException("Active suppliers must have an email and address.")
