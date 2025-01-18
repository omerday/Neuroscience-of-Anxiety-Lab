#!/bin/bash

#Indicate the session that needs to be analysed
session=1
compute_sswarper=true

if ["$#" -e 0]; then
    echo "No subjects provided"
    exit 1
fi

for subj in "$@"; do
    echo "Preparing timing files for subject ${subj}"
    echo ${subj} > subjList.txt
    sh convert_event_onset_files.sh

    if [ $compute_sswarper = true ]; then
    echo "Running SSWarper on ${subj}"
    sswarper2 -input ${subj}/ses-${session}/anat/${subj}_ses-${session}_T1w.nii.gz -base MNI152_2009_template_SSW.nii.gz -subid ${subj} -odir ${subj}/ses-${session}/anat_warped -giant_move
    fi

    echo "Moving previous outputs for subject"
    time=`date +"%H"`.`date +%M`
    mv ${subj}.results ${subj}.results.old.${time}
    mv proc.${subj} ${subj}.results.old.${time}/proc.${subj}
    mv output.proc.${subj} ${subj}.results.old.${time}/output.proc.${subj}

    echo "Running afni_proc.py for subject ${subj}"
    afni_proc.py \
        -subj_id ${subj} \
        -dsets_me_run \
            ${subj}/ses-${session}/func/${subj}_ses-${session}_task-war_run-1_echo-1_bold.nii.gz \
            ${subj}/ses-${session}/func/${subj}_ses-${session}_task-war_run-1_echo-2_bold.nii.gz \
            ${subj}/ses-${session}/func/${subj}_ses-${session}_task-war_run-1_echo-3_bold.nii.gz \
        -echo_times 13.6 25.96 38.3 \
        -dsets_me_run \
            ${subj}/ses-${session}/func/${subj}_ses-${session}_task-war_run-2_echo-1_bold.nii.gz \
            ${subj}/ses-${session}/func/${subj}_ses-${session}_task-war_run-2_echo-2_bold.nii.gz \
            ${subj}/ses-${session}/func/${subj}_ses-${session}_task-war_run-2_echo-3_bold.nii.gz \
        -echo_times 13.6 25.96 38.3 \
        -copy_anat \
            ${subj}/ses-${session}/anat/${subj}_ses-${session}_T1w.nii.gz \
        -blocks \
            tshift align tlrc volreg mask blur scale combine regress \
        -mask_epi_anat yes \
        -mask_apply anat \
        -tcat_remove_first_trs 5 \
        -html_review_style pythonic \
        -align_unifize_epi local \
        -align_opts_aea \
            -cost lpc+ZZ \
            -giant_move \
            -check_flip \
        -volreg_align_to MIN_OUTLIER \
        -volreg_align_e2a \
        -volreg_tlrc_warp \
        -mask_epi_anat yes \
        -volreg_compute_tsnr yes \
        -tlrc_base MNI152_2009_template.nii.gz \
        -tlrc_NL_warp \
        -tlrc_NL_warped_dsets \
            ${subj}/ses-${session}/anat_warped/anatQQ.${subj}.nii \
            ${subj}/ses-${session}/anat_warped/anatQQ.${subj}.aff12.1D \
            ${subj}/ses-${session}/anat_warped/anatQQ.${subj}_WARP.nii \
        -regress_stim_times       \
            ${subj}/ses-${session}/func/negative_block.1D \
            ${subj}/ses-${session}/func/positive_block.1D \
            ${subj}/ses-${session}/func/neutral_block.1D \
            ${subj}/ses-${session}/func/rest.1D \
        -regress_stim_labels      neg_blck pos_blck neut_blck rest   \
        -regress_basis            'BLOCK(20,1)' \
        -regress_opts_3dD \
            -jobs 8 \
            -gltsym 'SYM: neg_blck -neut_blck' \
            -glt_label 1 neg-neut-blck \
            -gltsym 'SYM: neg_blck -rest' \
            -glt_label 2 neg_blck-rest \
            -gltsym 'SYM: pos_blck -neut_blck' \
            -glt_label 3 pos-neut-blck \
            -gltsym 'SYM: neg_blck -pos_blck' \
            -glt_label 4 neg-pos-blck \
        -regress_motion_per_run                                          \
        -regress_censor_motion    0.5                                    \
        -regress_censor_outliers  0.05                                   \
        -regress_reml_exec                                               \
        -regress_compute_fitts                                           \
        -regress_make_ideal_sum   sum_ideal.1D                           \
        -regress_est_blur_epits                                          \
        -regress_est_blur_errts                                          \
        -regress_run_clustsim     no                                     \
        -execute                                                          
    echo "Done running afni_proc.py for subject ${subj}"
done