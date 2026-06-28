#!/usr/bin/env bash
# ============================================================
# setup-freecad-env.sh
# Chevrolet Duramax 3.0 LM2 / LZ0 — Oil Cooler CAD Scripts
# ============================================================
#
# Creates a Python virtual environment, installs supporting
# packages, and wires the venv to the system FreeCAD
# installation so that macros in this directory can be run
# from the command line without opening the FreeCAD GUI.
#
# What it does
# ------------
#  1. Locates Python 3.10+ on the system.
#  2. Creates a .venv in this directory.
#  3. Installs pip-available supporting packages (numpy, scipy).
#  4. Searches common macOS and Linux paths for a FreeCAD
#     installation; if found, injects its library directory into
#     the venv via a .pth file so that "import FreeCAD" works.
#  5. Generates a run-macro.sh convenience wrapper that chooses
#     the correct Python interpreter at run time.
#
# Preferred run method (no venv needed)
# --------------------------------------
#  If FreeCAD is installed as an app bundle or system package,
#  the cleanest way to run a macro is via FreeCAD's own Python:
#
#    /Applications/FreeCAD.app/Contents/MacOS/FreeCADCmd  \
#        oil-filter-thread-adapter.py
#
#  run-macro.sh (generated here) handles this automatically.
#
# Usage
# -----
#  chmod +x setup-freecad-env.sh
#  ./setup-freecad-env.sh
#
# Tested on
# ---------
#  macOS 14 (Sonoma) — FreeCAD 0.21 app bundle
#  Ubuntu 22.04      — FreeCAD via apt / AppImage
#
# Requirements
# ------------
#  Python 3.10+   (system or homebrew)
#  FreeCAD 0.21+  (see README.md for install links)
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"
RUN_WRAPPER="${SCRIPT_DIR}/run-macro.sh"

# ── Colour helpers ────────────────────────────────────────────────────────────
RED='\033[0;31m'
YEL='\033[0;33m'
GRN='\033[0;32m'
CYN='\033[0;36m'
BLD='\033[1m'
RST='\033[0m'

info()    { echo -e "${CYN}[setup]${RST} $*"; }
success() { echo -e "${GRN}[setup]${RST} $*"; }
warn()    { echo -e "${YEL}[setup]${RST} $*"; }
fatal()   { echo -e "${RED}[setup] ERROR:${RST} $*" >&2; exit 1; }

# ── Step 1 — Locate Python 3.10+ ─────────────────────────────────────────────
info "Locating Python 3.10+ ..."

