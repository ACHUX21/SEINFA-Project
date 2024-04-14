# SEINFA-Project

# to install python-pip
yay -S python-pip
# to install the python requirments
pip install flask pyodbc mysql.connector pyjwt
# to install mssql driver 17
yay -S msodbcsql17 
cd && python -m venv .venv
export PATH=$HOME/.venv/bin:$PATH
echo 'export PATH=$HOME/.venv/bin:$PATH' >> .zshrc