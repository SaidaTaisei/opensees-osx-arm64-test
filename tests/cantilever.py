"""Elastic cantilever: tip deflection must match P L^3 / (3 E I)."""
import sys

import opensees as ops

L, E, A, I, P = 100.0, 29000.0, 10.0, 100.0, 5.0
expected = -P * L**3 / (3.0 * E * I)

ops.wipe()
ops.model("basic", "-ndm", 2, "-ndf", 3)
ops.node(1, 0.0, 0.0)
ops.node(2, L, 0.0)
ops.fix(1, 1, 1, 1)
ops.geomTransf("Linear", 1)
ops.element("elasticBeamColumn", 1, 1, 2, A, E, I, 1)

ops.timeSeries("Linear", 1)
ops.pattern("Plain", 1, 1)
ops.load(2, 0.0, -P, 0.0)

ops.system("BandGeneral")
ops.numberer("RCM")
ops.constraints("Plain")
ops.integrator("LoadControl", 1.0)
ops.algorithm("Linear")
ops.analysis("Static")

if ops.analyze(1) != 0:
    sys.exit("analysis failed")

disp = ops.nodeDisp(2, 2)
print(f"tip displacement = {disp:.6e}, expected = {expected:.6e}")
if abs(disp - expected) > 1e-8 * abs(expected):
    sys.exit("mismatch")
print("OK")
