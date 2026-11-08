# Elastic cantilever: tip deflection must match P L^3 / (3 E I).
set L 100.0; set E 29000.0; set A 10.0; set I 100.0; set P 5.0
set expected [expr {-$P * pow($L, 3) / (3.0 * $E * $I)}]

wipe
model basic -ndm 2 -ndf 3
node 1 0.0 0.0
node 2 $L 0.0
fix 1 1 1 1
geomTransf Linear 1
element elasticBeamColumn 1 1 2 $A $E $I 1

timeSeries Linear 1
pattern Plain 1 1 {
    load 2 0.0 [expr {-$P}] 0.0
}

system BandGeneral
numberer RCM
constraints Plain
integrator LoadControl 1.0
algorithm Linear
analysis Static

if {[analyze 1] != 0} {
    puts "analysis failed"
    exit 1
}

set disp [nodeDisp 2 2]
puts "tip displacement = $disp, expected = $expected"
if {abs($disp - $expected) > 1e-8 * abs($expected)} {
    puts "mismatch"
    exit 1
}
puts "OK"
exit 0
