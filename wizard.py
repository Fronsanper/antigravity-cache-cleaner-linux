#!/usr/bin/env python3
import json, os, shutil, subprocess, sys, tempfile, textwrap
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

PROJECT_DIR = Path(__file__).resolve().parent
APP_NAME = "Antigravity Cache Cleaner"
VERSION = "1.0.0"
DATA_DIR = Path(os.environ.get("XDG_DATA_HOME", Path.home()/".local/share")) / "antigravity-cache-cleaner"
BACKUP_DIR = DATA_DIR / "backup"
SCRIPT_DEST = DATA_DIR / "clear_cache_antigravity.sh"
LANG_FILE = DATA_DIR / "language"
STATE_FILE = DATA_DIR / "state.json"
DESKTOP_DEST = Path("/usr/share/applications/antigravity.desktop")
LOCAL_DESKTOP_DEST = Path(os.environ.get("XDG_DATA_HOME", Path.home()/".local/share")) / "applications/antigravity.desktop"

STR = {
    "pt_BR": {
        "lang_name": "Português (Brasil)", "title": "Antigravity Cache Cleaner", "subtitle": "Setup Wizard • By Fronsanper",
        "back": "Voltar", "next": "Continuar", "cancel": "Cancelar", "select": "Selecionar",
        "welcome": "Bem-vindo", "welcome_text": "Este assistente instala o limpador de cache do Antigravity, cria o atalho e mantém um backup do atalho original para permitir reversão.",
        "terms": "Termos e privacidade", "terms_text": "O projeto não coleta, envia ou vende dados. Não há telemetria nem conexão de rede feita pelo instalador. A ferramenta altera apenas arquivos locais descritos nesta janela. Ao executar a limpeza, algumas pastas de armazenamento local do Antigravity serão esvaziadas. Leia a documentação antes de usar.",
        "works": "Como funciona", "works_text": "Depois da instalação, o atalho 'Antigravity' chama um script localizado em uma pasta de dados do seu usuário. O script fecha processos do Antigravity/Intel SDE, remove locks e limpa globalStorage, workspaceStorage, Local Storage e IndexedDB; em seguida tenta iniciar o Antigravity. O comportamento de limpeza é baseado no script fornecido por você.",
        "backup": "Backup", "backup_text": "Antes de substituir /usr/share/applications/antigravity.desktop, o instalador salva uma cópia do arquivo original em uma área de backup dentro da pasta de dados do usuário. Se o arquivo original não existir, isso também será registrado.",
        "ready": "Pronto para instalar", "ready_text": "O assistente está pronto para instalar os arquivos, configurar o idioma escolhido e criar o atalho. Será necessária autorização administrativa para alterar o atalho em /usr/share/applications quando esse arquivo existir no sistema.",
        "install": "Instalar", "revert": "Reverter para o original", "uninstall": "Desinstalar", "installed": "Instalação concluída!", "installed_text": "Tudo pronto. O atalho foi configurado e o backup foi preservado. Você pode reverter ou desinstalar por este assistente.",
        "finish": "Obrigado!", "finish_text": "Obrigado por usar o projeto. Siga-me nos canais abaixo:", "close": "Fechar",
        "links": ["Discord", "Telegram", "YouTube", "GitHub"],
        "confirm_cancel": "Cancelar a operação? Nenhuma alteração será aplicada nesta etapa.",
        "need_linux": "Este projeto foi desenvolvido e testado para Linux. Windows não é suportado: os caminhos, permissões, .desktop e ferramentas usadas são específicos do Linux.",
        "success": "Sucesso", "failure": "Falha", "done_install": "Instalação concluída com sucesso.", "done_revert": "O backup original foi restaurado (quando disponível).", "done_uninstall": "Desinstalação concluída e o backup original foi restaurado (quando disponível).",
        "admin": "Autorização administrativa", "admin_text": "Para gravar o atalho em /usr/share/applications, o Linux pode solicitar sua senha de administrador.",
        "not_installed": "A instalação ainda não foi feita.", "no_backup": "Não foi encontrado um backup do atalho original.",
        "main_menu": "Gerenciamento", "main_menu_text": "Escolha uma ação para uma instalação já existente.",
    },
    "en_US": {
        "lang_name": "English (US)", "title": "Antigravity Cache Cleaner", "subtitle": "Setup Wizard • By Fronsanper",
        "back": "Back", "next": "Continue", "cancel": "Cancel", "select": "Select",
        "welcome": "Welcome", "welcome_text": "This wizard installs the Antigravity cache cleaner, creates the launcher shortcut, and keeps a backup of the original shortcut so it can be restored.",
        "terms": "Terms & privacy", "terms_text": "The project does not collect, send, or sell data. There is no telemetry or network connection made by the installer. The tool changes only the local files described here. Running the cleaner empties some Antigravity local storage folders. Read the documentation before use.",
        "works": "How it works", "works_text": "After installation, the 'Antigravity' desktop shortcut calls a script stored in your user data directory. The script closes Antigravity/Intel SDE processes, removes locks, clears globalStorage, workspaceStorage, Local Storage and IndexedDB, then tries to start Antigravity. The cleanup behavior is based on the script you provided.",
        "backup": "Backup", "backup_text": "Before replacing /usr/share/applications/antigravity.desktop, the installer saves a copy of the original file in a backup area inside your user data directory. If the original file does not exist, that is recorded too.",
        "ready": "Ready to install", "ready_text": "The wizard is ready to install the files, configure the selected language, and create the launcher shortcut. Administrative authorization may be required to change /usr/share/applications/antigravity.desktop.",
        "install": "Install", "revert": "Restore original", "uninstall": "Uninstall", "installed": "Installation complete!", "installed_text": "Everything is ready. The shortcut is configured and the backup has been preserved. You can restore or uninstall from this wizard.",
        "finish": "Thank you!", "finish_text": "Thanks for using the project. Follow me here:", "close": "Close",
        "links": ["Discord", "Telegram", "YouTube", "GitHub"],
        "confirm_cancel": "Cancel this operation? No changes will be applied at this stage.",
        "need_linux": "This project was developed and tested for Linux. Windows is not supported: the paths, permissions, .desktop files, and tools are Linux-specific.",
        "success": "Success", "failure": "Failure", "done_install": "Installation completed successfully.", "done_revert": "The original backup was restored (when available).", "done_uninstall": "Uninstallation completed and the original backup was restored (when available).",
        "admin": "Administrative authorization", "admin_text": "To write the shortcut into /usr/share/applications, Linux may ask for your administrator password.",
        "not_installed": "The installation has not been completed yet.", "no_backup": "No original shortcut backup was found.",
        "main_menu": "Management", "main_menu_text": "Choose an action for an existing installation.",
    }
}

