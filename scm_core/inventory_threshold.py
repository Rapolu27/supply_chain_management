from datetime import datetime

def get_out_of_range_products(inventory):
    """
    Find products that do not fall within their min and max stock limits.
    :param inventory: Queryset or list of inventory items with fields 
                      product_id, stock, min_stock, max_stock.
    :return: List of products out of stock range.
    """
    out_of_range = []
    print('inventories: ', inventory)
    for item in inventory:
        if item.stock < item.min_stock or item.stock > item.max_stock:
            out_of_range.append(item)
    print('out_of_range_products: ', out_of_range)
    return out_of_range

def create_auto_purchase_orders(inventories, suppliers):
    """
    Create purchase orders for products below their min stock limit.
    :param products: List of products with product_id and min_stock details.
    :param supplier_id: Supplier ID to associate with the purchase order.
    :return: List of generated purchase orders.
    """
    purchase_orders = []
    for inv in inventories:
        if inv.stock < inv.min_stock:
            quantity_to_order = inv.max_stock - inv.stock
            # supplier = suppliers.filter(products_in=inv.product)
            purchase_order = {
                "product_id": inv.product.id,
                "supplier_id": inv.product.supplier.id,
                "quantity": quantity_to_order,
                "status": "Pending",
                "order_date": datetime.now(),
            }
            purchase_orders.append(purchase_order)
    print('auto purchase_orders : ', purchase_orders)
    return purchase_orders
