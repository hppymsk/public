#Josh Albertson
#---This code is insecure, and for testing purposes only---
#Installs LAMP stack on remote server using paramiko

import paramiko
import time


host = ['192.168.0.111', '192.168.0.112', '192.168.0.121', '192.168.0.122']
username = 'justincase'
password = 'Password01'

class ssh:
    client = None
    shell = None

    def __init__(self, host, username, password):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(host, username=username, password=password)
        self.shell = self.client.invoke_shell()
    
    def close_connection(self):
        if (self.client != None):
            self.client.close()
    
    def open_shell(self):
        self.shell = self.client.invoke_shell()
    
    def send_command(self, command):
        self.shell.send(command + '\n')
        return self.shell.recv(1024).decode()

    def send_commands(self, commands):
        for command in commands:
            self.shell.send(command + '\n')
            while not self.shell.exit_status_ready() and not self.shell.recv_ready():
                time.sleep(1)
                print(self.shell.recv(1024)).decode()

            output = self.shell.recv(1024)
            output += self.shell.recv(1024)
        time.sleep(0.1)
        return output.decode()
    def expect_prompt(self):
        pass
    def expect_other(self, expect):
        pass
def install_apache():
    commands = ['sudo -s', 'Password01', 'yum install httpd', 'y', 'systemctl start httpd', 'systemctl enable httpd', 'systemctl status httpd']
    #commands = ['ls', 'systemctl is-active httpd']
    
    global username, password, host 
       
    connection = ssh(host[0], username, password)
    connection.open_shell()
    
    for command in commands:
       time.sleep(1)
       print(connection.send_command(command))

    connection.close_connection()

def install_mysql():
    pass

def main():
    install_apache()
    install_mysql()

if __name__ == "__main__":
    main()


#commands = ['sudo -s', 'Password01', 'systemctl is-active httpd']
commands = ['ls', 'systemctl is-active httpd']