LINKS = {
    "Discord": "https://discord.com/invite/z5gb4zvWsY",
    "Telegram": "https://t.me/+Ygtl-pe64d5jN2Nh",
    "YouTube": "https://www.youtube.com/@FronsanperOfficial",
    "GitHub": "https://github.com/Fronsanper",
}


def tk_font(size, weight="normal"):
    return ("TkDefaultFont", size, weight)


def run_privileged_copy(src: Path, dest: Path, mode=0o644):
    # Prefer pkexec for graphical authorization. Fall back to a terminal sudo prompt.
    if shutil.which("pkexec"):
        helper = textwrap.dedent(f"""
        import os, shutil, stat
        shutil.copy2({str(src)!r}, {str(dest)!r})
        os.chmod({str(dest)!r}, {mode})
        """)
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
            f.write(helper); hp = f.name
        try:
            r = subprocess.run(["pkexec", sys.executable, hp], check=False)
            if r.returncode != 0:
                raise RuntimeError(f"pkexec returned {r.returncode}")
        finally:
            try: os.unlink(hp)
            except OSError: pass
    else:
        subprocess.run(["sudo", "-v"], check=True)
        subprocess.run(["sudo", "install", "-m", oct(mode)[2:], str(src), str(dest)], check=True)


def run_privileged_restore(src: Path, dest: Path):
    if shutil.which("pkexec"):
        helper = textwrap.dedent(f"""
        import shutil
        shutil.copy2({str(src)!r}, {str(dest)!r})
        """)
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
            f.write(helper); hp = f.name
        try:
            r = subprocess.run(["pkexec", sys.executable, hp], check=False)
            if r.returncode != 0: raise RuntimeError(f"pkexec returned {r.returncode}")
        finally:
            try: os.unlink(hp)
            except OSError: pass
    else:
        subprocess.run(["sudo", "-v"], check=True)
        subprocess.run(["sudo", "cp", str(src), str(dest)], check=True)


