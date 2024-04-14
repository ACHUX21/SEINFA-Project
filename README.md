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

# For UBUNTU :

# to install the python requirments
```shell
pip install flask pyodbc mysql.connector pyjwt
```

# to install mssql driver 17
```bash
apt-get update && apt-get install -y gnupg2 curl unixodbc-dev
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17
```