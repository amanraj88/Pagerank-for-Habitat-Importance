# --------------------------------------------------------------------------
# Ranking Habitat Importance Using PageRank
#
# This script models a landscape of fragmented habitats as a network and
# uses a weighted PageRank algorithm to rank the importance of each habitat
# patch for maintaining overall ecosystem connectivity.
#
# Author: [Aman Raj]
# Date: October 1, 2025
# --------------------------------------------------------------------------

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# --- 1. CONFIGURATION AND PARAMETERS ---

# Path to the data file containing habitat patch information
DATA_FILE = 'data/habitat_patches.csv'

# Species-specific parameter: average dispersal distance (in the same units as coordinates)
# A larger value means the species can travel farther, making the network more connected.
DISPERSAL_DISTANCE = 15.0

# PageRank algorithm's damping factor
DAMPING_FACTOR = 0.85

# A threshold to decide if a connection is too weak to be included in the graph
WEIGHT_THRESHOLD = 0.01


# --- 2. HELPER FUNCTION: CALCULATE EDGE WEIGHT ---

def calculate_edge_weight(patch1, patch2, dispersal_dist):
    """
    Calculates a connectivity weight between two habitat patches.

    The weight is a combination of the distance between patches (with exponential decay)
    and the quality of the two patches.

    Args:
        patch1 (Series): A pandas Series with 'x', 'y', and 'quality' for the source patch.
        patch2 (Series): A pandas Series with 'x', 'y', and 'quality' for the target patch.
        dispersal_dist (float): The species' average dispersal distance.

    Returns:
        float: The calculated connectivity weight (between 0 and 1).
    """
    # Calculate Euclidean distance between the two patches
    distance = np.sqrt((patch1['x'] - patch2['x'])**2 + (patch1['y'] - patch2['y'])**2)

    # Calculate the distance decay factor
    distance_factor = np.exp(-distance / dispersal_dist)

    # Calculate the habitat quality factor
    quality_factor = np.sqrt(patch1['quality'] * patch2['quality'])

    # The final weight is the product of the two factors
    return distance_factor * quality_factor


# --- 3. MAIN SCRIPT LOGIC ---

def main():
    """Main function to run the habitat ranking analysis."""
    
    # --- DATA LOADING ---
    print("Step 1: Loading habitat patch data...")
    try:
        patches_df = pd.read_csv(DATA_FILE)
        # Set the patch ID as the index for easy lookup
        patches_df.set_index('id', inplace=True)
        print(f"Loaded {len(patches_df)} habitat patches.")
    except FileNotFoundError:
        print(f"Error: Data file not found at '{DATA_FILE}'. Please check the path.")
        return

    # --- NETWORK CONSTRUCTION ---
    print("\nStep 2: Building the weighted habitat network...")
    G = nx.DiGraph()

    # Add nodes to the graph with their attributes (quality, coordinates)
    for patch_id, data in patches_df.iterrows():
        G.add_node(patch_id, quality=data['quality'], pos=(data['x'], data['y']))

    # Add weighted edges between all pairs of nodes
    for source_id, source_data in patches_df.iterrows():
        for target_id, target_data in patches_df.iterrows():
            if source_id != target_id:
                # Calculate the weight for the potential connection
                weight = calculate_edge_weight(source_data, target_data, DISPERSAL_DISTANCE)
                
                # Only add an edge if the connection is strong enough
                if weight > WEIGHT_THRESHOLD:
                    G.add_edge(source_id, target_id, weight=weight)
    
    print(f"Network built with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    # --- PAGERANK CALCULATION ---
    print("\nStep 3: Running the weighted PageRank algorithm...")
    # Use NetworkX's pagerank function, specifying the 'weight' attribute
    pagerank_scores = nx.pagerank(G, alpha=DAMPING_FACTOR, weight='weight')
    
    # Sort the results for a clean, ranked output
    sorted_ranks = sorted(pagerank_scores.items(), key=lambda item: item[1], reverse=True)

    # --- RESULTS DISPLAY ---
    print("\n--- Habitat Importance Ranking ---")
    for patch_id, score in sorted_ranks:
        print(f"  - Patch {patch_id}: \t Importance Score = {score:.4f}")

    # --- VISUALIZATION ---
    print("\nStep 4: Generating network visualization...")
    plt.figure(figsize=(12, 8))

    # Get positions from node attributes
    pos = nx.get_node_attributes(G, 'pos')
    
    # Node size is proportional to its PageRank score
    node_sizes = [5000 * score for score in pagerank_scores.values()]
    
    # Edge width is proportional to its weight
    edge_widths = [G[u][v]['weight'] * 5 for u, v in G.edges()]

    nx.draw(G, pos, 
            with_labels=True,
            node_color='skyblue',
            node_size=node_sizes,
            width=edge_widths,
            edge_color='gray',
            alpha=0.8,
            arrows=True)
            
    plt.title("Habitat Connectivity Network (Node size is proportional to PageRank score)")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    main()
