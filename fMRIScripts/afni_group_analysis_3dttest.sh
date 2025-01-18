#!/bin/bash

sub_a_paths=""
sub_b_paths=""
sub_a_argument="-setA MDMA"
sub_b_argument=""
prefix="group_analysis_`date +"%H"`.`date +%M`"

if [[ $# -eq 0 ]]; then
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
    sub_a_argument="${sub_a_argument} ${subj} ./InputAfni/${subj}.results/stats.${subj}+tlrc[neg-neut-blck_GLT#0_Coef]"
    sub_a_paths="${sub_a_paths} ./InputAfni/${subj}.results/stats.${subj}+tlrc[neg-neut-blck_GLT#0_Coef]"
done

if [ ! -f subB.txt ]; then
    echo "subA.txt not found, Running single group analysis."
else
    sub_b_argument="-setB Control"
    #Loop over subjects in the control group
    for subj in `cat subB.txt`; do
    sub_b_argument="${sub_b_argument} ${subj} ./Control/${subj}.results/stats.${subj}+tlrc[neg-neut-blck_GLT#0_Coef]"
    sub_b_paths="${sub_b_paths} ./Control/${subj}.results/stats.${subj}+tlrc[neg-neut-blck_GLT#0_Coef]"
    done
fi

3dmask_tool \
    -input \
        ${sub_a_paths} \
        ${sub_b_paths} \
    -prefix \
        ${prefix}_intersect \
    -frac 0.7

3dttest++ \
    ${sub_a_argument} \
    ${sub_b_argument} \
    -prefix ${prefix} \
    -mask ${prefix}_intersect+tlrc