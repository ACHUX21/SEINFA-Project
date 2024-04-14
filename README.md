# SEINFA-Project installation

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