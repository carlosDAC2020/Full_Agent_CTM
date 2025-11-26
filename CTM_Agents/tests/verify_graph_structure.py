import os
import sys
import importlib
from langgraph.graph import StateGraph

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

def check_graph_structure(strategy):
    print(f"\n--- Testing Strategy: {strategy} ---")
    os.environ["CTM_EXECUTION_STRATEGY"] = strategy
    
    # Force reload of the module to pick up env var changes
    if 'agents.tech_surveillance.graph' in sys.modules:
        del sys.modules['agents.tech_surveillance.graph']
    
    from agents.tech_surveillance.graph import workflow
    
    # Compile to get the graph
    app = workflow.compile()
    
    # Inspect edges (this is a bit internal, but we can check the nodes and edges)
    # LangGraph 0.1+ exposes .get_graph()
    graph = app.get_graph()
    
    print("Nodes:", [node.id for node in graph.nodes.values()])
    
    # Check edges
    found_presentation = False
    edges = []
    for edge in graph.edges:
        edges.append(f"{edge.source} -> {edge.target}")
        if edge.target == "presentation_generator":
            found_presentation = True
            print(f"✅ Found edge to presentation: {edge.source} -> {edge.target}")
        if edge.source == "presentation_generator":
            print(f"✅ Found edge from presentation: {edge.source} -> {edge.target}")

    if not found_presentation:
        print("❌ Presentation node not connected!")
    
    # Specific checks
    if strategy == "PARALLEL":
        if "images_generator -> presentation_generator" in edges and "presentation_generator -> __end__" in edges:
             print("✅ Parallel Logic Verified: images -> presentation -> END")
        else:
             print("❌ Parallel Logic Failed")
             
    else: # SEQUENTIAL
        if "images_generator -> presentation_generator" in edges and "presentation_generator -> report" in edges:
             print("✅ Sequential Logic Verified: images -> presentation -> report")
        else:
             print("❌ Sequential Logic Failed")

if __name__ == "__main__":
    check_graph_structure("SEQUENTIAL")
    check_graph_structure("PARALLEL")
