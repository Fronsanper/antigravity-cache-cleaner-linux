# Antigravity Cache Cleaner for Linux — By Fronsanper

> A Linux-only utility that installs a graphical setup wizard, creates an Antigravity desktop shortcut, backs up the original shortcut, restores it when requested, and provides a clean uninstall path.

## English (US)

### What this project does

This project turns the Antigravity cache-clearing script into a distributable Linux utility for other users. It includes a graphical Setup Wizard with:

- EN-US as the default interface language, with PT-BR also available;
- a terms and privacy screen;
- a plain-language explanation of what the tool does;
- a confirmation screen before changes are applied;
- a backup of the original `antigravity.desktop` before replacement;
- installation under the user's XDG data directory instead of a hard-coded `/home/<name>` path;
- creation/update of `/usr/share/applications/antigravity.desktop` when administrative access is available;
- a restore action that puts the original desktop file back from the backup;
- an uninstall flow that restores the original file before removing the project;
- bilingual installer and cleaner messages;
- version `1.0.0`.

### Important: what the cleaner removes

The cleaner is based on the original script supplied for this project. It only works with Antigravity's own local configuration/storage paths listed below:

```text
~/.config/Antigravity/User/globalStorage
~/.config/Antigravity/User/workspaceStorage
~/.config/Antigravity/Local Storage
~/.config/Antigravity/IndexedDB
```

It does **not** delete the user's personal files, home-directory files, source-code projects, or files outside the Antigravity locations listed above. The cleaner also terminates `antigravity-ide` and `sde64`, removes `Singleton*` and `code.lock`, and then attempts to launch `/usr/share/antigravity/antigravity-ide` with `--max-old-space-size=8192`.

The directories above are Antigravity-managed local storage. Depending on the Antigravity version and installed extensions, they may contain local cache, extension state, workspace metadata, session information, or similar application data. The cleaner empties those storage directories; it does **not** remove the actual project files stored elsewhere on your system.

**Important:** the installer backup protects the original `.desktop` launcher. It does **not** back up the Antigravity storage directories listed above. Review the terms screen before using the cleaner.

### Installation location

The script is installed under the XDG data directory:

```text
~/.local/share/antigravity-cache-cleaner/clear_cache_antigravity.sh
```

If `XDG_DATA_HOME` is set, it is respected. No username such as `/home/user` is embedded in the project.

### Requirements

- Linux.
- Python 3.
- Tkinter (`python3-tk` on Debian/Ubuntu-based systems).
- A graphical Linux session for the wizard.
- `pkexec` is recommended for graphical administrative authentication; `sudo` may be used as a fallback.
- Antigravity installed at `/usr/share/antigravity/antigravity-ide` for the post-clean launch step.

### Windows

**Windows is not supported.** This project uses Linux paths, Unix permissions, `.desktop` files, `pkill`, `setsid`, `pkexec`/`sudo`, and the Linux Antigravity configuration layout. Windows compatibility has not been tested.

### Quick start

After downloading or cloning the repository:

```bash
git clone https://github.com/Fronsanper/antigravity-cache-cleaner-linux.git
cd antigravity-cache-cleaner-linux
chmod +x install.sh
./install.sh
```

The wizard guides you through language selection, terms, explanation, backup, installation, restore, and uninstall.

If Tkinter is missing on Debian/Ubuntu-based systems:

```bash
sudo apt install python3 python3-tk
```

### Community

