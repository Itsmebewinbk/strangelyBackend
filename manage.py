import os
import sys
print(sys.argv)

if len(sys.argv) < 2:
    print("Usage: python manage.py <command>")
    sys.exit(1)

command = sys.argv[1]

if command == "makemigrations":
    message = input("Enter migration message: ")
    os.system(f'alembic revision --autogenerate -m "{message}"')

elif command == "migrate":
    os.system("alembic upgrade head")

elif command == "runserver":
    os.system("uvicorn main:app --reload --port 5000")


elif command == "createapp":
    app_name = input("Enter app name: ")
    os.system(f"mkdir {app_name}")
    os.makedirs(os.path.join(app_name, "cruds"))
    os.makedirs(os.path.join(app_name, "models"))
    os.makedirs(os.path.join(app_name, "schemas"))
    os.makedirs(os.path.join(app_name, "tests"))
    with open(os.path.join(app_name, "cruds", "__init__.py"), "w"):
        pass
    with open(os.path.join(app_name, "models", "__init__.py"), "w"):
        pass
    with open(os.path.join(app_name, "schemas", "__init__.py"), "w"):
        pass
    with open(os.path.join(app_name, "tests", "__init__.py"), "w"):
    
        pass
    with open(os.path.join(app_name, "admin.py"), "w"):
        pass
    with open(os.path.join(app_name, "urls.py"), "w"):
        pass
       



else:
    print("Invalid command. Available commands: makemigrations, migrate, runserver,createapp")
