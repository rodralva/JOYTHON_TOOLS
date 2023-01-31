#!/bin/usr/env bash

#Script must be run from main folder or paths will be messed up

# runes de interes feb22_2: calib(1,2,3)    laser(9,10,11)  alpha(25,26,27)
# runes de interes feb22:   calib(1,2,3)    laser(45,46,47) alpha(12,13,14)
# runes de interes jan22:   calib(1,2,3)    laser(55,56,57) alpha(12,13,14)
# runes de interes dic21:   calib(18,19,20) laser(48,49,50) alpha(62,63,64)

# Write all runs inside the scp command to avoid inserting password more than once
scp -r pcae182_outside:/pnfs/ciemat.es/data/neutrinos/Super-cells_LAr/Feb22_2/ROOT/run{"01","02","03","09","10","11","25","26","27"}_ch* ../data/raw/.