def run_privileged_remove(path: Path):
    if shutil.which("pkexec"):
        helper = textwrap.dedent(f"""
        import os
        try: os.remove({str(path)!r})
        except FileNotFoundError: pass
        """)
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
            f.write(helper); hp = f.name
        try:
            r = subprocess.run(["pkexec", sys.executable, hp], check=False)
            if r.returncode != 0: raise RuntimeError(f"pkexec returned {r.returncode}")
        finally:
            try: os.unlink(hp)
            except OSError: pass
    else:
        subprocess.run(["sudo", "-v"], check=True)
        subprocess.run(["sudo", "rm", "-f", str(path)], check=True)


def make_desktop(lang):
    t = STR[lang]
    script_expr = f'$HOME/{DATA_DIR.relative_to(Path.home())}/clear_cache_antigravity.sh'
    # Use sh -c so $HOME resolves for every user; script itself lives in XDG data path.
    name = "Antigravity"
    comment = "Clear cache and launch Antigravity — By Fronsanper" if lang == "en_US" else "Limpa o cache e inicia o Antigravity — By Fronsanper"
    action = "New Empty Window" if lang == "en_US" else "Nova janela vazia"
    return f'''[Desktop Entry]\nName={name}\nComment={comment}\nGenericName=Text Editor\nExec=/bin/sh -c '"$HOME/{DATA_DIR.relative_to(Path.home())}/clear_cache_antigravity.sh"'\nIcon=/usr/share/pixmaps/antigravity.png\nType=Application\nTerminal=true\nStartupNotify=false\nStartupWMClass=antigravity-ide\nCategories=TextEditor;Development;IDE;\nMimeType=application/x-antigravity-workspace;\nActions=new-empty-window;\nKeywords=vscode;\n\n[Desktop Action new-empty-window]\nName={action}\nName[pt_BR]=Nova janela vazia\nName[en_US]=New Empty Window\nExec=/bin/sh -c '"$HOME/{DATA_DIR.relative_to(Path.home())}/clear_cache_antigravity.sh"'\nIcon=/usr/share/antigravity/resources/app/out/vs/platform/browserOnboarding/static/antigravity.svg\n'''


def save_state(lang, installed=True, original_exists=False):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps({"version": VERSION, "language": lang, "installed": installed, "original_desktop_exists": original_exists}, indent=2), encoding="utf-8")
    LANG_FILE.write_text(lang, encoding="utf-8")


