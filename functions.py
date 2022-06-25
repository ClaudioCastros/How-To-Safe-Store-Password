import bcrypt
import sqlite3
from colorama import Fore, Style
import os
from texttable import Texttable

'''
passwd = 's$cret12'.encode('utf-8')

salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(passwd, salt)

print(salt)
print(hashed)

if bcrypt.checkpw(passwd, hashed):
    print("match")
else:
    print("does not match")
'''

def create_table(connection):
    connection.execute('''
    CREATE TABLE IF NOT EXISTS USUARIOS (
    nome  STRING PRIMARY KEY,
    senha STRING NOT NULL
    )
    WITHOUT ROWID;
    ''')

def create_new_user(connection, username, password):
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(password, salt)
    hashed_pass = hashed_pass.decode('utf-8')

    #Verify if user already exists
    cursor = connection.execute('''SELECT nome FROM USUARIOS WHERE nome=?''', (username,))
    dados = cursor.fetchone()

    if  dados is None:
        connection.execute('insert into USUARIOS values ("%s", "%s")' % (username, hashed_pass))
        connection.commit()
        print(Fore.GREEN + f'Usuário {username.upper()} criado com sucesso.' + Style.RESET_ALL)
        print('Clear Text Password:  ', password.decode('utf-8'))
        print('Hashed Password:      ', hashed_pass)
        print('Hashed Password Salt: ', salt.decode('utf-8'))
    else:
        print(Fore.RED + 'Este usuário já existe no banco de dados.' + Style.RESET_ALL)
        
def delete_user(connection, username):
    cursor = connection.execute('''SELECT nome FROM USUARIOS WHERE nome=?''', (username,))
    dados = cursor.fetchone()

    if  dados is None:
        print(Fore.RED + 'Usuário não existe.' + Style.RESET_ALL)
    else:
        connection.execute('DELETE FROM USUARIOS WHERE nome=?', (username, ))
        connection.commit()
        print(Fore.GREEN + f'Usuário {username.upper()} deletado com sucesso.' + Style.RESET_ALL)

def verify_user_password(connection, username, password):

    cursor = connection.execute('''SELECT nome FROM USUARIOS WHERE nome=?''', (username,))
    dados = cursor.fetchone()

    if  dados is None:
        print(Fore.RED + 'Usuário não encontrado.' + Style.RESET_ALL)
        return


    password = password.encode('UTF-8')
    cursor = connection.execute('select SENHA from USUARIOS where NOME = "%s"' % (username,))
    dados = cursor.fetchone()
    hashed_pass = str(dados[0])
    #print('Debug - Password: ', password)
    hashed_pass = str.encode(hashed_pass)
    #print('Debug - Hashed Passord: ', hashed_pass)
    if bcrypt.checkpw(password, hashed_pass):
        print(Fore.GREEN + "Senha válida." + Style.RESET_ALL)
    else:
        print(Fore.RED + "Senha inválida." + Style.RESET_ALL)

def show_options():
    print()
    print(' Opções '.center(40, '='))
    print('''
    [ 1 ] Realizar Login
    [ 2 ] Criar Usuário
    [ 3 ] Excluir Usuário
    [ 4 ] Mostrar tabela do DB

    [ 0 ] Finalizar Programa
    ''')
    print()

def login(connection):
    print()
    print(' Login '.center(40, '='))
    username = input('Usuário: ')
    password = input('Senha: ')
    verify_user_password(connection, username, password)

def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def show_user_table(connection):
    cursor = connection.execute('select * from USUARIOS')
    dados = cursor.fetchall()
    t = Texttable()
    t.add_row(['Usuario', 'Senha'])
    for user in dados:
        t.add_row([user[0], user[1]])
    print(t.draw())
