# Inventory Management System

This project is an Inventory Management System that interacts with a Firestore database to manage products, palettes, and warehouses. It provides functionality for importing/exporting data, resetting collections, and processing inbound and outbound activities.

## Features

- Export and import collection data between development and production databases
- Reset product, palette, and warehouse data
- Process inbound and outbound activities
- Update product and palette information based on activities

## Requirements

- Python 3.7+
- Google Cloud Firestore
- Additional dependencies listed in `requirements.txt`

## Installation

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up your Google Cloud credentials and ensure you have the necessary service account JSON files.

## Usage

The script can be run with different command-line arguments:

- Test activities:
  ```
  python importexport.py test
  ```

- Reset test data:
  ```
  python importexport.py reset-test
  ```

- Push activities to the database:
  ```
  python importexport.py push
  ```

- Reset all collections:
  ```
  python importexport.py reset-all
  ```

- Get product name by ID:
  ```
  python importexport.py get-product-name <product_id>
  ```

## Main Functions

- `export_all_collection_data()`: Exports data from development to production database
- `reset_product_palettes()`: Resets specific product and palette data
- `reset_all_products()`, `reset_all_warehouses()`, `reset_all_palettes()`: Reset all data in respective collections
- `test_activities()`: Run test activities
- `add_activities()`: Process and add activities to the database
- `update_palettes_collection()`, `update_products_collection()`: Update collections based on activities

## Note

Ensure you have the correct permissions and service account JSON files set up for both development and production environments before running the script.