def backup_and_install(lang):
    DATA_DIR.mkdir(parents=True, exist_ok=True); BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    original_exists = DESKTOP_DEST.exists()
    metadata = {"desktop_path": str(DESKTOP_DEST), "original_exists": original_exists}
    (BACKUP_DIR / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    if original_exists:
        shutil.copy2(DESKTOP_DEST, BACKUP_DIR / "antigravity.desktop.original")
    # Keep a second copy under user applications when possible as a fallback only.
    SCRIPT_DEST.write_text((PROJECT_DIR / "clear_cache_antigravity.sh").read_text(encoding="utf-8"), encoding="utf-8")
    os.chmod(SCRIPT_DEST, 0o755)
    (DATA_DIR / "LICENSE.txt").write_text((PROJECT_DIR / "LICENSE.txt").read_text(encoding="utf-8"), encoding="utf-8")
    LANG_FILE.write_text(lang, encoding="utf-8")
    desktop_tmp = DATA_DIR / "antigravity.desktop"
    desktop_tmp.write_text(make_desktop(lang), encoding="utf-8")
    try:
        run_privileged_copy(desktop_tmp, DESKTOP_DEST, 0o644)
    except FileNotFoundError:
        # If system desktop folder/file is not present, install in XDG user applications.
        LOCAL_DESKTOP_DEST.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(desktop_tmp, LOCAL_DESKTOP_DEST)
    save_state(lang, True, original_exists)


def restore_original():
    meta = BACKUP_DIR / "metadata.json"
    orig = BACKUP_DIR / "antigravity.desktop.original"
    if orig.exists():
        run_privileged_restore(orig, DESKTOP_DEST)
        return True
    # If original did not exist, remove our installed shortcut.
    if meta.exists():
        data = json.loads(meta.read_text(encoding="utf-8"))
        if not data.get("original_exists", False):
            try: run_privileged_remove(DESKTOP_DEST)
            except Exception: pass
            try: LOCAL_DESKTOP_DEST.unlink()
            except FileNotFoundError: pass
            return True
    return False


def uninstall_all():
    restore_original()
    try: LOCAL_DESKTOP_DEST.unlink()
    except FileNotFoundError: pass
    # Never delete the user's backup until the operation succeeds; now remove installer files.
    if DATA_DIR.exists():
        shutil.rmtree(DATA_DIR)


class Wizard(tk.Tk):
    def __init__(self, forced_action=None):
        super().__init__()
        self.lang = self.load_lang()
        self.t = STR[self.lang]
        self.title(f"{self.t['title']} — {self.t['subtitle']}")
        self.geometry("820x570"); self.minsize(760, 520)
        self.configure(bg="#0f172a")
        self.current = 0
        self.pages = []
        self.selected_lang = tk.StringVar(value=self.lang)
        self.status = tk.StringVar()
        self.build_shell()
        self.build_pages()
        if forced_action == "uninstall":
            self.show_management(); self.run_action("uninstall")
        else:
            self.show_page(0)

    def load_lang(self):
        try:
            v = LANG_FILE.read_text(encoding="utf-8").strip()
            return v if v in STR else "en_US"
        except Exception:
            return "en_US"

    def build_shell(self):
        header = tk.Frame(self, bg="#111827", height=92); header.pack(fill="x")
        tk.Label(header, text="✦", font=("TkDefaultFont", 30, "bold"), fg="#38bdf8", bg="#111827").pack(side="left", padx=(28,12))
        box = tk.Frame(header, bg="#111827"); box.pack(side="left", fill="x", expand=True, pady=16)
        self.title_label = tk.Label(box, text="", font=tk_font(19,"bold"), fg="white", bg="#111827", anchor="w"); self.title_label.pack(anchor="w")
        self.sub_label = tk.Label(box, text="", font=tk_font(10), fg="#94a3b8", bg="#111827", anchor="w"); self.sub_label.pack(anchor="w")
        self.body = tk.Frame(self, bg="#0f172a"); self.body.pack(fill="both", expand=True, padx=32, pady=25)
        self.footer = tk.Frame(self, bg="#111827", height=70); self.footer.pack(fill="x", side="bottom")
        self.back_btn = tk.Button(self.footer, text="", command=self.back, bg="#1f2937", fg="white", relief="flat", padx=20, pady=10)
        self.back_btn.pack(side="left", padx=18, pady=14)
        self.cancel_btn = tk.Button(self.footer, text="", command=self.cancel, bg="#374151", fg="white", relief="flat", padx=18, pady=10)
        self.cancel_btn.pack(side="right", padx=18, pady=14)
        self.next_btn = tk.Button(self.footer, text="", command=self.next_page, bg="#0284c7", fg="white", activebackground="#0369a1", relief="flat", padx=22, pady=10)
        self.next_btn.pack(side="right", padx=6, pady=14)

    def label_text(self, title, text):
        tk.Label(self.body, text=title, font=tk_font(24,"bold"), fg="white", bg="#0f172a", anchor="w").pack(anchor="w", pady=(0,12))
        tk.Label(self.body, text=text, font=tk_font(12), fg="#cbd5e1", bg="#0f172a", wraplength=720, justify="left", anchor="nw").pack(fill="x", anchor="w")

    def build_pages(self):
        self.pages = [self.page_language(), self.page_welcome(), self.page_terms(), self.page_works(), self.page_backup(), self.page_ready(), self.page_finish()]

    def new_frame(self): return tk.Frame(self.body, bg="#0f172a")

    def page_language(self):
        f=self.new_frame()
        tk.Label(f,text="Language / Idioma",font=tk_font(25,"bold"),fg="white",bg="#0f172a").pack(anchor="w",pady=(10,20))
        tk.Label(f,text="Select the setup language / Selecione o idioma do assistente.",font=tk_font(12),fg="#cbd5e1",bg="#0f172a").pack(anchor="w",pady=(0,20))
        for code, label in (("pt_BR", STR["pt_BR"]["lang_name"]),("en_US", STR["en_US"]["lang_name"])):
            tk.Radiobutton(f,text=label,variable=self.selected_lang,value=code,font=tk_font(14),fg="white",bg="#0f172a",activebackground="#0f172a",activeforeground="white",selectcolor="#1e293b").pack(anchor="w",pady=8)
        return f

    def page_simple(self, key, second_key=None):
        f=self.new_frame()
        tk.Label(f,text=self.t.get(key,""),font=tk_font(25,"bold"),fg="white",bg="#0f172a").pack(anchor="w",pady=(10,18))
        tk.Label(f,text=self.t.get(f"{key}_text", ""),font=tk_font(12),fg="#cbd5e1",bg="#0f172a",wraplength=720,justify="left").pack(anchor="w",fill="x")
        return f


    def page_welcome(self): return self.page_simple("welcome")
    def page_terms(self): return self.page_simple("terms")
    def page_works(self): return self.page_simple("works")
    def page_backup(self): return self.page_simple("backup")
    def page_ready(self):
        f=self.page_simple("ready")
        tk.Label(f,text="\n"+self.t["admin"]+"\n"+self.t["admin_text"],font=tk_font(11),fg="#7dd3fc",bg="#0f172a",wraplength=720,justify="left").pack(anchor="w")
        return f
    def page_finish(self):
        f=self.new_frame()
        tk.Label(f,text=self.t["finish"],font=tk_font(28,"bold"),fg="white",bg="#0f172a").pack(anchor="w",pady=(10,12))
        self.finish_msg=tk.Label(f,text=self.t["finish_text"],font=tk_font(13),fg="#cbd5e1",bg="#0f172a",wraplength=700,justify="left"); self.finish_msg.pack(anchor="w",pady=(0,18))
        links=tk.Frame(f,bg="#0f172a"); links.pack(anchor="w")
        for label,url in LINKS.items():
            b=tk.Button(links,text=label,command=lambda u=url:self.open_url(u),bg="#1e293b",fg="#7dd3fc",relief="flat",padx=14,pady=8); b.pack(side="left",padx=(0,8))
        manage=tk.Frame(f,bg="#0f172a"); manage.pack(anchor="w",pady=(25,0))
        tk.Button(manage,text=self.t["revert"],command=lambda:self.run_action("revert"),bg="#f59e0b",fg="black",relief="flat",padx=15,pady=9).pack(side="left",padx=(0,8))
        tk.Button(manage,text=self.t["uninstall"],command=lambda:self.run_action("uninstall"),bg="#ef4444",fg="white",relief="flat",padx=15,pady=9).pack(side="left",padx=(0,8))
        return f

    def build_management_page(self):
        f=self.new_frame(); self.mgmt=f
        tk.Label(f,text=self.t["main_menu"],font=tk_font(26,"bold"),fg="white",bg="#0f172a").pack(anchor="w",pady=(10,14))
        tk.Label(f,text=self.t["main_menu_text"],font=tk_font(12),fg="#cbd5e1",bg="#0f172a",wraplength=700,justify="left").pack(anchor="w",pady=(0,20))
        row=tk.Frame(f,bg="#0f172a"); row.pack(anchor="w")
        tk.Button(row,text=self.t["revert"],command=lambda:self.run_action("revert"),bg="#f59e0b",fg="black",relief="flat",padx=18,pady=12).pack(side="left",padx=(0,10))
        tk.Button(row,text=self.t["uninstall"],command=lambda:self.run_action("uninstall"),bg="#ef4444",fg="white",relief="flat",padx=18,pady=12).pack(side="left")
        tk.Button(f,text=self.t["close"],command=self.destroy,bg="#334155",fg="white",relief="flat",padx=18,pady=10).pack(anchor="w",pady=20)
        return f

    def show_management(self):
        for w in self.body.winfo_children(): w.pack_forget()
        f=self.build_management_page(); f.pack(fill="both",expand=True)
        self.back_btn.pack_forget(); self.next_btn.pack_forget(); self.cancel_btn.pack_forget(); self.title_label.config(text=self.t["title"]); self.sub_label.config(text=self.t["subtitle"])

    def refresh_text(self):
        self.t=STR[self.selected_lang.get()]
        self.title_label.config(text=self.t["title"]); self.sub_label.config(text=self.t["subtitle"])
        self.back_btn.config(text=self.t["back"]); self.cancel_btn.config(text=self.t["cancel"]); self.next_btn.config(text=self.t["next"] if self.current < 6 else self.t["close"])

    def show_page(self, idx):
        self.current=idx
        for w in self.body.winfo_children(): w.pack_forget()
        if idx < len(self.pages):
            self.pages[idx].pack(fill="both",expand=True)
        self.refresh_text()
        self.back_btn.config(state="normal" if idx>0 else "disabled")
        self.next_btn.config(text=self.t["install"] if idx==5 else self.t["close"] if idx==6 else self.t["next"])
        if idx==5:
            self.next_btn.config(command=self.install_action)
        elif idx==6:
            self.next_btn.config(command=self.destroy)
        else:
            self.next_btn.config(command=self.next_page)

    def next_page(self):
        if self.current==0:
            self.lang=self.selected_lang.get(); self.t=STR[self.lang]
            self.show_page(1); return
        if self.current < 6: self.show_page(self.current+1)

    def back(self):
        if self.current>0: self.show_page(self.current-1)

    def cancel(self):
        if messagebox.askyesno(self.t["cancel"], self.t["confirm_cancel"], parent=self): self.destroy()

    def install_action(self):
        try:
            backup_and_install(self.selected_lang.get())
            self.show_page(6)
            messagebox.showinfo(self.t["success"], self.t["done_install"], parent=self)
        except Exception as e:
            messagebox.showerror(self.t["failure"], f"{e}", parent=self)

    def run_action(self, action):
        try:
            if action=="revert":
                ok=restore_original()
                if not ok: messagebox.showwarning(self.t["success"], self.t["no_backup"], parent=self)
                else: messagebox.showinfo(self.t["success"], self.t["done_revert"], parent=self)
            elif action=="uninstall":
                uninstall_all(); messagebox.showinfo(self.t["success"], self.t["done_uninstall"], parent=self); self.destroy()
        except Exception as e:
            messagebox.showerror(self.t["failure"], str(e), parent=self)

    def open_url(self,url):
        import webbrowser; webbrowser.open(url)

    def management_if_installed(self):
        return STATE_FILE.exists() or SCRIPT_DEST.exists()


if __name__ == "__main__":
    try:
        if "--uninstall" in sys.argv:
            app=Wizard("uninstall")
        elif STATE_FILE.exists() or SCRIPT_DEST.exists():
            app=Wizard(None)
            app.after(50, app.show_management)
        else:
            app=Wizard(None)
        app.mainloop()
    except tk.TclError as e:
        print("Tkinter GUI could not start. Make sure a graphical Linux session and python3-tk are installed.")
        print(e)
        sys.exit(2)
