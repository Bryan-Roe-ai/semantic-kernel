#!/usr/bin/env bash
# Copyright (c) .NET Foundation and contributors. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

# Stop script on NZEC
set -e
# Stop script if unbound variable found (use ${var:-} if intentional)
set -u
# By default cmd1 | cmd2 returns exit code of cmd2 regardless of cmd1 success
# This is causing it to fail
set -o pipefail

# Colors for terminal output
setup_colors() {
    if [ -t 1 ] && command -v tput > /dev/null; then
        ncolors=$(tput colors || echo 0)
        if [ -n "$ncolors" ] && [ $ncolors -ge 8 ]; then
            bold="$(tput bold || echo)"
            normal="$(tput sgr0 || echo)"
            black="$(tput setaf 0 || echo)"
            red="$(tput setaf 1 || echo)"
            green="$(tput setaf 2 || echo)"
            yellow="$(tput setaf 3 || echo)"
            blue="$(tput setaf 4 || echo)"
            magenta="$(tput setaf 5 || echo)"
            cyan="$(tput setaf 6 || echo)"
            white="$(tput setaf 7 || echo)"
        fi
    fi
}

# Logging functions
log_info() {
    printf "%b\n" "${cyan:-}dotnet-install:${normal:-} $1" >&3
}

log_warning() {
    printf "%b\n" "${yellow:-}dotnet_install: Warning: $1${normal:-}" >&3
}

log_error() {
    printf "%b\n" "${red:-}dotnet_install: Error: $1${normal:-}" >&2
}

# Check for required commands
check_min_reqs() {
    if ! command -v curl > /dev/null && ! command -v wget > /dev/null; then
        log_error "curl (recommended) or wget are required to download dotnet. Install missing prerequisite to proceed."
        exit 1
    fi
}

# Get the current OS name
get_current_os_name() {
    local uname
    uname=$(uname)
    case "$uname" in
        Darwin) echo "osx" ;;
        FreeBSD) echo "freebsd" ;;
        Linux)
            if is_musl_based_distro; then
                echo "linux-musl"
            else
                echo "linux"
            fi
            ;;
        *) log_error "OS name could not be detected: UName = $uname" ;;
    esac
}

# Check if the system is musl-based
is_musl_based_distro() {
    (ldd --version 2>&1 || true) | grep -q musl
}

# Main installation function
install_dotnet() {
    # Your installation logic here
    :
}

# Main script execution
main() {
    setup_colors
    check_min_reqs

    # Parse arguments and set variables

    install_dotnet

    log_info "Installation finished successfully."
}

main "$@"
