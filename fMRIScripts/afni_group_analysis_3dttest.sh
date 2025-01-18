#!/bin/bash

sub_a_paths="-setA"
sub_b_paths=""
prefix="group_analysis_`date +"%H"`.`date +%M`"

if ["$#" -e 0]; then
    echo "No prefix provided, using default"
else
    prefix=$1
fi

#Check whether the file subA.txt exists; if not, create it
if [ ! -f subA.txt ]; then
	echo "subA.txt doesn't exist. Teminating."
    exit 1
fi

#Loop over subjects in the test group and add their stats to the path
for subj in `cat subA.txt`; do
    sub_a_paths ="${sub_a_paths} ~/Desktop/MDMA/InputAfni/${subj}.results/stats.${subj}+tlrc[neg-neut-blck_GLT#0_Coef]"
done

if [ ! -f subB.txt ]; then
    echo "subA.txt not found, Running single group analysis."
else
    sub_b_paths="-subB"
    #Loop over subjects in the control group
    for subj in `cat subB.txt`; do
    sub_b_paths ="${sub_b_paths} ~/Desktop/MDMA/Control/${subj}.results/stats.${subj}+tlrc[neg-neut-blck_GLT#0_Coef]"
fi

3dttest++ \
    -prefix prefix \
    ${sub_a_paths} \
    ${sub_b_paths}