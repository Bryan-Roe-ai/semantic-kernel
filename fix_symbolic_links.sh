#!/bin/bash
# filepath: /home/broe/semantic-kernel/fix_symbolic_links.sh

set -euo pipefail

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Repository root
readonly REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
cd "$REPO_ROOT"

log() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $*"
}

success() {
    echo -e "${GREEN}✅${NC} $*"
}

warning() {
    echo -e "${YELLOW}⚠️${NC} $*"
}

error() {
    echo -e "${RED}❌${NC} $*"
}

remove_broken_symlinks() {
    log "Removing broken symbolic links..."
    local removed=0
    while IFS= read -r -d '' link; do
        if [[ ! -e "$link" ]]; then
            rm -f "$link"
            warning "Removed broken symlink: $(basename "$link")"
            ((removed++))
        fi
    done < <(find "$REPO_ROOT" -maxdepth 1 -type l -print0)
    log "Removed $removed broken symlinks"
}

create_essential_symlinks() {
    log "Creating essential symbolic links..."
    declare -A essential_links=(
        [dotnet]="01-core-implementations/dotnet"
        [python]="01-core-implementations/python"
        [java]="01-core-implementations/java"
        [typescript]="01-core-implementations/typescript"
        [samples]="01-core-implementations/samples"
        [tests]="01-core-implementations/tests"
        [plugins]="01-core-implementations/plugins"
        [ai-workspace]="02-ai-workspace"
        [notebooks]="02-ai-workspace/01-notebooks"
        [scripts]="04-infrastructure/scripts"
        [.github]="04-infrastructure/.github"
        [docs]="05-documentation"
        [data]="07-resources/data"
        [config]="04-infrastructure/config"
    )
    local created=0
    local updated=0
    for link in "${!essential_links[@]}"; do
        local target="${essential_links[$link]}"
        if [[ ! -e "$REPO_ROOT/$target" ]]; then
            warning "Target does not exist: $target"
            continue
        fi
        if [[ -L "$link" ]]; then rm -f "$link" && ((updated++));
        elif [[ -e "$link" ]]; then warning "Skipping existing non-symlink: $link" && continue; fi
        ln -s "$target" "$link"
        success "Created symlink: $link -> $target"
        ((created++))
    done
    log "Created/updated $((created+updated)) essential symlinks"
}

remove_unnecessary_symlinks() {
    log "Removing unnecessary symbolic links..."
    local removed=0
    for pattern in "*~*" "*-temp" "temp-*" "*-backup" "duplicate-*" "*-old"; do
        while IFS= read -r -d '' link; do
            rm -f "$link"
            warning "Removed: $(basename "$link")"
            ((removed++))
        done < <(find "$REPO_ROOT" -maxdepth 1 -name "$pattern" -type l -print0)
    done
    log "Removed $removed unnecessary symlinks"
}

organize_remaining_symlinks() {
    log "Organizing remaining symbolic links..."
    local dir="$REPO_ROOT/19-miscellaneous/symlinks"
    mkdir -p "$dir"
    local essential=(dotnet python java typescript samples tests plugins ai-workspace notebooks scripts .github docs data config)
    local moved=0
    while IFS= read -r -d '' link; do
        name=$(basename "$link")
        if [[ ! " ${essential[*]} " =~ " $name " ]]; then
            mv "$link" "$dir/"
            success "Moved symlink: $name"
            ((moved++))
        fi
    done < <(find "$REPO_ROOT" -maxdepth 1 -type l -print0)
    log "Moved $moved non-essential symlinks"
}

organize_root_files() {
    log "Organizing remaining root files..."
    # Move non-essential regular files (not directories or symlinks) from root into a subfolder
    local dir="$REPO_ROOT/19-miscellaneous/root_files"
    mkdir -p "$dir"
    local moved=0
    while IFS= read -r -d '' file; do
        name=$(basename "$file")
        # Skip hidden files and this script itself
        if [[ "$name" == ".*" ]] || [[ "$name" == "fix_symbolic_links.sh" ]]; then
            continue
        fi
        mv "$file" "$dir/" && success "Moved file: $name" && ((moved++))
    done < <(find "$REPO_ROOT" -maxdepth 1 -type f -print0)
    log "Moved $moved non-essential files"
}

verify_symlinks() {
    log "Verifying symlinks..."
    local broken=0 total=0
    while IFS= read -r -d '' link; do
        ((total++))
        [[ ! -e "$link" ]] && error "Broken: $(basename "$link")" && ((broken++))
    done < <(find "$REPO_ROOT" -type l -print0)
    if (( broken==0 )); then success "All $total symlinks OK"; else error "$broken broken out of $total" && return 1; fi
}

enforce_root_limit() {
    log "Ensuring root has no more than 12 items..."
    local entries=()
    while IFS= read -r -d '' entry; do
        entries+=("$entry")
    done < <(find "$REPO_ROOT" -maxdepth 1 -mindepth 1 -print0 | sort -z)
    local total=${#entries[@]}
    if (( total <= 12 )); then
        success "Root contains $total items, within limit"
        return
    fi
    local dir="$REPO_ROOT/19-miscellaneous/excess_root"
    mkdir -p "$dir"
    for ((i=12; i<total; i++)); do
        local entry="${entries[$i]}"
        local name="$(basename "$entry")"
        mv "$entry" "$dir/" && success "Moved excess item: $name"
    done
    log "Root reduced to 12 items"
}

main() {
    log "Starting symlink cleanup..."
    mkdir -p ".symlink_backup_$(date +%Y%m%d_%H%M%S)"
    remove_broken_symlinks
    remove_unnecessary_symlinks
    organize_remaining_symlinks
    organize_root_files
    create_essential_symlinks
    enforce_root_limit
    verify_symlinks && log "Cleanup complete!"
}

main "$@"


