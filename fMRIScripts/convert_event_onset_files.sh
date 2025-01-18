#!/bin/bash


#Check whether the file subjList.txt exists; if not, create it
if [ ! -f subjList.txt ]; then
	ls | grep ^sub- > subjList.txt
fi

#Loop over all subjects and format timing files into FSL format
for subj in `cat subjList.txt`; do
	cd $subj/ses-1/func
	cat ${subj}_ses-1_task-war_run-1_events.tsv | awk '{if ($2==31 || $2==32 || $2==33 || $2==34) {print $1 - 10, $4, 1}}' > negative_image_run1.txt
    cat ${subj}_ses-1_task-war_run-1_events.tsv | awk '{if ($2=="71" || $2=="72" || $2=="73" || $2=="74") {print $1 - 10, $4, 1}}' > positive_image_run1.txt
    cat ${subj}_ses-1_task-war_run-1_events.tsv | awk '{if ($2=="51" || $2=="52" || $2=="53" || $2=="54") {print $1 - 10, $4, 1}}' > neutral_image_run1.txt
    cat ${subj}_ses-1_task-war_run-1_events.tsv | awk '{if ($2=="31") {print $1 - 10, 22, 1}}' > negative_block_run1.txt
    cat ${subj}_ses-1_task-war_run-1_events.tsv | awk '{if ($2=="71") {print $1 - 10, 22, 1}}' > positive_block_run1.txt
    cat ${subj}_ses-1_task-war_run-1_events.tsv | awk '{if ($2=="51") {print $1 - 10, 22, 1}}' > neutral_block_run1.txt
    cat ${subj}_ses-1_task-war_run-1_events.tsv | awk '{if ($2=="22" || $2=="24") {print $1 - 10, $4, 1}}' > rest_run1.txt

    cat ${subj}_ses-1_task-war_run-2_events.tsv | awk '{if ($2=="31" || $2=="32" || $2=="33" || $2=="34") {print $1 - 10, $4, 1}}' > negative_image_run2.txt
    cat ${subj}_ses-1_task-war_run-2_events.tsv | awk '{if ($2=="71" || $2=="72" || $2=="73" || $2=="74") {print $1 - 10, $4, 1}}' > positive_image_run2.txt
    cat ${subj}_ses-1_task-war_run-2_events.tsv | awk '{if ($2=="51" || $2=="52" || $2=="53" || $2=="54") {print $1 - 10, $4, 1}}' > neutral_image_run2.txt
    cat ${subj}_ses-1_task-war_run-2_events.tsv | awk '{if ($2=="31") {print $1 - 10, 22, 1}}' > negative_block_run2.txt
    cat ${subj}_ses-1_task-war_run-2_events.tsv | awk '{if ($2=="71") {print $1 - 10, 22, 1}}' > positive_block_run2.txt
    cat ${subj}_ses-1_task-war_run-2_events.tsv | awk '{if ($2=="51") {print $1 - 10, 22, 1}}' > neutral_block_run2.txt
    cat ${subj}_ses-1_task-war_run-2_events.tsv | awk '{if ($2=="22" || $2=="24") {print $1 - 10, $4, 1}}' > rest_run2.txt

#Now convert to AFNI format
	timing_tool.py -fsl_timing_files negative_image*.txt -write_timing negative_image.1D
    timing_tool.py -fsl_timing_files positive_image*.txt -write_timing positive_image.1D
    timing_tool.py -fsl_timing_files neutral_image*.txt -write_timing neutral_image.1D
    timing_tool.py -fsl_timing_files negative_block*.txt -write_timing negative_block.1D
    timing_tool.py -fsl_timing_files positive_block*.txt -write_timing positive_block.1D
    timing_tool.py -fsl_timing_files neutral_block*.txt -write_timing neutral_block.1D
    timing_tool.py -fsl_timing_files rest*.txt -write_timing rest.1D

	cd ../../..

done