PYTHON_BIN=""
for candidate in python3.13 python3.12 python3.11 python3.10 python3; do
    if command -v "${candidate}" &>/dev/null; then
        ver=$("${candidate}" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        major="${ver%%.*}"
        minor="${ver##*.}"
        if [[ "${major}" -ge 3 && "${minor}" -ge 10 ]]; then
            PYTHON_BIN="$(command -v "${candidate}")"
            break
        fi
    fi
done

[[ -z "${PYTHON_BIN}" ]] && fatal \
    "Python 3.10 or newer is required.\n" \
    "  macOS:  brew install python@3.12\n" \
    "  Linux:  sudo apt install python3.12"

PYTHON_VERSION=$("${PYTHON_BIN}" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
success "Found Python ${PYTHON_VERSION} at ${PYTHON_BIN}"

# ── Step 2 — Locate FreeCAD ───────────────────────────────────────────────────
info "Searching for FreeCAD installation ..."

FREECAD_CMD=""
FREECAD_LIB_DIR=""

# Candidate freecadcmd binaries
# Note: some bundles ship "FreeCAD" (no "Cmd" suffix) — check both.
FREECAD_CMD_CANDIDATES=(
    "/Applications/FreeCAD.app/Contents/MacOS/FreeCADCmd"
    "/Applications/FreeCAD.app/Contents/MacOS/FreeCAD"
    "/Applications/FreeCAD_0.21.app/Contents/MacOS/FreeCADCmd"
    "/Applications/FreeCAD_0.21.app/Contents/MacOS/FreeCAD"
    "${HOME}/Applications/FreeCAD.app/Contents/MacOS/FreeCADCmd"
    "${HOME}/Applications/FreeCAD.app/Contents/MacOS/FreeCAD"
    "/usr/bin/freecadcmd"
    "/usr/local/bin/freecadcmd"
    "/snap/bin/freecad"
)

for c in "${FREECAD_CMD_CANDIDATES[@]}"; do
    if [[ -x "${c}" ]]; then
        FREECAD_CMD="${c}"
        break
    fi
done

if command -v freecadcmd &>/dev/null && [[ -z "${FREECAD_CMD}" ]]; then
    FREECAD_CMD="$(command -v freecadcmd)"
fi

# Candidate library directories (for .pth injection)
# macOS bundles use Contents/Resources/lib or Contents/lib depending on version.
FREECAD_LIB_CANDIDATES=(
    "/Applications/FreeCAD.app/Contents/Resources/lib"
    "/Applications/FreeCAD.app/Contents/lib"
    "/Applications/FreeCAD_0.21.app/Contents/Resources/lib"
    "/Applications/FreeCAD_0.21.app/Contents/lib"
    "${HOME}/Applications/FreeCAD.app/Contents/Resources/lib"
    "${HOME}/Applications/FreeCAD.app/Contents/lib"
    "/usr/lib/freecad/lib"
    "/usr/lib/freecad-python3/lib"
    "/usr/local/lib/freecad/lib"
    "/usr/lib/x86_64-linux-gnu/freecad/lib"
)

for d in "${FREECAD_LIB_CANDIDATES[@]}"; do
    if [[ -d "${d}" ]]; then
        FREECAD_LIB_DIR="${d}"
        break
    fi
done

# Also search relative to the binary if no lib dir was found yet
if [[ -n "${FREECAD_CMD}" && -z "${FREECAD_LIB_DIR}" ]]; then
    bundle_root="$(dirname "$(dirname "${FREECAD_CMD}")")"   # e.g. Contents/
    for candidate_lib in \
        "${bundle_root}/Resources/lib" \
        "${bundle_root}/lib"
    do
        if [[ -d "${candidate_lib}" ]]; then
            FREECAD_LIB_DIR="${candidate_lib}"
            break
        fi
    done
fi

if [[ -n "${FREECAD_CMD}" ]]; then
    success "Found FreeCAD command: ${FREECAD_CMD}"
else
    warn "FreeCAD command not found."
    warn "  Macros cannot run headless until FreeCAD is installed."
    warn "  Download: https://www.freecad.org/downloads.php"
fi

if [[ -n "${FREECAD_LIB_DIR}" ]]; then
    success "Found FreeCAD lib dir: ${FREECAD_LIB_DIR}"
else
    warn "FreeCAD library directory not found — 'import FreeCAD' may fail in venv."
fi

# ── Step 3 — Create virtual environment ──────────────────────────────────────
if [[ -d "${VENV_DIR}" ]]; then
    warn "Existing venv found at .venv — removing and recreating."
    rm -rf "${VENV_DIR}"
fi

info "Creating virtual environment at .venv ..."
"${PYTHON_BIN}" -m venv "${VENV_DIR}"
success "Virtual environment created."

VENV_PYTHON="${VENV_DIR}/bin/python"
VENV_PIP="${VENV_DIR}/bin/pip"

# ── Step 4 — Upgrade pip and install packages ─────────────────────────────────
info "Upgrading pip ..."
"${VENV_PYTHON}" -m pip install --quiet --upgrade pip

info "Installing Python packages ..."

# Core scientific stack (pure Python / wheels — no FreeCAD dependency)
PACKAGES=(
    "numpy"                  # array math, used in thread/geometry calculations
    "scipy"                  # engineering calculations
    "matplotlib"             # optional: plot temperature matrices, clearance graphs
)

for pkg in "${PACKAGES[@]}"; do
    info "  Installing ${pkg} ..."
    "${VENV_PIP}" install --quiet "${pkg}"
done

success "Packages installed: ${PACKAGES[*]}"

# ── Step 5 — Inject FreeCAD library path into venv ───────────────────────────
if [[ -n "${FREECAD_LIB_DIR}" ]]; then
    info "Injecting FreeCAD library path into venv ..."

    PTH_DIR="${VENV_DIR}/lib/python${PYTHON_VERSION}/site-packages"
    PTH_FILE="${PTH_DIR}/freecad-bundle.pth"

    # Write the .pth file — Python adds every line to sys.path at startup
    {
        echo "# FreeCAD library path — auto-generated by setup-freecad-env.sh"
        echo "${FREECAD_LIB_DIR}"
    } > "${PTH_FILE}"

    # Also add the parent of lib (e.g. FreeCAD.app/Contents) if it exists
    FREECAD_PARENT="$(dirname "${FREECAD_LIB_DIR}")"
    if [[ -d "${FREECAD_PARENT}" ]]; then
        echo "${FREECAD_PARENT}" >> "${PTH_FILE}"
    fi

    # Verify import works
    if "${VENV_PYTHON}" -c "import FreeCAD" 2>/dev/null; then
        success "'import FreeCAD' works inside the venv."
    else
        warn "'import FreeCAD' still fails inside the venv."
        warn "This is common when FreeCAD uses a different Python ABI."
        warn "Use run-macro.sh (generated below) to run macros via FreeCADCmd."
    fi
fi

# ── Step 6 — Generate run-macro.sh wrapper ───────────────────────────────────
info "Generating ${RUN_WRAPPER} ..."

cat > "${RUN_WRAPPER}" << 'WRAPPER_EOF'
#!/usr/bin/env bash
# ============================================================
# run-macro.sh — auto-generated by setup-freecad-env.sh
# Run a FreeCAD Python macro from the command line.
#
# Usage:  ./run-macro.sh <script.py> [args...]
#
# Priority order:
#   1. FreeCADCmd  (FreeCAD's own Python — most compatible)
#   2. .venv/bin/python  (venv with FreeCAD path injected)
#   3. System python3  (fallback; FreeCAD modules likely missing)
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

[[ $# -eq 0 ]] && { echo "Usage: $0 <macro.py> [args...]"; exit 1; }

MACRO="${SCRIPT_DIR}/${1}"
[[ ! -f "${MACRO}" ]] && MACRO="${1}"  # allow absolute paths too
[[ ! -f "${MACRO}" ]] && { echo "Error: macro not found: ${1}"; exit 1; }

FREECAD_CMD_CANDIDATES=(
    "/Applications/FreeCAD.app/Contents/MacOS/FreeCADCmd"
    "/Applications/FreeCAD.app/Contents/MacOS/FreeCAD"
    "/Applications/FreeCAD_0.21.app/Contents/MacOS/FreeCADCmd"
    "/Applications/FreeCAD_0.21.app/Contents/MacOS/FreeCAD"
    "${HOME}/Applications/FreeCAD.app/Contents/MacOS/FreeCADCmd"
    "${HOME}/Applications/FreeCAD.app/Contents/MacOS/FreeCAD"
    "/usr/bin/freecadcmd"
    "/usr/local/bin/freecadcmd"
    "/snap/bin/freecad"
)

FREECAD_CMD=""
for c in "${FREECAD_CMD_CANDIDATES[@]}"; do
    [[ -x "${c}" ]] && FREECAD_CMD="${c}" && break
done
command -v freecadcmd &>/dev/null && FREECAD_CMD="${FREECAD_CMD:-$(command -v freecadcmd)}"

if [[ -n "${FREECAD_CMD}" ]]; then
    echo "[run] Using FreeCADCmd: ${FREECAD_CMD}"
    exec "${FREECAD_CMD}" "${MACRO}" "${@:2}"
elif [[ -x "${SCRIPT_DIR}/.venv/bin/python" ]]; then
    echo "[run] FreeCADCmd not found — using venv Python (may lack FreeCAD modules)."
    exec "${SCRIPT_DIR}/.venv/bin/python" "${MACRO}" "${@:2}"
else
    echo "[run] WARNING: Neither FreeCADCmd nor .venv found. Using system python3."
    exec python3 "${MACRO}" "${@:2}"
fi
WRAPPER_EOF

chmod +x "${RUN_WRAPPER}"
success "Generated run-macro.sh"

# ── Step 7 — Print installed package versions ─────────────────────────────────
info "Installed package summary:"
"${VENV_PIP}" list --format=columns 2>/dev/null | grep -E "^(Package|---|-|numpy|scipy|matplotlib)" || true

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo -e "${BLD}${GRN}Setup complete.${RST}"
echo ""
echo -e "${BLD}To run a macro:${RST}"

if [[ -n "${FREECAD_CMD}" ]]; then
    echo -e "  ${CYN}# Preferred — uses FreeCAD's own Python interpreter:${RST}"
    echo -e "  ${BLD}./run-macro.sh oil-filter-thread-adapter.py${RST}"
    echo ""
    echo -e "  ${CYN}# Or call FreeCADCmd directly:${RST}"
    echo -e "  ${BLD}${FREECAD_CMD} oil-filter-thread-adapter.py${RST}"
else
    echo -e "  ${YEL}Install FreeCAD first: https://www.freecad.org/downloads.php${RST}"
    echo -e "  Then re-run this script, or run macros from the FreeCAD GUI:"
    echo -e "    Macro ▸ Macros… ▸ Browse to .py file ▸ Execute"
fi

echo ""
echo -e "${CYN}  Or open FreeCAD GUI and use:${RST}"
echo -e "  Macro ▸ Macros… ▸ Browse to .py file ▸ Execute"
echo ""
