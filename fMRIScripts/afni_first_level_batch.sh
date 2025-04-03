#!/bin/bash

OPTIND=1
#Indicate the session that needs to be analysed
session=1
num_procs=1
compute_sswarper=false
num_jobs=0

while getopts "hs:wn:" opt; do
    case "$opt" in
    h)
        echo "Usage: $0 [-s session] [-w] [-n nprocs] sub-??*"
        exit 1
        ;;
    w)
        compute_sswarper=true
        echo "++Set to compute SSWarper"
        ;;
    s)
        session=$OPTARG
        echo "++Session mentioned is $session"
        ;;
    n)
        num_procs=$OPTARG
        echo "++Running $num_procs processes in parallel"
    esac
done

shift $((OPTIND - 1))

if [ "$#" -eq 0 ]; then
    echo "No subjects provided"
    exit 1
fi

task() {
    echo "Started running for ${subj} with PID $PID"
    echo "Preparing timing files for subject "$1""
    echo "$1" > subjList.txt
    sh convert_event_onset_files.sh -s ${session}

    if [ $compute_sswarper = true ]; then
    echo "Running SSWarper on "$1""
    @SSwarper -input "$1"/ses-${session}/anat/"$1"_ses-${session}_T1w.nii.gz \
            -base MNI152_2009_template_SSW.nii.gz \
            -subid "$1" -odir "$1"/ses-${session}/anat_warped \
            -giant_move \
            -cost_nl_final lpa \
            -minp 8
    fi

    echo "Moving previous outputs for subject"
    time=`date +"%H"`.`date +%M`
    old_results_path="$1".ses-"$session".results
    if [ -f old_results_path ]; then
        if [ -f proc."$1" ]; then
        mv proc."$1" ${old_results_path}
        fi
        if [ -f output.proc."$1" ]; then
            mv output.proc."$1" ${old_results_path}
        fi
        mv ${old_results_path} old_results/${old_results_path}.old.${time}
    else
        if [ -f proc."$1" ]; then
            rm proc."$1"
        fi
        if [ -f output.proc."$1" ]; then
            rm output.proc."$1"
        fi
    fi

    echo "Running afni_proc.py for subject "$1""
    afni_proc.py \
        -subj_id "$1" \
        -dsets_me_run \
            "$1"/ses-${session}/func/"$1"_ses-${session}_task-war_run-1_echo-1_bold.nii.gz \
            "$1"/ses-${session}/func/"$1"_ses-${session}_task-war_run-1_echo-2_bold.nii.gz \
            "$1"/ses-${session}/func/"$1"_ses-${session}_task-war_run-1_echo-3_bold.nii.gz \
        -echo_times 13.6 25.96 38.3 \
        -dsets_me_run \
            "$1"/ses-${session}/func/"$1"_ses-${session}_task-war_run-2_echo-1_bold.nii.gz \
            "$1"/ses-${session}/func/"$1"_ses-${session}_task-war_run-2_echo-2_bold.nii.gz \
            "$1"/ses-${session}/func/"$1"_ses-${session}_task-war_run-2_echo-3_bold.nii.gz \
        -echo_times 13.6 25.96 38.3 \
        -copy_anat \
            "$1"/ses-${session}/anat/"$1"_ses-${session}_T1w.nii.gz \
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
        -mask_segment_anat yes \
        -volreg_compute_tsnr yes \
        -tlrc_base MNI152_2009_template.nii.gz \
        -tlrc_NL_warp \
        -tlrc_NL_warped_dsets \
            "$1"/ses-${session}/anat_warped/anatQQ."$1".nii \
            "$1"/ses-${session}/anat_warped/anatQQ."$1".aff12.1D \
            "$1"/ses-${session}/anat_warped/anatQQ."$1"_WARP.nii \
        -regress_stim_times       \
            "$1"/ses-${session}/func/negative_block.1D \
            "$1"/ses-${session}/func/positive_block.1D \
            "$1"/ses-${session}/func/neutral_block.1D \
            "$1"/ses-${session}/func/rest.1D \
        -regress_stim_labels      neg_blck pos_blck neut_blck rest   \
        #TODO: Try and use regress_stim_times
        -regress_basis            'BLOCK(22,1)' \
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
        #TODO: Multiply GM with the activity, and run clustsim on the result (Maybe post-script?)                                               
    echo "Done running afni_proc.py for subject "$1""
    echo "Moving results to sub-folder by session"
    mv "$1".results "$1".ses-"$session".results
    echo "Done"
}

if [ $num_procs -eq 1 ]; then
    for subj in "$@"; do
        task "$subj" > ${subj}.txt
    done
else
    for subj in "$@"; do
        while [ $num_jobs -ge $num_procs ]; do
            wait -n
        done
        num_jobs=$num_jobs+1
        task "$subj" > ${subj}.txt && num_jobs=$num_jobs-1 &
    done
fi

wait
echo "All processes finished successfully!"