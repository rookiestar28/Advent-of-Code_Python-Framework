from utils.solution_base import SolutionBase
from itertools import combinations
import networkx as nx

"""
https://en.wikipedia.org/wiki/Clique_(graph_theory)
"""


class Solution(SolutionBase):
    def part1(self, data):
        G = nx.Graph()
        for line in data:
            parts = line.split("-")
            G.add_edge(parts[0], parts[1])

        """
        count = 0
        for nodes in combinations(G.nodes(), 3):
            if G.has_edge(nodes[0], nodes[1]) and G.has_edge(nodes[1], nodes[2]) and G.has_edge(nodes[0], nodes[2]):
                if any(n[0] == "t" for n in nodes):
                    count += 1
        """

        cliques = [c for c in nx.find_cliques(G) if len(c) >= 3 and any(n[0] == "t" for n in c)]
        sets = set()
        for c in cliques:
            for nodes in combinations(c, 3):
                if any(n[0] == "t" for n in nodes):
                    sets.add(tuple(sorted(nodes)))
        count = len(sets)

        return count

    def part2(self, data):
        G = nx.Graph()
        for line in data:
            parts = line.split("-")
            G.add_edge(parts[0], parts[1])

        cliques = nx.find_cliques(G)
        LAN = sorted(sorted(cliques, key=len, reverse=True)[0])

        return ",".join(LAN)
