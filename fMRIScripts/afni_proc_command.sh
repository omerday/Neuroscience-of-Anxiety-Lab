afni_proc.py \
    -subj_id sub-21 \
    -dsets_me_run \
        sub-21/ses-1/func/sub-21_ses-1_task-war_run-1_echo-1_bold.nii.gz \
        sub-21/ses-1/func/sub-21_ses-1_task-war_run-1_echo-2_bold.nii.gz \
        sub-21/ses-1/func/sub-21_ses-1_task-war_run-1_echo-3_bold.nii.gz \
    -echo_times 13.6 25.96 38.3 \
    -dsets_me_run \
        sub-21/ses-1/func/sub-21_ses-1_task-war_run-2_echo-1_bold.nii.gz \
        sub-21/ses-1/func/sub-21_ses-1_task-war_run-2_echo-2_bold.nii.gz \
        sub-21/ses-1/func/sub-21_ses-1_task-war_run-2_echo-3_bold.nii.gz \
    -echo_times 13.6 25.96 38.3 \
    -copy_anat \
        sub-21/ses-1/anat/sub-21_ses-1_T1w.nii.gz \
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
        sub-21/ses-1/anat_warped/anatQQ.sub-21.nii \
        sub-21/ses-1/anat_warped/anatQQ.sub-21.aff12.1D \
        sub-21/ses-1/anat_warped/anatQQ.sub-21_WARP.nii \
    -regress_stim_times       \
        sub-21/ses-1/func/negative_block.1D \
        sub-21/ses-1/func/positive_block.1D \
        sub-21/ses-1/func/neutral_block.1D \
        sub-21/ses-1/func/rest.1D \
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