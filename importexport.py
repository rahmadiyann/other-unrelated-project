from google.cloud import firestore
import sys
from operator import itemgetter
import pandas as pd

prod_db = firestore.Client.from_service_account_json("serviceaccount/bugel_serviceaccount.json")
dev_db = firestore.Client.from_service_account_json("serviceaccount/mli_serviceaccount.json")

units = ['bags','kgm','meters','pallets','rolls','sheets','sqm','yards']

def export_all_collection_data():
    collections = ['warehouses', 'products', 'palettes']
    count_collection = 1
    for collection in collections:
        docs = dev_db.collection(collection).stream()
        print(f"{count_collection}: {collection}")
        count_doc = 1
        for doc in docs:
            doc_dict = doc.to_dict()
            print(f"{count_doc}: {doc.id}")
            count_doc+=1
            prod_db.collection(collection).document(doc.id).set(doc_dict)
            print(f"exported {doc.id} from {collection} to prod database")

def reset_product_palettes():
    product_id = ['0SRwjeYXSTf1M3aP1wcz', '0kTWFpBSZZhJvev0khrm']
    palette_id = ['4shAMbwouDqXMWcj64uj', '9CXi0rnd24soRftruboC']
    for product in product_id:
        product_doc = dev_db.collection('products').document(product).get()
        product_dict = product_doc.to_dict()
        for unit in units:
            product_dict[unit] = 0
        product_dict['palettes'] = []
        dev_db.collection('products').document(product).update(product_dict)
        print(f"reset palettes field to [] for {product} in products collection")
    for palette in palette_id:
        palette_doc = dev_db.collection('palettes').document(palette).get()
        palette_dict = palette_doc.to_dict()
        palette_dict['products'] = []
        palette_dict['soStatus'] = 'Unconfirmed'
        palette_dict['whid'] = ''
        palette_dict['whname'] = ''
        dev_db.collection('palettes').document(palette).update(palette_dict)
        print(f"reset products field to [] for {palette} in palettes collection")
        
# reset unit to 0 on all products and clear palettes field to []
def reset_all_products():
    docs = dev_db.collection('products').stream()
    for doc in docs:
        doc_dict = doc.to_dict()
        for unit in units:
            doc_dict[unit] = 0
        doc_dict['palettes'] = []
        dev_db.collection('products').document(doc.id).update(doc_dict)
        print(f"reset {doc.id} in products collection")
        
# reset palettes field to [] in warehouse collection
def reset_all_warehouses():
    docs = dev_db.collection('warehouses').stream()
    for doc in docs:
        doc_dict = doc.to_dict()
        doc_dict['palettes'] = []
        dev_db.collection('warehouses').document(doc.id).update(doc_dict)
        print(f"reset {doc.id} in warehouses collection")
        
# reset product field on palettes collection to [] and set soStatus to 'Unconfirmed', and set whid = '' and whname = ''
def reset_all_palettes():
    docs = dev_db.collection('palettes').stream()
    for doc in docs:
        doc_dict = doc.to_dict()
        doc_dict['products'] = []
        doc_dict['soStatus'] = 'Unconfirmed'
        doc_dict['whid'] = ''
        doc_dict['whname'] = ''
        dev_db.collection('palettes').document(doc.id).update(doc_dict)
        print(f"reset {doc.id} in palettes collection")
        
# get warehouse name by id
def get_warehouse_name(whid):
    doc = dev_db.collection('warehouses').document(whid).get()
    return doc.to_dict()['name']

# get product name by id
def get_product_name(prodid):
    doc = dev_db.collection('products').document(prodid).get()
    return doc.to_dict()['name']

# get palette name by id
def get_palette_name(palid):
    doc = dev_db.collection('palettes').document(palid).get()
    return doc.to_dict()['name']

