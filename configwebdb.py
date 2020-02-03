#!/usr/bin/python3
#This program connects to servers over SSH and installs some software and creates a user

import sys
import pexpect
from pexpect import pxssh

#We use a class here to maintain session data
class ssh:
    
    client = None
    
    #the init function of a class is run when the class is called
    #our init function establishes the ssh connection and saves it
    #for use in other functions within the class
    
    def __init__(self, host, username, password):
        self.client = pxssh.pxssh()
        self.client.login(host, username, password)
        print('SSH Login on ', host)
        self.client.sendline('sudo -s')
        self.client.expect(r"[\$\#\:] ")
        self.client.sendline(password)
        self.client.expect(r"[\$\#] ")
        print('Logged in as root.')

    def install_sql(self):
        s = self.client
        s.sendline('dnf install https://dev.mysql.com/get/mysql80-community-release-fc30-1.noarch.rpm')
        s.expect('[y/N]')
        print('Installing...')
        
        s.sendline('y')
        s.expect(r"[\$\#] ")

        s.sendline('dnf install mysql-community-server')
        s.expect('[y/N]')
        
        s.sendline('y')
        s.expect(r"[\$\#] ")
        s.expect('[y/N]')
        
        s.sendline('y')
        s.expect(r"[\$\#] ")
        print('Installed mySQL.')

        s.sendline('systemctl start mysqld')
        s.expect(r"[\$\#] ")
        print('Started mySQL Service.')

        s.sendline('systemctl enable mysqld')
        s.expect(r"[\$\#] ")
        print('Enabled Autostart.')
        
        s.sendline('exit')
        s.sendline('exit')
        s.close()

    def install_apache(self):
        s = self.client
        s.sendline('yum install httpd')
        print('Installing...')
        s.expect('[y/N]')
        
        s.sendline('y')
        print('Installing.....')
        s.expect(r"[\$\#] ")
        print('Installed Apache.')

        s.sendline('systemctl start httpd')
        s.expect(r"[\$\#] ")
        print('Started Apache Service.')

        s.sendline('systemctl enable httpd')
        s.expect(r"[\$\#] ")
        print('Enabled Autostart.')
        
        s.sendline('exit')
        s.sendline('exit')
        s.close()
    
    def create_user(self):
        s = self.client
        s.sendline('useradd egoad')
        s.expect(r"[\$\#] ")

        s.sendline('passwd egoad')
        s.expect('password:')

        s.sendline('RubberDuck!')
        s.expect('password:')

        s.sendline('RubberDuck!')
        s.expect(r"[\$\#] ")

def main():
    webhosts = ['192.168.0.111', '192.168.0.112'] 
    dbhosts = ['192.168.0.121', '192.168.0.122']
    username = ''
    password = ''
    
    for host in webhosts:
        connect = ssh(host, username, password)
        connect.create_user()
        connect.install_apache()
    
    for host in dbhosts:
        connect = ssh(host, username, password)
        connect.create_user()
        connect.install_sql()

if __name__ == '__main__':
    main()
