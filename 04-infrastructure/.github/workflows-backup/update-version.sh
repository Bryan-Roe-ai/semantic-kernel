#!/bin/bash

# Function to display error messages
error_exit() {
    echo "ERROR: $1"
    exit 1
}

# Parse arguments
POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--file)
            file="$2"
            shift 2
            ;;
        -p|--propsFile)
            propsFile="$2"
            shift 2
            ;;
        -b|--buildAndRevisionNumber)
            buildAndRevisionNumber="$2"
            shift 2
            ;;
        -*|--*)
            error_exit "Unknown option $1"
            ;;
        *)
            POSITIONAL_ARGS+=("$1")
            shift
            ;;
    esac
done

# Restore positional parameters
set -- "${POSITIONAL_ARGS[@]}"

# Validate inputs
[[ -z "$file" ]] && error_exit "Parameter file (-f|--file) not provided"
[[ ! -f "$file" ]] && error_exit "file ${file} not found"

grep -q "<IsPackable>false</IsPackable>" "$file" && {
    echo "Project is marked as NOT packable - skipping."
    exit 0
}

[[ -z "$propsFile" ]] && error_exit "Parameter propsFile (-p|--propsFile) not provided"
[[ ! -f "$propsFile" ]] && error_exit "propsFile ${propsFile} not found"

[[ -z "$buildAndRevisionNumber" ]] && error_exit "Parameter buildAndRevisionNumber (-b|--buildAndRevisionNumber) not provided"

# Extract version from propsFile
propsVersionString=$(grep -i "<Version>" "$propsFile")
regex="<Version>([0-9.]*)<\/Version>"
[[ $propsVersionString =~ $regex ]] || error_exit "Version tag not found in propsFile"

propsVersion=${BASH_REMATCH[1]}
[[ -z "$propsVersion" ]] && error_exit "Version tag not found in propsFile"
[[ ! "$propsVersion" =~ ^0.* ]] && error_exit "Version expected to start with 0. Actual: ${propsVersion}"

fullVersionString="${propsVersion}.${buildAndRevisionNumber}-preview"
[[ ! "$fullVersionString" =~ ^0.* ]] && error_exit "Version expected to start with 0. Actual: ${fullVersionString}"

# Display information
cat <<EOF
==== Project: ${file} ====
propsFile = ${propsFile}
buildAndRevisionNumber = ${buildAndRevisionNumber}
version prefix from propsFile = ${propsVersion}
full version string: ${fullVersionString}
EOF

# Update or add version tag in the project file
if grep -qi "<Version>" "$file"; then
    echo "Updating version tag..."
    sed -i "s/<Version>[0-9]*\.[0-9]*<\/Version>/<Version>$fullVersionString<\/Version>/g" "$file"
else
    echo "Project is packable - adding version tag..."
    sed -i "s/<\/Project>/<PropertyGroup><Version>$fullVersionString<\/Version><\/PropertyGroup><\/Project>/g" "$file"
fi

echo "DONE"
