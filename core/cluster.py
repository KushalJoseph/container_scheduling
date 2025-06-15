from typing import List, Dict
from core.node import Node

class Cluster:
    def __init__(self, cluster_config: Dict, verbose: bool=False):
        self.nodes: List[Node] = []
        for node_cnt in range(cluster_config["num_nodes"]):
            node = Node(
                id=f"n-{node_cnt}", 
                cpu_capacity=cluster_config["node_cpu"], 
                gpu_capacity=cluster_config["node_gpu"]
            )
            self.nodes.append(node)

    def get_all_nodes(self) -> List[Node]:
        return self.nodes

    def release_resources(self, current_time: float):
        """Call release on all nodes to free up completed tasks."""
        for node in self.nodes:
            node.release_completed_tasks(current_time)

    def get_node_by_id(self, node_id: str) -> Node:
        for node in self.nodes:
            if node.id == node_id:
                return node
        raise ValueError(f"Node with id '{node_id}' not found")

    def report(self, verbose: bool):
        for node in self.nodes:
            if verbose:
                print(node)