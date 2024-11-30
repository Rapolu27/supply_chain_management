from datetime import datetime, timedelta
def filter_already_scheduled_po(PurchaseOrder, out_of_range_products):
     # Filter out products that already have pending purchase orders
    products_with_pending_po = set(
        PurchaseOrder.objects.filter(
            status="pending"
        ).values_list("product_id", flat=True)
    )
    out_of_range_products = [
        product for product in out_of_range_products if product.product_id not in products_with_pending_po
    ]
    return out_of_range_products


def get_date_for_filters(filter_type):
    today = datetime.now()

    # Calculate start date based on filter
    if filter_type == '1D':
        start_date = today - timedelta(days=1)
    elif filter_type == '1W':
        start_date = today - timedelta(weeks=1)
    elif filter_type == '1M':
        start_date = today - timedelta(days=30)
    elif filter_type == '3M':
        start_date = today - timedelta(days=90)
    elif filter_type == '6M':
        start_date = today - timedelta(days=180)
    else:
        start_date = today - timedelta(days=30)  # Fallback to last month
    return start_date

