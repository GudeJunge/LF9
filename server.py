from flask import Flask, request, jsonify, abort
import uuid

# initialize Flask server
app = Flask(__name__)

# create unique id for lists, entries
todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'
todo_1_id = str(uuid.uuid4())
todo_2_id = str(uuid.uuid4())
todo_3_id = str(uuid.uuid4())
todo_4_id = str(uuid.uuid4())

# define internal data structures with example data
todo_lists = {
    todo_list_1_id: {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    todo_list_2_id: {'id': todo_list_2_id, 'name': 'Arbeit'},
    todo_list_3_id: {'id': todo_list_3_id, 'name': 'Privat'},
}
todo_entries = {
    todo_1_id: {'id': todo_1_id, 'name': 'Milch', 'description': '', 'list_id': todo_list_1_id},
    todo_2_id: {'id': todo_2_id, 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list_id': todo_list_2_id},
    todo_3_id: {'id': todo_3_id, 'name': 'Kinokarten kaufen', 'description': '', 'list_id': todo_list_3_id},
    todo_4_id: {'id': todo_4_id, 'name': 'Eier', 'description': '', 'list_id': todo_list_1_id},
}

# add some headers to allow cross origin access to the API on this server, necessary for using preview in Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,PATCH'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/list', methods=['POST'])
def add_list():
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, description="Invalid parameters")
    
    list_id = str(uuid.uuid4())
    todo_lists[list_id] = {
        'id': list_id,
        'name': data['name']
    }
    return jsonify(todo_lists[list_id]), 201

@app.route('/lists', methods=['GET'])
def get_lists():
    return jsonify(list(todo_lists.values())), 200

@app.route('/list/<list_id>/item', methods=['POST'])
def post_new_todo(list_id):
    if list_id not in todo_lists:
        abort(404, description="Todo list not found")
    
    data = request.get_json()
    if not data or 'name' not in data or 'description' not in data:
        abort(400, description="Invalid parameters")
    
    item_id = str(uuid.uuid4())
    todo_entry = {
        'id': item_id,
        'name': data['name'],
        'description': data['description'],
        'list_id': list_id
    }
    todo_entries[item_id] = todo_entry
    return jsonify(todo_entry), 201

@app.route('/list/<list_id>', methods=['GET'])
def get_todo_list_items(list_id):
    if list_id not in todo_lists:
        abort(404, description="Todo list not found")
    
    items = [item for item in todo_entries.values() if item['list_id'] == list_id]
    return jsonify(items), 200

@app.route('/list/<list_id>', methods=['DELETE'])
def delete_list_by_id(list_id):
    if list_id not in todo_lists:
        abort(404, description="Todo list not found")
    
    del todo_lists[list_id]
    for item_id in list(todo_entries.keys()):
        if todo_entries[item_id]['list_id'] == list_id:
            del todo_entries[item_id]
    
    return '', 204

@app.route('/list/<list_id>/item/<item_id>', methods=['PATCH'])
def patch_todo_list_item(list_id, item_id):
    if item_id not in todo_entries or todo_entries[item_id]['list_id'] != list_id:
        abort(404, description="Todo item not found")
    
    data = request.get_json()
    if not data:
        abort(400, description="Invalid parameters")
    
    todo_entries[item_id].update(data)
    return jsonify(todo_entries[item_id]), 200

@app.route('/list/<list_id>/item/<item_id>', methods=['DELETE'])
def delete_todo_list_item(list_id, item_id):
    if item_id not in todo_entries or todo_entries[item_id]['list_id'] != list_id:
        abort(404, description="Todo item not found")
    
    del todo_entries[item_id]
    return '', 204

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
