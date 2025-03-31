#!/bin/bash
# Gati Analyzer Force Installer
# Author: SABIR

# =====================
#  CONFIGURATION
# =====================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
VENV_NAME="gati_venv"
SCRIPT_NAME="gati.py"

# =====================
#  DETECT ENVIRONMENT
# =====================
detect_environment() {
    echo -e "\n${BLUE}[+] SYSTEM DETECTION ${NC}"
    
    # Detect OS
    case "$(uname -s)" in
        Linux*) OS="Linux" ;;
        Darwin*) OS="MacOS" ;;
        CYGWIN*|MSYS*|MINGW*) OS="Windows" ;;
        *) OS="Unknown" ;;
    esac
    echo -e "${CYAN}>>> OS Detected: ${YELLOW}$OS${NC}"

    # Detect Python
    if command -v python3 &>/dev/null; then
        PY_CMD="python3"
        PIP_CMD="pip3"
    elif command -v python &>/dev/null; then
        PY_CMD="python"
        PIP_CMD="pip"
    else
        echo -e "${RED}[!] CRITICAL: No Python found!${NC}"
        exit 1
    fi

    # Get Python version
    PY_VERSION=$($PY_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    echo -e "${CYAN}>>> Python Version: ${YELLOW}$PY_VERSION${NC}"
}

# =====================
#  HYBRID INSTALLATION
# =====================
hybrid_install() {
    echo -e "\n${BLUE}[+] FORCE INSTALLATION ${NC}"
    
    # Try virtual environment first
    echo -e "${YELLOW}>>> Attempting virtual environment installation...${NC}"
    if [ ! -d "$VENV_NAME" ]; then
        $PY_CMD -m venv "$VENV_NAME"
    fi
    
    # Activate based on OS
    if [[ "$OS" == "Windows" ]]; then
        source "$VENV_NAME/Scripts/activate"
    else
        source "$VENV_NAME/bin/activate"
    fi

    # Install packages in venv
    declare -A PKGS=(
        ["speedtest-cli"]="SpeedTest"
        ["requests"]="HTTP Requests"
        ["ping3"]="Ping Utility"
        ["tk"]="Tkinter GUI"
    )

    for pkg in "${!PKGS[@]}"; do
        echo -ne "${CYAN}>>> Installing ${PKGS[$pkg]} in venv...${NC}"
        pip install --force-reinstall "$pkg" --quiet
        if [ $? -ne 0 ]; then
            echo -e "${RED} FAILED - Trying system-wide...${NC}"
            # Fallback to system install
            if [[ "$OS" != "Windows" ]]; then
                sudo $PIP_CMD install --force-reinstall "$pkg" --quiet
            else
                $PIP_CMD install --force-reinstall "$pkg" --quiet
            fi
            [ $? -eq 0 ] && echo -e "${GREEN} SYSTEM INSTALL SUCCESS${NC}" || echo -e "${RED} COMPLETE FAILURE${NC}"
        else
            echo -e "${GREEN} VENV SUCCESS${NC}"
        fi
    done

    # Special handling for tkinter
    if [[ "$OS" == "Linux" ]]; then
        echo -e "${CYAN}>>> Ensuring tkinter system package...${NC}"
        sudo apt-get install -y python3-tk >/dev/null 2>&1
    fi
}

