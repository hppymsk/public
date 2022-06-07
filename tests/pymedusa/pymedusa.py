#!/usr/bin/env pipenv-shebang
#!/usr/bin/env python3

import uuid
import argparse
import fileinput
import datetime
import sys, logging
from os import path
from parsers.parser import Parser

output_file = ""

def print_logo():

    logo = '''
     _____       __  __          _                 
    |  __ \     |  \/  |        | |                
    | |__) |   _| \  / | ___  __| |_   _ ___  __ _ 
    |  ___/ | | | |\/| |/ _ \/ _` | | | / __|/ _` |
    | |   | |_| | |  | |  __/ (_| | |_| \__ \ (_| |
    |_|    \__, |_|  |_|\___|\__,_|\__,_|___/\__,_|
            __/ |                                  
           |___/                                   

   '''
   
    print(logo)

# def loggerCreate(params):
#     logger = logging.getLogger('pymedusa')
#     logger.setLevel(logging.DEBUG)

#     # Output response to a File
#     filename = logging.FileHandler(params.get("output"))
#     filename.setLevel(logging.DEBUG)
#     logger.addHandler(filename)

#     # Output response to Screen
#     # screenOutput = logging.StreamHandler(sys.stdout)
#     # screenOutput.setLevel(logging.DEBUG)
#     # logger.addHandler(screenOutput)

#     return logger

def print_time_start():
    print(
        '# PyMedusa v0.9 ({:%Y-%m-%d %H:%M:%S})'.format(datetime.datetime.now()) + "\n")
    if args.output != None:
        parsed_arguments['filelogger'].debug('# PyMedusa v0.9 ( {:%Y-%m-%d %H:%M:%S})'.format(
            datetime.datetime.now()) + "\n" + syntax_used + "\n")


def print_time_end():
    print(
        '# PyMedusa has finished ({:%Y-%m-%d %H:%M:%S}).'.format(datetime.datetime.now()) + "\n")
    if args.output != None:
        parsed_arguments['filelogger'].debug(
            '# PyMedusa has finished ({:%Y-%m-%d %H:%M:%S}).'.format(datetime.datetime.now()) + "\n")


