#ESXi Patcher
#Uses sftp to send ESXi files to a server then uses ssh commands to update ESXi
#Version: 0.3
#Author: Josh Albertson
#Date: 11/16/2021

import pip

try:
    __import__('paramiko')
except ImportError:
    pip.main(['install', 'paramiko'])

import paramiko

class SSH:
    def __init__(self, host, port, user, password):
        
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(host,port, username=user, password=password)
        
        self.sftp = self.ssh.open_sftp()

    def send_command(self,command, output='stdin'):
        # Run a command
        stdin, stdout, stderr = self.ssh.exec_command(command)
        
        returncode = stdout.channel.recv_exit_status()
        
        #Close file streams
        stdin.close()
        stdout.close()
        stderr.close()

        return (f'Completed with return code: {returncode}')


    def send_file(self, filename, srclocation, destlocation):
        try:
            self.sftp.put(f'{srclocation}{filename}', f'{destlocation}{filename}')
            return (f'File Sent: {filename}')
        except:
            return ('Com Error')
    
    def close_session(self):
        self.ssh.close()
        self.sftp.close()


def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()


def get_info():
    host = input('Enter IP: ')
    password = input('Enter password: ')
    port = 22
    user = 'root'
    
    print('Is this information correct?\n',
        f'Server: {host}\n',
        f' Password: {password}')

    choice = input('[y/n]: ')
    
    if choice in ('y','Y',''):
        return host, port, user, password
    else:
        return get_info()

def main():
    srclocation = 'C:\\ESXi Patcher\\Patch Files\\'
    destlocation = './vmfs/volumes/datastore1/'
    command_list = ['esxcli software profile update -p ESXi-6.7.0-20191104001-standard -d /vmfs/volumes/datastore1/ESXi670-201911001.zip','esxcli software profile update -p ESXi-6.7.0-20191201001s-standard -d /vmfs/volumes/datastore1/ESXi670-201912001.zip','esxcli software profile update -p ESXi-6.7.0-20191204001-standard -d /vmfs/volumes/datastore1/ESXi670-201912001.zip','esxcli software profile update -p ESXi-6.7.0-20200403001-standard -d /vmfs/volumes/datastore1/ESXi670-202004001.zip','esxcli software profile update -p ESXi-6.7.0-20200401001s-standard -d /vmfs/volumes/datastore1/ESXi670-202004002.zip','esxcli software profile update -p ESXi-6.7.0-20200404001-standard -d /vmfs/volumes/datastore1/ESXi670-202004002.zip','esxcli software profile update -p ESXi-6.7.0-20200604001-standard -d /vmfs/volumes/datastore1/ESXi670-202006001.zip','esxcli software profile update -p ESXi-6.7.0-20200801001s-standard -d /vmfs/volumes/datastore1/ESXi670-202008001.zip','esxcli software profile update -p ESXi-6.7.0-20200804001-standard -d /vmfs/volumes/datastore1/ESXi670-202008001.zip','esxcli software profile update -p ESXi-6.7.0-20201004001-standard -d /vmfs/volumes/datastore1/ESXi670-202010001.zip','esxcli software profile update -p ESXi-6.7.0-20201103001-standard -d /vmfs/volumes/datastore1/ESXi670-202011001.zip','esxcli software profile update -p ESXi-6.7.0-20201101001s-standard -d /vmfs/volumes/datastore1/ESXi670-202011002.zip','esxcli software profile update -p ESXi-6.7.0-20201104001-standard -d /vmfs/volumes/datastore1/ESXi670-202011002.zip','esxcli software profile update -p ESXi-6.7.0-20210204001-standard -d /vmfs/volumes/datastore1/ESXi670-202102001.zip','esxcli software profile update -p ESXi-6.7.0-20210301001s-standard -d /vmfs/volumes/datastore1/ESXi670-202103001.zip','esxcli software profile update -p ESXi-6.7.0-20210304001-standard -d /vmfs/volumes/datastore1/ESXi670-202103001.zip','esxcli software profile update -p ESXi-6.7.0-20211101001s-standard -d /vmfs/volumes/datastore1/ESXi670-202111001.zip','esxcli software profile update -p ESXi-6.7.0-20211104001-standard -d /vmfs/volumes/datastore1/ESXi670-202111001.zip']
    file_list = ['ESXi670-201911001.zip', 'ESXi670-201912001.zip', 'ESXi670-202004001.zip', 'ESXi670-202004002.zip', 'ESXi670-202006001.zip', 'ESXi670-202008001.zip', 'ESXi670-202010001.zip', 'ESXi670-202011001.zip', 'ESXi670-202011002.zip', 'ESXi670-202102001.zip', 'ESXi670-202103001.zip','ESXi670-202111001.zip']
    
    print('==================ESXi Patcher==================')
    serverinfo = get_info()

    try:
        print(f'Connecting to: {serverinfo[0]}')
        s = SSH(serverinfo[0], serverinfo[1], serverinfo[2], serverinfo[3])
    except:
        print(f'Could not connect to {serverinfo[0]}')
        return
    
    print('Uploading patch files')
    i=0
    for item in progressBar(file_list, prefix = 'Uploading:', suffix = 'Complete', length = len(file_list)):
        try:
            s.send_file(file_list[i], srclocation, destlocation)
            i+=1
        except:
            print('An error occured during upload.')
            break
    
    print('Running Patch Commands')
    i=0
    for item in progressBar(command_list, prefix = 'Patching:', suffix = 'Complete', length = len(command_list)):
        try:
            s.send_command(command_list[i])
            i+=1
        except:
            print('An error occured while running commands')
            break
    '''
    print('Deleting leftover patch files')
    i=0
    for item in progressBar(file_list, prefix = 'Patching:', suffix = 'Complete', length = len(file_list)):
        try:
            s.send_command(f'rm {destlocation}{file_list[i]}')
            i+=1
        except:
            print('An error occured while deleting')
            break
        
    print('Rebooting ESXi')
    try:
        s.send_command('reboot')
    except:
        print('An error occured during reboot')
    '''
    s.close_session()
    print('Session closed.')
    return

if __name__ == "__main__":
    main()