# =====================
#  SCRIPT PREPARATION
# =====================
prepare_script() {
    echo -e "\n${BLUE}[+] SCRIPT SETUP ${NC}"
    
    # Add shebang if missing
    if ! head -1 "$SCRIPT_NAME" | grep -q python; then
        echo -e "${YELLOW}>>> Adding Python shebang...${NC}"
        sed -i '1i#!/usr/bin/env python3' "$SCRIPT_NAME"
    fi

    # Make executable
    chmod +x "$SCRIPT_NAME"
    
    # Create gati launcher
    echo -e "${YELLOW}>>> Creating Gati launcher...${NC}"
    cat > gati.sh << 'EOF'
#!/bin/bash
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

# Try virtual environment first
if [ -d "$SCRIPT_DIR/gati_venv" ]; then
    if [ -f "$SCRIPT_DIR/gati_venv/bin/activate" ]; then
        source "$SCRIPT_DIR/gati_venv/bin/activate"
    elif [ -f "$SCRIPT_DIR/gati_venv/Scripts/activate" ]; then
        source "$SCRIPT_DIR/gati_venv/Scripts/activate"
    fi
fi

# Run the script
python "$SCRIPT_DIR/gati.py"
EOF

    chmod +x gati.sh
    
    # Windows specific
    if [[ "$OS" == "Windows" ]]; then
        echo -e "${YELLOW}>>> Creating Windows hybrid launcher...${NC}"
        cat > gati.bat << 'EOF'
@echo off
set SCRIPT_DIR=%~dp0

:: Try virtual environment first
if exist "%SCRIPT_DIR%gati_venv\Scripts\activate.bat" (
    call "%SCRIPT_DIR%gati_venv\Scripts\activate.bat"
)

:: Run the script
python "%SCRIPT_DIR%gati.py"
EOF
    fi
}

# =====================
#  VERIFICATION
# =====================
verify_installation() {
    echo -e "\n${BLUE}[+] VERIFICATION ${NC}"
    
    # Check in virtual environment
    if [ -d "$VENV_NAME" ]; then
        echo -e "${CYAN}>>> Checking virtual environment...${NC}"
        if [[ "$OS" == "Windows" ]]; then
            source "$VENV_NAME/Scripts/activate"
        else
            source "$VENV_NAME/bin/activate"
        fi
        pip list | grep -E "speedtest-cli|requests|ping3|tk"
        deactivate
    fi
    
    # Check system-wide
    echo -e "\n${CYAN}>>> Checking system-wide...${NC}"
    $PY_CMD -c "
import sys
modules = ['speedtest', 'requests', 'ping3', 'tkinter']
print('${YELLOW}>>> Module Status:${NC}')
for m in modules:
    try:
        __import__(m)
        print(f'${GREEN}[✓] {m:12} OK${NC}')
    except:
        print(f'${RED}[✗] {m:12} MISSING${NC}')
"
}

# =====================
#  MAIN EXECUTION
# =====================
clear
echo -e "${CYAN}"
cat << "EOF"
   _____       _ _    _                  
  / ____|     | | |  (_)             
 | |  __  __ _| | |_  _ 
 | | |_ |/ _` | | __|| | 
 | |__| | (_| | | |_ | | 
  \_____|\__,_|_|\__||_|  --Dependency Installer--
EOF
echo -e "${NC}"
echo -e "${YELLOW}>>> Force Installer${NC}"
echo -e "${YELLOW}===============================================${NC}"

# Check if script exists
if [ ! -f "$SCRIPT_NAME" ]; then
    echo -e "${RED}[!] ERROR: $SCRIPT_NAME not found!${NC}"
    exit 1
fi

# Run installation
detect_environment
hybrid_install
prepare_script
verify_installation

# Show run instructions
echo -e "\n${GREEN}[+] INSTALLATION COMPLETE! ${NC}"
echo -e "${YELLOW}===============================================${NC}"
echo -e "${CYAN}>>> To run your analyzer:${NC}"

if [[ "$OS" == "Windows" ]]; then
    echo -e "${BLUE}   Double-click gati.bat${NC}"
    echo -e "${YELLOW}   OR${NC}"
    echo -e "${BLUE}   .\\gati.bat${NC}"
else
    echo -e "${BLUE}   ./gati.sh${NC}"
    echo -e "${YELLOW}   OR${NC}"
    echo -e "${BLUE}   python3 $SCRIPT_NAME${NC}"
fi

echo -e "\n${YELLOW}>>> The gati launcher will try virtual environment first,${NC}"
echo -e "${YELLOW}>>> then fall back to system-wide packages if needed${NC}"
echo -e "${YELLOW}===============================================${NC}"
