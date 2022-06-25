from functions import *
from time import sleep

#DataBase Connection
connection = sqlite3.connect('./db.sqlite3')
create_table(connection)
while True:
    show_options()
    option = input('Digite uma opção: ')

    if option == '1' or option == '01':
        clr()
        login(connection)

    elif option == '2' or option == '02':
        clr()
        print()
        print(' Novo Usuário '.center(40, '='))
        username = str(input('New Login: '))
        password = str(input('New Password: '))
        create_new_user(connection, username, password)

    elif option == '3' or option == '03':
        clr()
        print()
        print(' Excluir Usuário '.center(40, '='))
        username = str(input('Login Usuário: '))
        delete_user(connection, username)
    elif option == '4' or option == '04':
        clr()
        show_user_table(connection)

    elif option == '0' or option == '00':
        print('Saindo...')
        sleep(3)
        break

    else:
        print(Fore.RED + 'Opção inválida!' + Style.RESET_ALL)
        