def test_activities():
    outbound_datas = [
        # {
        #     'type': 'Outbound',
        #     'unit': 'Rolls',
        #     'qty': 40,
        #     'palette_id': '4shAMbwouDqXMWcj64uj',
        #     'palette_name': '28',
        #     'product_id': '0SRwjeYXSTf1M3aP1wcz',
        #     'product_name': 'MESH HF DL 1393 CDP-P EM PRIMEBLUE EPM5 A0QM/AA2U',
        #     'whid': 'o7V4g7Cp0zAMcPq94IF3',
        #     'whname': 'WAREHOUSE 1'
        # },
        # {
        #     'type': 'Outbound',
        #     'unit': 'Bags',
        #     'qty': 40,
        #     'palette_id': '4shAMbwouDqXMWcj64uj',
        #     'palette_name': '28',
        #     'product_id': '0SRwjeYXSTf1M3aP1wcz',
        #     'product_name': 'MESH HF DL 1393 CDP-P EM PRIMEBLUE EPM5 A0QM/AA2U',
        #     'whid': 'o7V4g7Cp0zAMcPq94IF3',
        #     'whname': 'WAREHOUSE 1'
        # },
        # {
        #     'type': 'Outbound',
        #     'unit': 'Rolls',
        #     'qty': 40,
        #     'palette_id': '9CXi0rnd24soRftruboC',
        #     'palette_name': '22',
        #     'product_id': '0SRwjeYXSTf1M3aP1wcz',
        #     'product_name': 'MESH HF DL 1393 CDP-P EM PRIMEBLUE EPM5 A0QM/AA2U',
        #     'whid': 'o7V4g7Cp0zAMcPq94IF3',
        #     'whname': 'WAREHOUSE 1'
        # },
        # {
        #     'type': 'Outbound',
        #     'unit': 'Bags',
        #     'qty': 40,
        #     'palette_id': '9CXi0rnd24soRftruboC',
        #     'palette_name': '22',
        #     'product_id': '0SRwjeYXSTf1M3aP1wcz',
        #     'product_name': 'MESH HF DL 1393 CDP-P EM PRIMEBLUE EPM5 A0QM/AA2U',
        #     'whid': 'o7V4g7Cp0zAMcPq94IF3',
        #     'whname': 'WAREHOUSE 1'
        # },
        # {
        #     'type': 'Outbound',
        #     'unit': 'Meters',
        #     'qty': 40,
        #     'palette_id': '9CXi0rnd24soRftruboC',
        #     'palette_name': '22',
        #     'product_id': '0kTWFpBSZZhJvev0khrm',
        #     'product_name': 'NON WOVEN FORCETAPE SH610AD GREY 138CM"',
        #     'whid': 'o7V4g7Cp0zAMcPq94IF3',
        #     'whname': 'WAREHOUSE 1'
        # },
        # {
        #     'type': 'Outbound',
        #     'unit': 'KGM',
        #     'qty': 40,
        #     'palette_id': '9CXi0rnd24soRftruboC',
        #     'palette_name': '22',
        #     'product_id': '0kTWFpBSZZhJvev0khrm',
        #     'product_name': 'NON WOVEN FORCETAPE SH610AD GREY 138CM"',
        #     'whid': 'o7V4g7Cp0zAMcPq94IF3',
        #     'whname': 'WAREHOUSE 1'
        # },
        # {
        #     'type': 'Outbound',
        #     'unit': 'Meters',
        #     'qty': 40,
        #     'palette_id': '4shAMbwouDqXMWcj64uj',
        #     'palette_name': '28',
        #     'product_id': '0kTWFpBSZZhJvev0khrm',
        #     'product_name': 'NON WOVEN FORCETAPE SH610AD GREY 138CM"',
        #     'whid': 'o7V4g7Cp0zAMcPq94IF3',
        #     'whname': 'WAREHOUSE 1'
        # },
        # {
        #     'type': 'Outbound',
        #     'unit': 'KGM',
        #     'qty': 40,
        #     'palette_id': '4shAMbwouDqXMWcj64uj',
        #     'palette_name': '28',
        #     'product_id': '0kTWFpBSZZhJvev0khrm',
        #     'product_name': 'NON WOVEN FORCETAPE SH610AD GREY 138CM"',
        #     'whid': 'o7V4g7Cp0zAMcPq94IF3',
        #     'whname': 'WAREHOUSE 1'
        # },
        {
            'type': 'Outbound',
            'unit': 'Sheets',
            'qty': 340,
            'palette_id': '4shAMbwouDqXMWcj64uj',
            'palette_name': '28',
            'product_id': '0SRwjeYXSTf1M3aP1wcz',
            'product_name': 'MESH HF DL 1393 CDP-P EM PRIMEBLUE EPM5 A0QM/AA2U',
            'whid': 'o7V4g7Cp0zAMcPq94IF3',
            'whname': 'WAREHOUSE 1'
        },
    ]
    inbound_datas = [
        {
            'type': 'Inbound',
            'unit': 'Sheets',
            'qty': 340,
            'palette_id': '4shAMbwouDqXMWcj64uj',
            'palette_name': '28',
            'product_id': '0SRwjeYXSTf1M3aP1wcz',
            'product_name': 'MESH HF DL 1393 CDP-P EM PRIMEBLUE EPM5 A0QM/AA2U',
            'whid': 'o7V4g7Cp0zAMcPq94IF3',
            'whname': 'WAREHOUSE 1'
        },
        # {
        #     'type': 'Inbound',
        #     'unit': 'Bags',
        #     'qty': 340,
        #     'palette_id': '4shAMbwouDqXMWcj64uj',
        #     'palette_name': '28',
        #     'product_id': '0SRwjeYXSTf1M3aP1wcz',
        #     'product_name': 'MESH HF DL 1393 CDP-P EM PRIMEBLUE EPM5 A0QM/AA2U',
        #     'whid': 'o7V4g7Cp0zAMcPq94IF3',
        #     'whname': 'WAREHOUSE 1'
        # },
        # {
        #     'type': 'Inbound',
        #     'unit': 'Rolls',
        #     'qty': 340,
        #     'palette_id': '9CXi0rnd24soRftruboC',
        #     'palette_name': '22',
        #     'product_id': '0SRwjeYXSTf1M3aP1wcz',
        #     'product_name': 'MESH HF DL 1393 CDP-P EM PRIMEBLUE EPM5 A0QM/AA2U',
        #     'whid': 'o7V4g7Cp0zAMcPq94IF3',
        #     'whname': 'WAREHOUSE 1'
        # },
        # {
        #     'type': 'Inbound',
        #     'unit': 'Bags',
        #     'qty': 340,
        #     'palette_id': '9CXi0rnd24soRftruboC',
        #     'palette_name': '22',
        #     'product_id': '0SRwjeYXSTf1M3aP1wcz',
        #     'product_name': 'MESH HF DL 1393 CDP-P EM PRIMEBLUE EPM5 A0QM/AA2U',
        #     'whid': 'o7V4g7Cp0zAMcPq94IF3',
        #     'whname': 'WAREHOUSE 1'
        # },
        # {
        #     'type': 'Inbound',
        #     'unit': 'Meters',
        #     'qty': 340,
        #     'palette_id': '9CXi0rnd24soRftruboC',
        #     'palette_name': '22',
        #     'product_id': '0kTWFpBSZZhJvev0khrm',
        #     'product_name': 'NON WOVEN FORCETAPE SH610AD GREY 138CM"',
        #     'whid': 'o7V4g7Cp0zAMcPq94IF3',
        #     'whname': 'WAREHOUSE 1'
        # },
        # {
        #     'type': 'Inbound',
        #     'unit': 'KGM',
        #     'qty': 340,
        #     'palette_id': '9CXi0rnd24soRftruboC',
        #     'palette_name': '22',
        #     'product_id': '0kTWFpBSZZhJvev0khrm',
        #     'product_name': 'NON WOVEN FORCETAPE SH610AD GREY 138CM"',
        #     'whid': 'o7V4g7Cp0zAMcPq94IF3',
        #     'whname': 'WAREHOUSE 1'
        # },
        # {
        #     'type': 'Inbound',
        #     'unit': 'Meters',
        #     'qty': 340,
        #     'palette_id': '4shAMbwouDqXMWcj64uj',
        #     'palette_name': '28',
        #     'product_id': '0kTWFpBSZZhJvev0khrm',
        #     'product_name': 'NON WOVEN FORCETAPE SH610AD GREY 138CM"',
        #     'whid': 'o7V4g7Cp0zAMcPq94IF3',
        #     'whname': 'WAREHOUSE 1'
        # },
        # {
        #     'type': 'Inbound',
        #     'unit': 'KGM',
        #     'qty': 340,
        #     'palette_id': '4shAMbwouDqXMWcj64uj',
        #     'palette_name': '28',
        #     'product_id': '0kTWFpBSZZhJvev0khrm',
        #     'product_name': 'NON WOVEN FORCETAPE SH610AD GREY 138CM"',
        #     'whid': 'o7V4g7Cp0zAMcPq94IF3',
        #     'whname': 'WAREHOUSE 1'
        # },
        # {
        #     'type': 'Inbound',
        #     'unit': 'Rolls',
        #     'qty': 340,
        #     'palette_id': '4shAMbwouDqXMWcj64uj',
        #     'palette_name': '28',
        #     'product_id': '0SRwjeYXSTf1M3aP1wcz',
        #     'product_name': 'MESH HF DL 1393 CDP-P EM PRIMEBLUE EPM5 A0QM/AA2U',
        #     'whid': 'o7V4g7Cp0zAMcPq94IF3',
        #     'whname': 'WAREHOUSE 1'
        # },
        # {
        #     'type': 'Inbound',
        #     'unit': 'Bags',
        #     'qty': 340,
        #     'palette_id': '4shAMbwouDqXMWcj64uj',
        #     'palette_name': '28',
        #     'product_id': '0SRwjeYXSTf1M3aP1wcz',
        #     'product_name': 'MESH HF DL 1393 CDP-P EM PRIMEBLUE EPM5 A0QM/AA2U',
        #     'whid': 'o7V4g7Cp0zAMcPq94IF3',
        #     'whname': 'WAREHOUSE 1'
        # },
        # {
        #     'type': 'Inbound',
        #     'unit': 'Rolls',
        #     'qty': 340,
        #     'palette_id': '9CXi0rnd24soRftruboC',
        #     'palette_name': '22',
        #     'product_id': '0SRwjeYXSTf1M3aP1wcz',
        #     'product_name': 'MESH HF DL 1393 CDP-P EM PRIMEBLUE EPM5 A0QM/AA2U',
        #     'whid': 'o7V4g7Cp0zAMcPq94IF3',
        #     'whname': 'WAREHOUSE 1'
        # },
        # {
        #     'type': 'Inbound',
        #     'unit': 'Bags',
        #     'qty': 340,
        #     'palette_id': '9CXi0rnd24soRftruboC',
        #     'palette_name': '22',
        #     'product_id': '0SRwjeYXSTf1M3aP1wcz',
        #     'product_name': 'MESH HF DL 1393 CDP-P EM PRIMEBLUE EPM5 A0QM/AA2U',
        #     'whid': 'o7V4g7Cp0zAMcPq94IF3',
        #     'whname': 'WAREHOUSE 1'
        # },
        # {
        #     'type': 'Inbound',
        #     'unit': 'Meters',
        #     'qty': 340,
        #     'palette_id': '9CXi0rnd24soRftruboC',
        #     'palette_name': '22',
        #     'product_id': '0kTWFpBSZZhJvev0khrm',
        #     'product_name': 'NON WOVEN FORCETAPE SH610AD GREY 138CM"',
        #     'whid': 'o7V4g7Cp0zAMcPq94IF3',
        #     'whname': 'WAREHOUSE 1'
        # },
        # {
        #     'type': 'Inbound',
        #     'unit': 'KGM',
        #     'qty': 340,
        #     'palette_id': '9CXi0rnd24soRftruboC',
        #     'palette_name': '22',
        #     'product_id': '0kTWFpBSZZhJvev0khrm',
        #     'product_name': 'NON WOVEN FORCETAPE SH610AD GREY 138CM"',
        #     'whid': 'o7V4g7Cp0zAMcPq94IF3',
        #     'whname': 'WAREHOUSE 1'
        # },
        # {
        #     'type': 'Inbound',
        #     'unit': 'Meters',
        #     'qty': 340,
        #     'palette_id': '4shAMbwouDqXMWcj64uj',
        #     'palette_name': '28',
        #     'product_id': '0kTWFpBSZZhJvev0khrm',
        #     'product_name': 'NON WOVEN FORCETAPE SH610AD GREY 138CM"',
        #     'whid': 'o7V4g7Cp0zAMcPq94IF3',
        #     'whname': 'WAREHOUSE 1'
        # },
        # {
        #     'type': 'Inbound',
        #     'unit': 'KGM',
        #     'qty': 340,
        #     'palette_id': '4shAMbwouDqXMWcj64uj',
        #     'palette_name': '28',
        #     'product_id': '0kTWFpBSZZhJvev0khrm',
        #     'product_name': 'NON WOVEN FORCETAPE SH610AD GREY 138CM"',
        #     'whid': 'o7V4g7Cp0zAMcPq94IF3',
        #     'whname': 'WAREHOUSE 1'
        # },
    ]
    # for data in inbound_datas:
        
    #     activity_type = data['type']
    #     unit = data['unit'].lower()
    #     qty = data['qty']
    #     palette_id = data['palette_id']
    #     palette_name = data['palette_name']
    #     product_id = data['product_id']
    #     product_name = data['product_name']
    #     whid = data['whid']
    #     whname = data['whname']
        
    #     update_palettes_collection(activity_type, palette_id, product_id, product_name, unit, qty, whid, whname)
    #     update_products_collection(activity_type, product_id, unit, qty, palette_id, palette_name)
        
    for data in outbound_datas:
        
        activity_type = data['type']
        unit = data['unit'].lower()
        qty = data['qty']
        palette_id = data['palette_id']
        palette_name = data['palette_name']
        product_id = data['product_id']
        product_name = data['product_name']
        whid = data['whid']
        whname = data['whname']
        
        update_palettes_collection(activity_type, palette_id, product_id, product_name, unit, qty, whid, whname)
        update_products_collection(activity_type, product_id, unit, qty, palette_id, palette_name)
    
    print("===FINISHED===")
        