if __name__ == "__main__":
    # This is where we start parsing arguments
    print_logo()
    parser = argparse.ArgumentParser(description='Python implementation of medusa to work with SMBv2/3',
                                     usage='python3 pymedusa.py module [options]')
    

    subparsers = parser.add_subparsers(
        title='protocols', dest='modules', description='available protocols')

    optional_parser = argparse.ArgumentParser(add_help=False)
    optional_parser.add_argument('-u', '--username-file', action="store",
                                 dest="username", metavar=' ', help='Username or Username File to test')
    #optional_parser.add_argument('-c', '--combo-file', action="store",
    #                             dest="combo", metavar=' ', help='Combo file in the format (username:password)')
    password_parser = optional_parser.add_mutually_exclusive_group()
    password_parser.add_argument('-p', '--password-file', metavar=' ', action="store",
                                 dest="password", help='Password or Password File to test')
    password_parser.add_argument('-e', '--extra', metavar=' ', action="store", dest="extra", choices=['s'], help='Extra options; Use s for password same as username')
    optional_parser.add_argument('-O', '--output', metavar=' ', action='store',
                                 dest='output', help='Log file to save successful logins')
    optional_parser.add_argument('-t', '--threads', help='No. of threads to use', metavar='', action='store', dest='thread', default='30',type=int)
    optional_parser.add_argument('--timeout', help='Timeout to observe', dest='conntimeout', action='store', metavar='', default='3', type=int)

    smb_parser = subparsers.add_parser(
        'smb', help="Can you login with SMB ?", parents=[optional_parser])
    smb_host_parser = smb_parser.add_mutually_exclusive_group(required=True)
    smb_host_parser.add_argument('-H', action="store",
                                 dest="host", help='Hostname or IP address')
    #smb_host_parser.add_argument('--cidr', action='store', help='CIDR subent to target', metavar='', dest='cidr')                                 
    smb_parser.add_argument('-Hash', '--hash-file', action='store',
                            dest='hash', metavar=' ', help='Hash or Hash File to test')

    domain_parser = smb_parser.add_mutually_exclusive_group()
    domain_parser.add_argument('-d', '--domain', metavar=' ', action="store",
                               dest="domain", help='Domain to use with SMB module')
    domain_parser.add_argument('--local', metavar=' ', action="store", dest="localauth",
                               help='Local Account authentication with SMB module', const='True', nargs='?')

    o365_parser = subparsers.add_parser(
        'o365', help="Can you login to Office365 ?", parents=[optional_parser])
    o365_parser.add_argument('--fireproxurl', help='Custom Fireprox URL', metavar='', action='store',dest='url')
    # owa_parser1 = owa_parser.add_mutually_exclusive_group(required=True)
    # owa_parser1.add_argument('-D', '--Domain', metavar=' ',
    #                         help='FQDN to get the Autodiscover', dest='fqdn', action='store')
    # owa_parser1.add_argument('--url', metavar=' ', action='store', dest='url', help='Custom autodiscover URL to target')

    owa_parser = subparsers.add_parser('owa', help="Can you login to OWA Autodiscover?", parents=[optional_parser])
    owa_parser.add_argument('--owaurl', help='OWA base URL', dest='host', action='store',metavar='')

    ews_parser = subparsers.add_parser('ews', help="Can you login to EWS?", parents=[optional_parser])
    ews_parser.add_argument('--ewsurl', help='EWS base URL', dest='host', action='store',metavar='')
    ews_parser.add_argument('--domain', help='Domain', dest='domain', action='store',metavar='')

    jump_parser = subparsers.add_parser('jumpcloud', help="Can you login to JumpCloud?", parents=[optional_parser])

    ldap_parser = subparsers.add_parser('ldap', help="Can you login to LDAP?", parents=[optional_parser])
    ldap_parser.add_argument('-H', help='System/IP to connect to', dest='host',action='store',metavar='')
    ldap_parser.add_argument('--port', help="Port where LDAP service is running", default='389', dest='ldapport', action='store', metavar='')
    ldap_parser.add_argument('--domain', help='Domain prefix', action='store', dest='ldapdomain', metavar='')
    ldap_parser.add_argument('--auth', help='Authentication Type', choices=['Simple','Anonymous','SASL'], action='store', dest='ldapauth',metavar='')

    citrix_parser = subparsers.add_parser('citrix', help="Can you login to Citrix/Netscaler?", parents=[optional_parser])
    citrix_parser.add_argument('--url', help='URL for citrix page (only subdomain and domain', metavar='',dest='host', action='store')
    citrix_parser.add_argument('--fireproxurl', help='Custom Fireprox URL', metavar='', action='store',dest='url')

    cisco_parser = subparsers.add_parser('cisco', help="Can you login to Cisco?", parents=[optional_parser])
    cisco_parser.add_argument('--ciscourl', help='URL for cisco sslvpn page ', metavar='',dest='host', action='store')
    cisco_parser.add_argument('--group', help='Group to target', metavar='', action='store', dest='group')

    ssh_parser = subparsers.add_parser('ssh', help="Can you login to SSH?", parents=[optional_parser])
    ssh_parser.add_argument('-H', help='System/IP to connect to', dest='host',action='store',metavar='')
    ssh_parser.add_argument('--port', help='Port to connect to', dest='sshport', default='22', action='store', metavar='', type=int)

    ftp_parser = subparsers.add_parser('ftp', help="Can you login to FTP?", parents=[optional_parser])
    ftp_parser.add_argument('-H', help='System/IP to connect to', dest='host',action='store',metavar='')
    ftp_parser.add_argument('--port', help='Port to connect to', dest='ftpport', default='21', action='store', metavar='', type=int)

    okta_parser = subparsers.add_parser('okta', help="Can you login to Okta?", parents=[optional_parser])
    okta_parser.add_argument('-d', help='Organization Domain (Provide xyz from xyz.okta.com)', dest='host',action='store',metavar='')
    okta_parser.add_argument('--fireproxurl', help='Custom Fireprox URL', metavar='', action='store',dest='url')

    rdweb_parser = subparsers.add_parser('rdweb', help="Can you login to RDWeb?", parents=[optional_parser])
    rdweb_parser.add_argument('-H', help='RDWeb portal URL', dest='host',action='store',metavar='')

    adfs_parser = subparsers.add_parser('adfs', help="Can you login to ADFS?", parents=[optional_parser])
    adfs_parser.add_argument('-d', help='Organization Domain (Provide xyz.com)', dest='host',action='store',metavar='')
    adfs_parser.add_argument('--fireproxurl', help='Custom Fireprox URL', metavar='', action='store',dest='url')

    me_parser = subparsers.add_parser('manageengine', help="Can you login to ManageEngine Servicedesk?", parents=[optional_parser])
    me_parser.add_argument('-d', help='Organization Domain (Provide from dropdown on login Page)', dest='domain',action='store',metavar='')
    me_parser.add_argument('-H', help='ManageEngine URL without http/https (e.g., manage.example.com or manage.example.com:8080)',
                           dest='host',action='store',metavar='')

    basic_parser = subparsers.add_parser('basic', help="Can you login to Basic Auth Page?", parents=[optional_parser])
    basic_parser.add_argument('-s', help='Enable SSL', dest='ssl',action='store',metavar='')
    basic_parser.add_argument('--dir', help='directory to target', dest='directory',action='store',metavar='')
    basic_parser.add_argument('-H', help='Host', dest='host',action='store',metavar='')

    gp_parser = subparsers.add_parser('globalprotect', help="Can you login to GlobalProtect?", parents=[optional_parser])
    gp_parser.add_argument('-H', help='System/IP to connect to', dest='host',action='store',metavar='')
    #gp_parser.add_argument('--fireproxurl', help='Custom Fireprox URL', metavar='', action='store',dest='url')

    forti_parser = subparsers.add_parser('fortigate', help="Can you login to Fortigate/Fortinet?", parents=[optional_parser])
    forti_parser.add_argument('-H', help='System/IP to connect to', dest='host',action='store',metavar='')
    forti_parser.add_argument('--port', help="Port where VPN service is running", default='443', dest='port', action='store', metavar='')


    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    
    if args.extra == None:
        if (args.password == None and args.hash == None):
            print("No Password or Password file provided. Exiting")
            sys.exit(1)

    banner = "# PyMedusa v0.9 [http://www.foofus.net] (C) sph1nx (Inspired by JoMo-Kun) Foofus Networks <sph1nx@foofus.net>"
    print(
        "# PyMedusa v0.9 [http://www.foofus.net] (C) sph1nx (Inspired by JoMo-Kun) Foofus Networks <sph1nx@foofus.net>" + "\n")
    syntax_used = 'pymedusa.py ' + ' '.join(sys.argv[1:])

    args_instance = Parser()
    parsed_arguments = args_instance.parse_values(vars(args))
    #print(parsed_arguments)


    # if parsed_arguments.get("output"):
    #     loghandle = loggerCreate(parsed_arguments)

    print_time_start()

    args_instance.workerfunc(parsed_arguments)

    print_time_end()
