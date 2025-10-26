#!/bin/bash

# This script copies all assets from the original 'img' and 'sounds' directories
# into the Android project's 'res' directory, renaming them to be compliant
# with Android resource naming conventions.

set -e

DEST_DRAWABLE="app/src/main/res/drawable"
DEST_RAW="app/src/main/res/raw"

# Ensure destination directories exist
mkdir -p "$DEST_DRAWABLE"
mkdir -p "$DEST_RAW"

# Function to sanitize and copy files
# Arg1: Base directory to search in
# Arg2: Destination directory for copied files
# Arg3: A prefix to be added to the new filename to ensure uniqueness
copy_and_sanitize() {
    local base_dir="$1"
    local dest_dir="$2"
    local prefix="$3"

    find "$base_dir" -type f -print0 | while IFS= read -r -d $'\0' filepath; do
        filename=$(basename -- "$filepath")
        extension=".${filename##*.}"
        filename_no_ext="${filename%.*}"

        # Sanitize the name: lowercase, replace invalid chars with underscores
        sanitized_filename=$(echo "${prefix}_${filename_no_ext}" | tr '[:upper:]' '[:lower:]' | tr ' -' '_' | tr -s '_')
        new_name="${sanitized_filename}${extension}"

        echo "Copying $filepath -> $dest_dir/$new_name"
        cp "$filepath" "$dest_dir/$new_name"
    done
}

# Process all asset directories
copy_and_sanitize "img/doors1" "$DEST_DRAWABLE" "d1"
copy_and_sanitize "img/doors2" "$DEST_DRAWABLE" "d2"
copy_and_sanitize "img/InstructionsEnglish" "$DEST_DRAWABLE" "inst_en"
copy_and_sanitize "img/InstructionsHebrew" "$DEST_DRAWABLE" "inst_he"
copy_and_sanitize "img/outcomes" "$DEST_DRAWABLE" "outcome"
copy_and_sanitize "img/versionSpecificInstructions" "$DEST_DRAWABLE" "inst_specific"

copy_and_sanitize "img/Wheels" "$DEST_RAW" "vid_wheel"
copy_and_sanitize "sounds" "$DEST_RAW" "sound"

# Copy remaining top-level files from 'img' directory
find img -maxdepth 1 -type f -print0 | while IFS= read -r -d $'\0' filepath; do
    filename=$(basename -- "$filepath")
    extension=".${filename##*.}"
    filename_no_ext="${filename%.*}"
    sanitized_filename=$(echo "$filename_no_ext" | tr '[:upper:]' '[:lower:]' | tr ' -' '_' | tr -s '_')
    new_name="${sanitized_filename}${extension}"

    if [[ ".mp4" == "$extension" ]]; then
        echo "Copying $filepath -> $DEST_RAW/$new_name"
        cp "$filepath" "$DEST_RAW/$new_name"
    else
        echo "Copying $filepath -> $DEST_DRAWABLE/$new_name"
        cp "$filepath" "$DEST_DRAWABLE/$new_name"
    fi
done

echo "
Asset copying complete."