def update_palettes_collection(activity_type, palette_id, product_id, product_name, unit, qty, whid, whname, activity_id):
    print(f"===UPDATING PALETTES COLLECTION: {get_palette_name(palette_id)}===")
    
    palette_doc = dev_db.collection('palettes').document(palette_id).get()
    palette_data = palette_doc.to_dict()
    product_list = palette_data.get('products', [])
    print(f"product list before update: {product_list}")
    
    dev_db.collection('palettes').document(palette_id).update({
        'whid': whid, 
        'whname': whname,
        'soStatus': 'Unconfirmed'
    })
    
    product_found = False
    for product in product_list:
        if product['productId'] == product_id:
            product_found = True
            if unit in product['qty_list']:
                if activity_type == 'Inbound':
                    product['qty_list'][unit] += qty
                elif activity_type == 'Outbound':
                    product['qty_list'][unit] = max(0, product['qty_list'][unit] - qty)
                    # if after subtracting qty the unit qty is 0, remove the unit from the qty_list
                    if product['qty_list'][unit] == 0:
                        del product['qty_list'][unit]
            else:
                if activity_type == 'Inbound':
                    product['qty_list'][unit] = qty
                else:
                    print(f"Warning: Unit {unit} not found for product {product_id} in palette {palette_id}. Skipping...")
            break
    
    if not product_found and activity_type == 'Inbound':
        product_list.append({
            "productId": product_id,
            "productName": product_name,
            "qty_list": {unit: qty}
        })
    elif not product_found and activity_type == 'Outbound':
        print(f"Warning: Product {product_id} not found in palette {palette_id} for outbound activity. Skipping...")

    print(f"product list after update: {product_list}")
    dev_db.collection('palettes').document(palette_id).update({'products': product_list})
                    
