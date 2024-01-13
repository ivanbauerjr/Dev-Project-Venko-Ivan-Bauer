import getpass
import configparser

class ConfigLinuxNetwork:
    def __init__(self):
        self.logged_in = False
        self.username = "admin"
        self.password = "23456"  # Corresponde a senha "12345" criptografada pela função criptografia "Cifra de César"
        #Tenho consciência de que a Cifra de César não é uma criptografia segura
        #Tenho consciência de que a senha estar diretamente no código-fonte não é uma boa prática
        self.current_user = None

    # Criptografia "Cifra de César", onde cada caracter é substituído pelo caracter seguinte na tabela ASCII
    def criptografia(s):
        chars = []
        for c in s:
            chars.append(chr(ord(c) + 1))
        return ''.join(chars)[::-1]

    def login(self):
        if self.logged_in:
            print("Already logged in.")
            return

        username = input("login: ")

        #o módulo getpass fornece a função getpass() utilizada para solicitar ao usuário uma senha sem que ela seja exibida na tela.
        #R0.2 A senha não pode ser mostrada durante o login, nem gravada em texto puro
        password = getpass.getpass("password: ")
        password = ConfigLinuxNetwork.criptografia(password)

        if username == self.username and password == self.password:
            print("Login successful.")
            self.logged_in = True
            self.current_user = username
        else:
            print("Login failed. Invalid credentials.")

    def show_interfaces(self):
        if not self.logged_in:
            print("Login required.")
            return

        # Implementar lógica para mostrar as interfaces
        # (implementar comandos reais e outputs respectivos)
        print("Intf\tIP address\tMAC\t\tMTU\tState")
        print("eth0\t172.30.19.70/20\t00:15:5d:3d:d5:72\t1500\tUP")
        print("eth1\t172.16.0.1/24\t00:fc:e7:46:e0:07\t1500\tDOWN")

    # Adicionar métodos similares para os outros comandos e requisitos

    def run_command(self, command):
        if not self.logged_in:
            print("Login required.")
            return

        if command.lower() == "show interfaces":
            self.show_interfaces()

        #R0.4 Deve existir um comando para sair do sistema
        elif command.lower() == "exit":
            self.logged_in = False
            print("Logged out. Goodbye!")
        #R0.3 A utilização de parâmetros ou comandos inválidos pelo usuário deve retornar mensagens de erro amigáveis
        else:
            print("Invalid command. Type 'exit' to logout.")

if __name__ == "__main__":
    config_system = ConfigLinuxNetwork()
    print("### Welcome to config linux network system ###")

    while not config_system.logged_in:
        config_system.login()

    while config_system.logged_in:
        user_input = input("> ")
        config_system.run_command(user_input)
