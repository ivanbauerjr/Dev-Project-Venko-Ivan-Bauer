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
    def compare_passwords(self, input_password, stored_hashed_password):
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
        if (username == self.username):
            if self.compare_passwords(input_password, self.password):
                print("\n### Welcome to config linux network system ###")
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

            '''words = result.split()
            for w in words:
                    intf = words[1]
                    ip_address = next((w for w in words if "inet" in w), "N/A")
                    mac = next((w for w in words if "ether" in w), "N/A")
                    mtu = words[7]
                    state = "UP" if "UP" in words else ("DOWN" if "DOWN" in words else "UNKNOWN")
                    print(f"{intf}\t{ip_address}\t{mac}\t{mtu}\t{state}")
            '''

        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e.stderr}")

    def show_routes(self):
        if not self.logged_in:
            print("Login required.")
            return
        
        try:
            result = subprocess.run(["ip", "route"], capture_output=True, text=True, check=True)
            #Devo alterar para listar de uma maneira mais amigável ao usuário. Ainda estou em dúvida qual maneira.
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e.stderr}")

    def create_bridge(self):
        if not self.logged_in:
            print("Login required.")
            return
        
        # Pedir ao usuário o nome desejado para a bridge
        bridge_name = input("Type the desired Bridge Bame: ")

        # Verificar se o nome é válido (pode precisar de verificações adicionais)
        if not bridge_name:
            print("Error: invalid Bridge Name")
            return

        try:
            # Tentar criar a bridge
            subprocess.run(["brctl", "addbr", bridge_name], check=True)
            print(f"Bridge '{bridge_name}' successfully created.")

        except subprocess.CalledProcessError as e:
            # Lidar com erros
            print(f"Error creating the Bridge: {e}")

    def config_ip(self):
        if not self.logged_in:
            print("Login required.")
            return

        # Pedir ao usuário o nome da interface
        interface_name = input("Type the desired Interface Name: ")

        # Verificar se o nome é válido (pode precisar de verificações adicionais)
        if not interface_name:
            print("Error: invalid Interface Name")
            return

        # Pedir ao usuário o IP desejado para a interface
        ip_address = input("Type the desired IP Address: ")

        # Verificar se o IP é válido (pode precisar de verificações adicionais)
        if not ip_address:
            print("Error: invalid IP Address")
            return

        try:
            # Tentar configurar o IP
            subprocess.run(["ip", "addr", "add", ip_address, "dev", interface_name], check=True)
            print(f"IP Address '{ip_address}' successfully configured.")

        except subprocess.CalledProcessError as e:
            # Lidar com erros
            print(f"Error configuring the IP Address: {e}")

    def run_command(self, command):
        if not self.logged_in:
            print("Login required.")
            return

        if command.lower() == "show interfaces":
            self.show_interfaces()
        
        elif command.lower() == "show routes":
            self.show_routes()

        elif command.lower() == "create bridge":
            self.create_bridge()

        elif command.lower() == "config ip":
            print("Not implemented yet.")

        #R0.4 Deve existir um comando para sair do sistema
        elif command.lower() == "exit":
            self.logged_in = False
            print("Logged out. Goodbye!")
        #R0.3 A utilização de parâmetros ou comandos inválidos pelo usuário deve retornar mensagens de erro amigáveis
        else:
            print("\nInvalid command.")

if __name__ == "__main__":
    config_system = ConfigLinuxNetwork()

    while not config_system.logged_in:
        config_system.login()

    while config_system.logged_in:
        print("\nAvailable commands:")
        print("Type 'show interfaces' to show interfaces")
        print("Type 'show routes' to show routes")
        print("Type 'create bridge' to create bridges")
        print("Type 'config ip' to configure ip address on interfaces")
        print("Type 'exit' to logout\n")
        user_input = input("> ")
        config_system.run_command(user_input)
