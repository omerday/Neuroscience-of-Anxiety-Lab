#!/bin/bash

sub_a_paths=""
sub_b_paths=""
# Variables for the neg-neut ttest
sub_a_neg_neut_argument="-setA BEFORE"
sub_b_neg_neut_argument="-setB AFTER"
# Variables for the pos-neut ttest
sub_a_pos_neut_argument="-setA BEFORE"
sub_b_pos_neut_argument="-setB AFTER"
# Variables for the neg-rest ttest
sub_a_neg_rest_argument="-setA BEFORE"
sub_b_neg_rest_argument="-setB AFTER"
prefix="group_analysis_`date +"%H"`.`date +%M`"

if [[ $# -eq 0 ]]; then
    echo "No prefix provided, using default"
else
    prefix=$1
fi

#Check whether the file subA.txt exists; if not, exit
if [ ! -f subA.txt ]; then
	echo "subA.txt doesn't exist. Teminating."
    exit 1
fi

#Loop over subjects in the test group and add their stats to the path
for subj in `cat subA.txt`; do
    sub_a_neg_neut_argument="${sub_a_neg_neut_argument} ${subj} ./${subj}.ses-1.results/stats.${subj}+tlrc[neg-neut-blck_GLT#0_Coef]"
    sub_a_pos_neut_argument="${sub_a_pos_neut_argument} ${subj} ./${subj}.ses-1.results/stats.${subj}+tlrc[pos-neut-blck_GLT#0_Coef]"
    sub_a_neg_rest_argument="${sub_a_pos_neut_argument} ${subj} ./${subj}.ses-1.results/stats.${subj}+tlrc[neg_blck-rest_GLT#0_Coef]"
    sub_a_paths="${sub_a_paths} ./${subj}.ses-1.results/mask_anat.${subj}+tlrc"
    sub_b_neg_neut_argument="-setB AFTER"
    sub_b_neg_neut_argument="${sub_b_neg_neut_argument} ${subj} ./${subj}.ses-2.results/stats.${subj}+tlrc[neg-neut-blck_GLT#0_Coef]"
    sub_b_pos_neut_argument="${sub_b_neg_neut_argument} ${subj} ./${subj}.ses-2.results/stats.${subj}+tlrc[pos-neut-blck_GLT#0_Coef]"
    sub_b_neg_rest_argument="${sub_b_neg_neut_argument} ${subj} ./${subj}.ses-2.results/stats.${subj}+tlrc[neg_blck-rest_GLT#0_Coef]"
    sub_b_paths="${sub_b_paths} ./${subj}.ses-2.results/mask_anat.${subj}+tlrc"
    done

3dmask_tool \
    -input \
        ${sub_a_paths} \
        ${sub_b_paths} \
    -prefix \
        ${prefix}_intersect \
    -frac 0.7

# Execute ttest for neg-neut
3dttest++ \
    ${sub_a_neg_neut_argument} \
    ${sub_b_neg_neut_argument} \
    -prefix ${prefix}_neg-neut \
    -mask ${prefix}_intersect+tlrc

# Execute ttest for pos-neut
3dttest++ \
    ${sub_a_pos_neut_argument} \
    ${sub_b_pos_neut_argument} \
    -prefix ${prefix}_pos-neut \
    -mask ${prefix}_intersect+tlrc

# Execute ttest for neg-rest
3dttest++ \
    ${sub_a_neg_rest_argument} \
    ${sub_b_neg_rest_argument} \
    -prefix ${prefix}_neg-rest \
    -mask ${prefix}_intersect+tlrc