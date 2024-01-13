import getpass
import configparser
import hashlib
import subprocess

class ConfigLinuxNetwork:
    def __init__(self):

        config = configparser.ConfigParser()
        config.read('config.ini')

        self.logged_in = False
        self.username = config.get('database', 'username')
        self.password = config.get('database', 'hashed_password')

    # Para comparar as senhas, é necessário aplicar o mesmo algoritmo de hash utilizado para gerar a senha armazenada no arquivo config.ini
    def compare_passwords(input_password, stored_hashed_password):
        hashed_input_password = hashlib.sha256(input_password.encode('utf-8')).hexdigest()
        return hashed_input_password == stored_hashed_password

    def login(self):
        if self.logged_in:
            print("Already logged in.")
            return

        username = input("login: ")

        #o módulo getpass fornece a função getpass() utilizada para solicitar ao usuário uma senha sem que ela seja exibida na tela.
        #R0.2 A senha não pode ser mostrada durante o login, nem gravada em texto puro
        input_password = getpass.getpass("password: ")

        #compara as senhas
        if self.compare_passwords(input_password, self.password) and (username == self.username):
            print("### Welcome to config linux network system ###")
            self.logged_in = True
        else:
            print("Login failed. Invalid credentials.")

    def show_interfaces(self):
        if not self.logged_in:
            print("Login required.")
            return

        try:
                    # Usando o módulo subprocess para executar o comando real do sistema operacional
                    result = subprocess.run(['ip', 'addr'], capture_output=True, text=True, check=True)

                    # Exibindo a saída de uma maneira mais amigável (este formato pode variar)
                    print("Intf\tIP address\tMAC\t\tMTU\tState")
                    for line in result.stdout.split('\n'):
                        if 'inet ' in line and 'link/ether' in line:
                            words = line.split()
                            intf = words[1]
                            ip_address = words[5]
                            mac = words[11]
                            mtu = words[7]
                            state = "UP" if "UP" in words else "DOWN"
                            print(f"{intf}\t{ip_address}\t{mac}\t{mtu}\t{state}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e.stderr}")

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

    while not config_system.logged_in:
        config_system.login()

    while config_system.logged_in:
        user_input = input("> ")
        config_system.run_command(user_input)
