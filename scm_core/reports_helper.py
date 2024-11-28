from collections import defaultdict

def calculate_supplier_units_and_ratings(Supplier, PurchaseOrder):
    # Dictionary to track total units per supplier
    supplier_units = defaultdict(int)

    # Iterate over all purchase orders
    purchase_orders = PurchaseOrder.objects.all()
    for po in purchase_orders:
        supplier_id = po.supplier_id
        supplier_units[supplier_id] += po.quantity  # Assuming `quantity` is a field in PurchaseOrder

    # Update each supplier's total units and rating
    for supplier_id, total_units in supplier_units.items():
        supplier = Supplier.objects.get(id=supplier_id)
        supplier.total_units_supplied = total_units

        # Assign rating based on total units
        if total_units < 100:
            supplier.rating = 1
        elif 100 <= total_units <= 500:
            supplier.rating = 2
        elif 501 <= total_units <= 1000:
            supplier.rating = 3
        elif 1001 <= total_units <= 5000:
            supplier.rating = 4
        else:
            supplier.rating = 5

        # Save updated supplier details
        supplier.save()

    print("Supplier units and ratings updated successfully.")