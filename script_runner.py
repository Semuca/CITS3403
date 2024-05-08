from sys import argv, exit

from app.scripts import create_admin_user

if (len(argv) != 2):
    print("Please pass in one string- the script that you would like to run")
    exit()

scripts = {
    "create_admin_user": create_admin_user
}

script = scripts[argv[1]]
if (script):
    script.main()