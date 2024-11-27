
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