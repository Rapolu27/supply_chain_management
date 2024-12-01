# supply_chain_management

## Project Overview

The Supply Chain Management System (SCM) is a lightweight Django-based application designed for managing suppliers, products, purchase orders, and inventory with CRUD operations. The system includes a library that provides reusable functionalities such as data validation, filtering, calculations, and business logic.

The project also integrates AWS services like AWS Lambda for automating processes, RDS for managing relational data, and S3 for storing static files, images.

## Features
### Core Features

    <strong>Supplier Management:</strong> Add, edit, and rate suppliers based on performance.
    <strong>Product Inventory Management:</strong> Manage product stock, set min/max limits, and track supplier-product mappings.
    <strong>Purchase Orders:</strong> Generate, track, and manage purchase orders with automated workflows.
    <strong>Reports:</strong> Generate and filter reports for purchase orders and supplier ratings.
    <strong>GRN (Goods Received Note) Inward Processing:</strong> Automate stock updates for received orders.

## Library Features

    The SCM library(<strong>scm_core</strong>) provides reusable modules for:

    Validations: Custom validators for suppliers, products, and orders.
    Calculations: Supplier ratings, stock-level checks, and automated purchase order generation.
    Filtering and Sorting: Utilities for filtering data by date, supplier, or product.

