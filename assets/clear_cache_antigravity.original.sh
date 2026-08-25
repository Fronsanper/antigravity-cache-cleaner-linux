#!/bin/bash

# Definição de Cores
BLUE='\033[1;34m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
NC='\033[0m'

clear
echo -e "${BLUE}====================================================${NC}"
echo -e "${BLUE}        ANTIGRAVITY CACHE CLEANER & LAUNCHER        ${NC}"
echo -e "${BLUE}====================================================${NC}"
echo ""

paths=(
    "$HOME/.config/Antigravity/User/globalStorage"
    "$HOME/.config/Antigravity/User/workspaceStorage"
    "$HOME/.config/Antigravity/Local Storage"
    "$HOME/.config/Antigravity/IndexedDB"
)

executar_limpeza() {
    local pass=$1
    echo -e "${CYAN}[*] Passo $pass/2: Fechando processos e limpando cache...${NC}"

    # Fechar processos
    pkill -9 -f "antigravity-ide" 2>/dev/null
    pkill -9 -f "sde64" 2>/dev/null

    sleep 0.5

    # Remover TODAS as travas de instância única
    rm -f "$HOME/.config/Antigravity/Singleton"* 2>/dev/null
    rm -f "$HOME/.config/Antigravity/code.lock" 2>/dev/null

    # Limpar pastas
    for dir in "${paths[@]}"; do
        if [ -d "$dir" ]; then
            rm -rf "$dir"/* 2>/dev/null
            echo -e "${GREEN}    [✓] Limpo: $(basename "$dir")${NC}"
        fi
    done
    echo ""
}

executar_limpeza "1"
sleep 1
executar_limpeza "2"

echo -e "${BLUE}====================================================${NC}"
echo -e "${GREEN}        LIMPEZA CONCLUÍDA! INICIANDO APP...         ${NC}"
echo -e "${BLUE}====================================================${NC}"
echo ""

# Inicia o app totalmente desvinculado do terminal
setsid /usr/share/antigravity/antigravity-ide --js-flags="--max-old-space-size=8192" >/dev/null 2>&1 &
disown

echo -e "${GREEN}[✓] AntiGravity iniciado com sucesso!${NC}"
sleep 2
exit 0
