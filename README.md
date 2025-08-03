# FsocietyControlToolkit 
![fsociety_control_toolkit](https://github.com/user-attachments/assets/053b52fb-fa61-494a-b954-07dcb4db964c)

<a href="LICENSE"><img alt="License" src="https://img.shields.io/github/license/mashape/apistatus.svg"></a>  
[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)  
[![Platform](https://img.shields.io/badge/Windows-10/11+-0078D6?logo=windows)](https://www.microsoft.com/windows)  


## About the Project
**FsocietyControlToolkit** is a multifunctional Python-based tool for automated control of Android devices via ADB and scrcpy.

*This tool is designed for **Windows only***.

**Key Features**:
- Control Android devices over USB
- Automatic device detection
- Screen mirroring via `scrcpy`
- Modular architecture support
- Lightweight and intuitive console interface

---

## Requirements (Windows only)

### 1. Install ADB (Android Debug Bridge)
- Download Android Platform Tools:  
  [https://developer.android.com/tools/releases/platform-tools](https://developer.android.com/tools/releases/platform-tools)
- Extract the archive and add the folder path to your **System PATH**  
  (e.g., `C:\platform-tools`)

### 2. Install `scrcpy` (for screen mirroring)
- Download the latest version of scrcpy:  
  [https://github.com/Genymobile/scrcpy/releases](https://github.com/Genymobile/scrcpy/releases)
- Extract the folder and add it to your **System PATH**

Make sure you can run `adb` and `scrcpy` from the terminal (CMD/PowerShell).

---

## Quick Start

### 3. Clone the project and install dependencies
```bash
git clone https://github.com/vicouncil/FsocietyControlToolkit.git
cd FsocietyControlToolkit
pip install -r requirements.txt
python fsociety.py
```
***
Si tout ça ne fonctionne pas essayez ce tuto
***
🧰 ÉTAPE 1 — Installer les outils nécessaires
✅ 1.1 Installer ADB (Android Debug Bridge)
Télécharge ce ZIP :
👉 https://developer.android.com/studio/releases/platform-tools

Extrais le dossier platform-tools où tu veux (ex : C:\ADB)

Ajoute ce dossier au PATH :

Touche Windows → tape variables d’environnement

Clique sur "Variables d’environnement"

Clique sur Path > Modifier > Nouveau

Colle : C:\ADB\platform-tools

Teste :
Ouvre CMD → tape :

bash
Copier
Modifier
adb devices
Ton appareil doit apparaître (s’il est branché avec le débogage USB activé).

✅ 1.2 Installer scrcpy
Va ici :
👉 https://github.com/Genymobile/scrcpy/releases

Télécharge la dernière version .zip pour Windows (ex : scrcpy-win64-v2.4.zip)

Extrais-le dans un dossier (ex : C:\scrcpy)

Ajoute ce dossier au PATH comme pour ADB

Teste :

bash
Copier
Modifier
scrcpy
Si ça ouvre l'écran de ton téléphone, c'est bon ✅

🐍 ÉTAPE 2 — Installer Python et les dépendances
✅ 2.1 Installer Python 3.10+
Télécharge ici :
👉 https://www.python.org/downloads/windows

Coche “Add Python to PATH” pendant l’installation.

✅ 2.2 Installer les modules nécessaires
Ouvre une fenêtre CMD et tape :

bash
Copier
Modifier
pip install pillow colorama
🗂️ ÉTAPE 3 — Préparer ton projet
✅ Crée un dossier FsocietyControlToolkit avec :
Ton script .py (tu peux le nommer fsociety_gui.py)

Une image fsociety.jpg (logo à afficher dans l’appli)

Une icône fsociety.ico (pour la fenêtre et l’exécutable final)

📁 Exemple structure :

Copier
Modifier
FsocietyControlToolkit\
│
├── fsociety_gui.py
├── fsociety.jpg
├── fsociety.ico
🧪 ÉTAPE 4 — Lancer le script en test
Dans le CMD, place-toi dans le dossier :

bash
Copier
Modifier
cd C:\Users\TONNOM\Desktop\FsocietyControlToolkit
python fsociety_gui.py
💡 Si tout est bien installé, ton GUI Fsociety s’ouvrira. Teste les menus.

🛠️ ÉTAPE 5 — Générer un exécutable .exe
✅ 5.1 Installer PyInstaller
bash
Copier
Modifier
pip install pyinstaller
✅ 5.2 Compiler
Dans le même dossier :

bash
Copier
Modifier
pyinstaller --noconsole --onefile --icon=fsociety.ico fsociety_gui.py