def update_products_collection(activity_type, product_id, unit, qty, palette_id, palette_name, activity_id):
    print(f"===UPDATING PRODUCTS COLLECTION: {get_product_name(product_id)}===")
    
    product_doc = dev_db.collection('products').document(product_id).get()
    product_data = product_doc.to_dict()
    palettes_list = product_data.get('palettes', [])
    print(f"palettes list before update: {palettes_list}")
    
    palette_found = False
    for palette in palettes_list:
        if palette['palette_id'] == palette_id:
            palette_found = True
            if unit in palette['qty_list']:
                if activity_type == 'Inbound':
                    palette['qty_list'][unit] += qty
                elif activity_type == 'Outbound':
                    palette['qty_list'][unit] = max(0, palette['qty_list'][unit] - qty)
                    # if after subtracting qty the unit qty is 0, remove the unit from the qty_list
                    if palette['qty_list'][unit] == 0:
                        del palette['qty_list'][unit]
            else:
                if activity_type == 'Inbound':
                    palette['qty_list'][unit] = qty
                else:
                    print(f"Warning: Unit {unit} not found for palette {palette_id} in product {product_id}. Skipping...")
            break
    
    if not palette_found and activity_type == 'Inbound':
        palettes_list.append({
            "palette_id": palette_id,
            "palette_name": palette_name,
            "qty_list": {unit: qty}
        })
    elif not palette_found and activity_type == 'Outbound':
        print(f"Warning: Palette {palette_id} not found in product {product_id} for outbound activity. Skipping...")

    if activity_type == 'Inbound':
        dev_db.collection('products').document(product_id).update({f'{unit}': firestore.Increment(qty)})
    elif activity_type == 'Outbound':
        # if result is less than the qty in the activity, throw an error
        if dev_db.collection('products').document(product_id).get().to_dict()[unit] < qty:
            print(f"""Warning: Operation above qty in the database
Operation data:
Activities ID: {activity_id}
Decrement qty: {qty}
Unit: {unit}
Product name: {get_product_name(product_id)}

Database data:
Current qty: {dev_db.collection('products').document(product_id).get().to_dict()[unit]}
""")
        else:
            dev_db.collection('products').document(product_id).update({f'{unit}': firestore.Increment(-qty)})
    else:
        print('Activity type is not recognized')

    print(f"palettes list after update: {palettes_list}")
    dev_db.collection('products').document(product_id).update({'palettes': palettes_list})
    
