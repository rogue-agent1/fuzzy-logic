#!/usr/bin/env python3
"""Fuzzy logic system with membership functions and inference."""
import sys

class TriMF:
    def __init__(self, a, b, c): self.a, self.b, self.c = a, b, c
    def __call__(self, x):
        if x <= self.a or x >= self.c: return 0.0
        if x <= self.b: return (x - self.a) / (self.b - self.a) if self.b != self.a else 1.0
        return (self.c - x) / (self.c - self.b) if self.c != self.b else 1.0

class TrapMF:
    def __init__(self, a, b, c, d): self.a, self.b, self.c, self.d = a, b, c, d
    def __call__(self, x):
        if x <= self.a or x >= self.d: return 0.0
        if self.a < x < self.b: return (x - self.a) / (self.b - self.a)
        if self.b <= x <= self.c: return 1.0
        return (self.d - x) / (self.d - self.c)

class FuzzyVar:
    def __init__(self, name, lo, hi):
        self.name, self.lo, self.hi, self.terms = name, lo, hi, {}
    def add_term(self, name, mf): self.terms[name] = mf
    def fuzzify(self, x): return {name: mf(x) for name, mf in self.terms.items()}

class FuzzyRule:
    def __init__(self, antecedents, consequent): self.ant, self.con = antecedents, consequent

def defuzzify_centroid(output_var, activations, n=100):
    step = (output_var.hi - output_var.lo) / n
    num = den = 0
    for i in range(n + 1):
        x = output_var.lo + i * step
        mu = max(min(output_var.terms[term](x), level) for term, level in activations.items() if level > 0) if any(v > 0 for v in activations.values()) else 0
        num += x * mu; den += mu
    return num / den if den > 0 else (output_var.lo + output_var.hi) / 2

def main():
    if len(sys.argv) < 2: print("Usage: fuzzy_logic.py <demo|test>"); return
    if sys.argv[1] == "test":
        tri = TriMF(0, 5, 10)
        assert tri(5) == 1.0; assert tri(0) == 0.0; assert tri(10) == 0.0
        assert abs(tri(2.5) - 0.5) < 0.01
        trap = TrapMF(0, 2, 8, 10)
        assert trap(5) == 1.0; assert trap(0) == 0.0; assert abs(trap(1) - 0.5) < 0.01
        temp = FuzzyVar("temp", 0, 40)
        temp.add_term("cold", TriMF(0, 0, 20))
        temp.add_term("warm", TriMF(10, 20, 30))
        temp.add_term("hot", TriMF(20, 40, 40))
        f = temp.fuzzify(15)
        assert f["cold"] > 0 and f["warm"] > 0 and f["hot"] == 0
        # Defuzzify
        out = FuzzyVar("speed", 0, 100)
        out.add_term("slow", TriMF(0, 0, 50))
        out.add_term("fast", TriMF(50, 100, 100))
        act = {"slow": 0.8, "fast": 0.2}
        result = defuzzify_centroid(out, act)
        assert 20 < result < 50  # should lean slow
        print("All tests passed!")
    else:
        temp = FuzzyVar("temp", 0, 40)
        temp.add_term("cold", TriMF(0, 0, 20)); temp.add_term("hot", TriMF(20, 40, 40))
        print(f"Fuzzify 25: {temp.fuzzify(25)}")

if __name__ == "__main__": main()
