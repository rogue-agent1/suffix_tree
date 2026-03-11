#!/usr/bin/env python3
"""Suffix Tree — Ukkonen's algorithm (simplified) for string matching."""
import sys

class SuffixTree:
    def __init__(self, text):
        self.text = text + '$'
        self.edges = {}  # (node, char) -> (child, start, end)
        self.nodes = 1; self._build()
    def _build(self):
        for i in range(len(self.text)):
            self._add_suffix(i)
    def _add_suffix(self, start):
        node = 0; pos = start
        while pos < len(self.text):
            c = self.text[pos]
            if (node, c) in self.edges:
                child, estart, eend = self.edges[(node, c)]
                j = estart
                while j < eend and pos < len(self.text) and self.text[j] == self.text[pos]:
                    j += 1; pos += 1
                if j == eend:
                    node = child; continue
                # Split edge
                mid = self.nodes; self.nodes += 1
                self.edges[(node, c)] = (mid, estart, j)
                self.edges[(mid, self.text[j])] = (child, j, eend)
                leaf = self.nodes; self.nodes += 1
                self.edges[(mid, self.text[pos])] = (leaf, pos, len(self.text))
                return
            else:
                leaf = self.nodes; self.nodes += 1
                self.edges[(node, c)] = (leaf, pos, len(self.text))
                return
    def search(self, pattern):
        node = 0
        pos = 0
        while pos < len(pattern):
            c = pattern[pos]
            if (node, c) not in self.edges: return False
            child, start, end = self.edges[(node, c)]
            j = start
            while j < end and pos < len(pattern):
                if self.text[j] != pattern[pos]: return False
                j += 1; pos += 1
            if j == end: node = child
        return True
    def count_leaves(self, node=0):
        leaves = 0
        for c in set(self.text):
            if (node, c) in self.edges:
                child, _, _ = self.edges[(node, c)]
                sub = self.count_leaves(child)
                leaves += sub if sub > 0 else 1
        return leaves or 1

if __name__ == "__main__":
    st = SuffixTree("banana")
    print(f"Nodes: {st.nodes}")
    for p in ["ban", "ana", "nan", "xyz"]:
        print(f"  '{p}' found: {st.search(p)}")
