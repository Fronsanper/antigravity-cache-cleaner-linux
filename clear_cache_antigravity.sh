#!/bin/bash
set -u

# Antigravity Cache Cleaner & Launcher — By Fronsanper
# Linux only. No telemetry, no network access.
# This script intentionally preserves the cleanup behavior of the original
# user-provided script while adding language support and safer checks.

APP_HOME="${XDG_CONFIG_HOME:-$HOME/.config}/Antigravity"
LANG_FILE="${XDG_DATA_HOME:-$HOME/.local/share}/antigravity-cache-cleaner/language"
LANG_CODE="$(cat "$LANG_FILE" 2>/dev/null || true)"
[[ "$LANG_CODE" == "en_US" ]] || LANG_CODE="pt_BR"

if [[ "$LANG_CODE" == "en_US" ]]; then
    T_TITLE='ANTIGRAVITY CACHE CLEANER & LAUNCHER'
    T_STEP='Step %s/2: Closing processes and cleaning cache...'
    T_CLOSED='Antigravity and Intel SDE processes closed.'
    T_CLEAN='Cleaned: %s'
    T_DONE='CLEANUP COMPLETED! STARTING APP...'
    T_STARTED='Antigravity started successfully.'
    T_NOAPP='Antigravity executable was not found at /usr/share/antigravity/antigravity-ide.'
else
    T_TITLE='ANTIGRAVITY CACHE CLEANER & LAUNCHER'
    T_STEP='Passo %s/2: Fechando processos e limpando cache...'
    T_CLOSED='Processos do Antigravity e Intel SDE encerrados.'
    T_CLEAN='Limpo: %s'
    T_DONE='LIMPEZA CONCLUÍDA! INICIANDO APP...'
    T_STARTED='Antigravity iniciado com sucesso.'
    T_NOAPP='O executável do Antigravity não foi encontrado em /usr/share/antigravity/antigravity-ide.'
fi

BLUE='\033[1;34m'; GREEN='\033[1;32m'; YELLOW='\033[1;33m'; CYAN='\033[1;36m'; NC='\033[0m'

clear
printf '%b====================================================%b\n' "$BLUE" "$NC"
printf '%b        %s        %b\n' "$BLUE" "$T_TITLE" "$NC"
printf '%b====================================================%b\n\n' "$BLUE" "$NC"

a=()
a+=("$APP_HOME/User/globalStorage")
a+=("$APP_HOME/User/workspaceStorage")
a+=("$APP_HOME/Local Storage")
a+=("$APP_HOME/IndexedDB")

executar_limpeza() {
    local pass="$1"
    printf '%b[*] ' "$CYAN"; printf "$T_STEP\n" "$pass"; printf '%b' "$NC"

    # Same cleanup targets as the original script.
    pkill -9 -f 'antigravity-ide' 2>/dev/null || true
    pkill -9 -f 'sde64' 2>/dev/null || true
    sleep 0.5

    rm -f "$APP_HOME/Singleton"* 2>/dev/null || true
    rm -f "$APP_HOME/code.lock" 2>/dev/null || true

    for dir in "${a[@]}"; do
        if [[ -d "$dir" ]]; then
            rm -rf -- "$dir"/* 2>/dev/null || true
            printf '%b    [✓] ' "$GREEN"; printf "$T_CLEAN\n" "$(basename "$dir")"; printf '%b' "$NC"
        fi
    done
    echo
}

executar_limpeza 1
sleep 1
executar_limpeza 2

printf '%b====================================================%b\n' "$BLUE" "$NC"
printf '%b        %s        %b\n' "$GREEN" "$T_DONE" "$NC"
printf '%b====================================================%b\n\n' "$BLUE" "$NC"

if [[ -x /usr/share/antigravity/antigravity-ide ]]; then
    setsid /usr/share/antigravity/antigravity-ide --js-flags="--max-old-space-size=8192" >/dev/null 2>&1 &
    disown || true
    printf '%b[✓] %s%b\n' "$GREEN" "$T_STARTED" "$NC"
else
    printf '%b[!] %s%b\n' "$YELLOW" "$T_NOAPP" "$NC"
fi
sleep 2
exit 0