- Discord: [NivalityOfficial](https://discord.com/invite/z5gb4zvWsY)
- Telegram: [NivalityOfficial](https://t.me/+Ygtl-pe64d5jN2Nh)
- YouTube: [FronsanperDev](https://www.youtube.com/@FronsanperOfficial)

**By Fronsanper**

---

# Limpador de Cache e Lançador Antigravidade — Feito por Fronsanper

> Utilitário exclusivo para Linux que instala um assistente de configuração gráfico, cria um atalho do Antigravity na área de trabalho, faz backup do atalho original e oferece opções de restauração e desinstalação.

## Português (Brasil)

### O que este projeto faz

Este projeto transforma o script de limpeza do Antigravity em uma instalação distribuível para outras pessoas. O projeto inclui um Setup Wizard em Python/Tkinter com:

- seleção de idioma PT-BR ou EN-US;
- tela de termos e privacidade;
- explicação detalhada do funcionamento;
- confirmação e aviso antes da instalação;
- backup do `antigravity.desktop` original antes da substituição;
- instalação do script em uma pasta de dados do usuário, em vez de depender de `/home/<nome>`;
- criação/substituição do atalho `/usr/share/applications/antigravity.desktop` quando disponível;
- área para restaurar o atalho original pelo backup;
- área para desinstalar, restaurando primeiro o original;
- mensagens do script de limpeza em PT-BR ou EN-US;
- versão `1.0.0`.

### Aviso importante sobre a limpeza

O script original fornecido para este projeto atua somente nas áreas de armazenamento local do próprio Antigravity:

```text
~/.config/Antigravity/User/globalStorage
~/.config/Antigravity/User/workspaceStorage
~/.config/Antigravity/Local Storage
~/.config/Antigravity/IndexedDB
```

Ele **não apaga arquivos pessoais, projetos, códigos-fonte ou outros arquivos do usuário que estejam fora dessas áreas do Antigravity**. Também encerra os processos `antigravity-ide` e `sde64`, remove arquivos `Singleton*` e `code.lock`, e tenta iniciar `/usr/share/antigravity/antigravity-ide` com `--max-old-space-size=8192`.

Essas pastas são armazenamento local do Antigravity e podem conter cache, dados locais de extensões, metadados de workspace, informações de sessão e outros dados de funcionamento do aplicativo. A limpeza esvazia esse armazenamento local, mas não remove os arquivos reais dos seus projetos que ficam em outras pastas do computador.

**Importante:** o backup criado pelo instalador é do atalho `.desktop`, não dessas pastas de armazenamento do Antigravity. Leia e entenda essa parte antes de executar a limpeza.

### Onde o script fica instalado

O script é armazenado usando o diretório de dados XDG do usuário:

```text
~/.local/share/antigravity-cache-cleaner/clear_cache_antigravity.sh
```

Se `XDG_DATA_HOME` estiver definido, o projeto respeita essa variável. Assim, não existe caminho hard-coded para `/home/user` ou para qualquer nome de usuário específico.

### Requisitos

- Linux (desenvolvido e testado para Linux).
- Python 3.
- `python3-tk`/Tkinter para a interface gráfica.
- Sessão gráfica Linux para abrir o wizard.
- `pkexec` é recomendado para pedir autorização administrativa de forma gráfica; se não existir, o projeto pode usar `sudo`.
- Antigravity instalado em `/usr/share/antigravity/antigravity-ide` para o launcher iniciar o aplicativo após a limpeza.

### Windows

**Windows não é suportado.** O projeto usa caminhos Linux, permissões Unix, arquivos `.desktop`, `pkexec`/`sudo`, `pkill`, `setsid` e a estrutura de configuração Linux do Antigravity. O comportamento no Windows não foi testado.

### Instalação

Baixe/clon e o repositório:

```bash
git clone https://github.com/Fronsanper/antigravity-cache-cleaner-linux.git
cd antigravity-cache-cleaner-linux
chmod +x install.sh
./install.sh
```

O wizard guiará você pela seleção de idioma, termos, explicação, backup e instalação.

Caso o sistema não tenha Tkinter:

```bash
sudo apt install python3 python3-tk
```

Em outras distribuições, instale o pacote equivalente de Python 3 + Tkinter.

### O que o instalador altera

1. Cria `~/.local/share/antigravity-cache-cleaner/`.
2. Salva uma cópia do `antigravity.desktop` original em:

```text
~/.local/share/antigravity-cache-cleaner/backup/antigravity.desktop.original
```

3. Guarda metadados do backup.
4. Instala o script executável nessa pasta de dados.
5. Cria o novo `.desktop` apontando para o script via `$HOME`.
6. Salva o idioma selecionado.

### Reverter

O assistente possui uma área de gerenciamento para **Restaurar original**. O processo usa o backup salvo antes da instalação. Se não existia um `antigravity.desktop` original, o projeto registra isso e remove o atalho criado ao restaurar/desinstalar.

### Desinstalar

A desinstalação restaura primeiro o `.desktop` original, quando houver backup, e depois remove os arquivos da instalação.

### Privacidade

O instalador não possui coleta de telemetria, não envia dados para servidores e não precisa de uma conta para funcionar. Os únicos endereços externos exibidos pelo wizard são os links sociais do próprio projeto fornecidos no README.

### Créditos / Links

- Discord: [NivalityOfficial](https://discord.com/invite/z5gb4zvWsY)
- Telegram: [NivalityOfficial](https://t.me/+Ygtl-pe64d5jN2Nh)
- YouTube: [FronsanperDev](https://www.youtube.com/@FronsanperOfficial)

**Feito por Fronsanper**

## Project layout

```text
antigravity-cache-cleaner-linux/
├── assets/
│   └── clear_cache_antigravity.original.sh
├── clear_cache_antigravity.sh
├── install.sh
├── uninstall.sh
├── wizard.py
├── LICENSE.txt
└── README.md
```

## License

MIT. See `LICENSE.txt`.
