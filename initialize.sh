echo "Setting up virtual directory"
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt

echo "Generating a random secret for django into [./main/secret_key.txt]"
head /dev/urandom | LC_ALL=C tr -dc A-Za-z0-9 | head -c 40 > ./main/secret_key.txt

echo "Migrating Database"
python manage.py migrate

echo "Creating super user for django admin login"
python manage.py createsuperuser

echo "Starting web server. You can do this manually via debug is vscode or [python ./main/manage.py runserver]"
python ./main/manage.py runserver