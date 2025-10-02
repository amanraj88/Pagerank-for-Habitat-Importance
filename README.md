Ranking Habitat Importance Using PageRank
This project provides a Python-based implementation for ranking the ecological importance of habitat patches using the PageRank algorithm. It adapts a famous algorithm from computer science to solve a real-world conservation problem: prioritizing which habitats to protect based on their role in maintaining ecosystem connectivity.

Problem Overview
In fragmented landscapes, not all habitat patches are created equal. Some act as critical "stepping stones" or "hubs" that are essential for wildlife movement and genetic diversity. This project models such a landscape as a network and uses PageRank to identify these keystone habitats.

The core idea is to treat:

Habitats as nodes in a graph.

Ecological corridors as weighted, directed edges.

A habitat's importance score increases if it is connected to other important habitats, allowing us to capture both direct and indirect influence within the ecosystem.

Features
Weighted Graph Construction: Builds a network where connections are weighted by distance and habitat quality.

PageRank Calculation: Applies a weighted PageRank algorithm to rank each habitat.

Data-Driven: Uses a simple CSV file for habitat data (coordinates, quality).

Visualization: Generates a network map where a habitat's size is proportional to its importance score.

Scenario-Ready: The code is structured to easily test "what-if" scenarios (e.g., adding a barrier or restoring a corridor)
