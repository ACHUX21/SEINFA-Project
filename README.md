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