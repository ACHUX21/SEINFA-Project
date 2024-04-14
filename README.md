# SEINFA-Project installation

# For Arch :

# to install python-pip
```shell
yay -S python-pip
```
# to install the python requirments
```shell
pip install flask pyodbc mysql.connector pyjwt
```
# to install mssql driver 17
```bash
yay -S msodbcsql17 
cd && python -m venv .venv
export PATH=$HOME/.venv/bin:$PATH
echo 'export PATH=$HOME/.venv/bin:$PATH' >> .zshrc
```

# For DEBIAN BASED :

# to install the python requirments
```shell
pip install flask pyodbc mysql.connector pyjwt
```

# to install mssql driver 17
```shell
sudo apt-get update && sudo apt-get install -y gnupg2 curl unixodbc-dev
sudo curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
sudo curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
sudo apt-get update && ACCEPT_EULA=Y sudo apt-get install -y msodbcsql17
```

# For DOCKER :

look at the docker file

# compile the project and make it as an executable and run it as a service for windows
## install pyinstaller to compile and create an executable
### install pyinstaller
```bash
pip install pyinstaller
```
### add this code to your main.py
```python
import sys
import os

if getattr(sys, 'frozen', False):
    # The application is frozen
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)

```

### generate the main.spec
```bash
pyinstaller --onefile --windowed main.py
```

### adjust your main.spec
```python
a = Analysis(...
     datas=[ ('templates/', 'templates'), ('static/', 'static') ],
     ...)
```

### rebuild your application
```bash
pyinstaller main.spec
```
## Run the project as a service 
### Create Your Executable: Make sure you have your executable main.exe ready.

### Open Command Prompt as Administrator: Search for "cmd", right-click on the Command Prompt app, and choose "Run as administrator".

### Create the Service:
```bash
sc create MyPythonService binPath= "C:\path\to\main.exe"
```
Replace C:\path\to\main.exe with the full path to your executable. The space after binPath= is required.

### Configure the Service to Start Automatically:
```bash
sc config MyPythonService start= auto
```
### Start the Service:
```bash
sc start MyPythonService
```