# add activities and update products, warehouses, palettes
def add_activities():
    
    docs = firestore.Client.from_service_account_json("bugel_serviceaccount.json").collection('activities').order_by('timestamp', direction=firestore.Query.ASCENDING).stream()
    inbound_activities = []
    outbound_activities = []
    count = 0
    print(f"===SPLITTING ACTIVITIES BY ACTIVITY TYPE. Please wait...===")
    for doc in docs:
        count += 1
        doc_data = doc.to_dict()
        activity_id = doc.id
        activity_type = doc_data.get('type')
        unit = doc_data.get('unit').lower()
        qty = doc_data.get('qty')
        product_id = doc_data.get('product_id')
        product_name = get_product_name(product_id)
        palette_id = doc_data.get('palette_id')
        palette_name = get_palette_name(palette_id)
        whid = doc_data.get('wh_id')
        whname = doc_data.get('wh_name')
        if activity_type == 'Inbound':
            inbound_activities.append({
                'id': activity_id,
                'type': activity_type,
                'unit': unit,
                'qty': qty,
                'product_id': product_id,
                'product_name': product_name,
                'palette_id': palette_id,
                'palette_name': palette_name,
                'whid': whid,
                'whname': whname
            })
        elif activity_type == 'Outbound':
            outbound_activities.append({
                'id': activity_id,
                'type': activity_type,
                'unit': unit,
                'qty': qty,
                'product_id': product_id,
                'product_name': product_name,
                'palette_id': palette_id,
                'palette_name': palette_name,
                'whid': whid,
                'whname': whname
            })
        else:
            print('Activity type is not recognized')
    print(f"\n\n===SUM OF INBOUND ACTIVITIES: {len(inbound_activities)}===")
    print(f"===SUM OF OUTBOUND ACTIVITIES: {len(outbound_activities)}===\n\n")
    print(f"===INBOUND ACTIVITIES PROCESSING===")
    for activity in inbound_activities:
        update_palettes_collection(activity_type=activity['type'], palette_id=activity['palette_id'], product_id=activity['product_id'], product_name=activity['product_name'], unit=activity['unit'], qty=activity['qty'], whid=activity['whid'], whname=activity['whname'], activity_id=activity['id'])
        update_products_collection(activity_type=activity['type'], product_id=activity['product_id'], unit=activity['unit'], qty=activity['qty'], palette_id=activity['palette_id'], palette_name=activity['palette_name'], activity_id=activity['id'])
    print(f"===OUTBOUND ACTIVITIES PROCESSING===")
    for activity in outbound_activities:
        update_palettes_collection(activity_type=activity['type'], palette_id=activity['palette_id'], product_id=activity['product_id'], product_name=activity['product_name'], unit=activity['unit'], qty=activity['qty'], whid=activity['whid'], whname=activity['whname'], activity_id=activity['id'])
        update_products_collection(activity_type=activity['type'], product_id=activity['product_id'], unit=activity['unit'], qty=activity['qty'], palette_id=activity['palette_id'], palette_name=activity['palette_name'], activity_id=activity['id'])

def check_activities_by_id(activity_id: str = 'qqth05LH9H8lToPL90y6'):
    doc = prod_db.collection('activities').document(activity_id).get()
    data = doc.to_dict()
    print(data)

def convert_unit_to_lowercase(product_id: str, palette_id: str):
    prod_db = firestore.Client.from_service_account_json("bugel_serviceaccount.json")
    docs = prod_db.collection('activities').where('product_id', '==', product_id).where('palette_id', '==', palette_id).stream()
    for doc in docs:
        data = doc.to_dict()
        # scoure every doc and check if unit is in Camelcase
        if data.get('unit') != data.get('unit').lower():
            print(data.get('unit'))
            print(data)
            # update the unit to lowercase
            prod_db.collection('activities').document(doc.id).update({'unit': data.get('unit').lower()})
    

if __name__ == "__main__":
    if sys.argv[1] == 'test':
        test_activities()
    elif sys.argv[1] == 'reset-test':
        reset_product_palettes()
    elif sys.argv[1] == 'push':
        add_activities()
    elif sys.argv[1] == 'reset-all':
        reset_all_warehouses()
        reset_all_products()
        reset_all_palettes()
    elif sys.argv[1] == 'get-product-name':
        print(get_product_name(sys.argv[2]))