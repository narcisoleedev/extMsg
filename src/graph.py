"""import json
import networkx as nx
import matplotlib.pyplot as plt

# Helper function to find starting block in a group
def find_starting_block(blocks):
    print("Finding starting block...")
    for block_id, block in blocks.items():
        block_name = block.get('data', {}).get('name', '').lower()
        print(f"Block ID: {block_id}, Name: {block_name}")
        # Look for a block with common start terms
        if any(keyword in block_name for keyword in ["boas_vindas", "pergunta_inicial", "home", "start"]):
            print(f"Found starting block: {block_id} (Name: {block_name})")
            return block_id
    # If no specific starting block found, return the first block in the group
    print("No specific starting block found, using first block in group.")
    return next(iter(blocks.keys()), None)

# Function to recursively add nodes and edges to the graph and jump to other groups if needed
def traverse_group(graph, groups, current_group, current_block_id, visited_blocks, visited_groups):
    if (current_group, current_block_id) in visited_blocks:
        return
    visited_blocks.add((current_group, current_block_id))
    
    blocks = groups[current_group]['blocks']['drawflow']
    current_block = blocks.get(str(current_block_id), {})
    block_name = current_block.get('data', {}).get('name', 'Unnamed Block')
    intent_type = current_block.get('data', {}).get('intentType', None)
    
    # Debugging output
    print(f"Traversing block: {block_name} (ID: {current_block_id}) in group: {current_group}")
    
    # Add the current block to the graph
    graph.add_node(f"{current_group}_{current_block_id}", label=f"{block_name} ({current_group})")
    
    # Traverse each output connection
    for output in current_block.get('outputs', {}).values():
        for connection in output.get('connections', []):
            next_block_id = connection['node']
            graph.add_edge(f"{current_group}_{current_block_id}", f"{current_group}_{next_block_id}")
            
            # Debugging output
            print(f"  Connecting to block ID: {next_block_id}")
            
            # If intentType == 7, jump to the next group
            if intent_type == 7:
                # Find the next group to jump to
                next_group = current_block.get('data', {}).get('groupId')
                if next_group and next_group not in visited_groups:
                    visited_groups.add(next_group)
                    start_block_id = find_starting_block(groups[next_group]['blocks']['drawflow'])
                    print(f"Jumping from {current_group} to {next_group} based on intentType == 7")
                    traverse_group(graph, groups, next_group, start_block_id, visited_blocks, visited_groups)
            else:
                # Normal traversal within the same group
                traverse_group(graph, groups, current_group, next_block_id, visited_blocks, visited_groups)

# Function to visualize the graph
def visualize_graph(graph):
    if len(graph.nodes) == 0:
        print("No nodes to visualize.")
        return
    
    pos = nx.spring_layout(graph)
    labels = nx.get_node_attributes(graph, 'label')
    nx.draw(graph, pos, with_labels=True, labels=labels, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold', edge_color='gray')
    plt.title(f"Graph")
    plt.show()

# Load the JSON data
with open("../data-json.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Start with the 'principal' group
start_group = 'principal'

# Check if the start group exists
if start_group in [group['groupName'] for group in data['groups']]:
    groups = {group['groupName']: group for group in data['groups']}
    
    # Debugging output to check group structure
    print(f"Group 'principal' structure: {groups[start_group]}")
    
    # Find the starting block in the 'principal' group
    start_block_id = find_starting_block(groups[start_group]['blocks']['drawflow'])
    
    # Create a new directed graph
    graph = nx.DiGraph()
    visited_blocks = set()
    visited_groups = {start_group}

    # Traverse and build the graph starting from 'principal' group
    traverse_group(graph, groups, start_group, start_block_id, visited_blocks, visited_groups)
    
    # Visualize the graph
    visualize_graph(graph)
else:
    print(f"'principal' group not found in the data")"""
