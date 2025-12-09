#!/usr/bin/env python

import socket, os, argparse, errno

parser = argparse.ArgumentParser(description='Controls the QYF-O491V2 ethernet relay board')
relays = list(range(8)) + ['all']
commands = list(map(lambda x: str(x)+'+', relays)) + list(map(lambda x: str(x)+'-', relays))
parser.add_argument('command', nargs='*', choices=commands, metavar='N{+|-}', help='turn ON (+) of OFF (-) the desired relay (starting from 0, \'all\' for all relays)')
parser.add_argument('-b', '--bind', nargs=1, default='192.168.1.100', type=str, metavar='IPADDR', help='IP address of the local machine to bind to (default: %(default)s)')
parser.add_argument('-p', '--port', nargs=1, default=8800, type=int, metavar='PORT', help='TCP port to bind to (default: %(default)s)')
parser.add_argument('-t', '--timeout', nargs=1, default=10, type=int, metavar='SEC', help='seconds to wait for relay board to connect (default: %(default)s)')
parser.add_argument('-v', '--verbose', action='store_true', help='be verbose: tell about what is being done')
args = parser.parse_args()
if args.verbose: print('Commands to execute:', args.command)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
sock.bind((args.bind, args.port))
sock.listen() 
sock.settimeout(args.timeout)
if args.verbose: print(f'Waiting for connections at {args.bind}:{args.port} for {args.timeout} seconds...')

for cmd in args.command:
    if (cmd[-1] == '+'):
        if args.verbose: print('Enabling ', end='')
        hi = 'f'
    else:
        if args.verbose: print('Disabling ', end='')
        hi = '0'
    if (cmd[:-1] == 'all'):
        if args.verbose: print('ALL relays.')
        lo = '9'
    else:
        if args.verbose: print(f'relay {cmd[:-1]}.')
        lo = cmd[:-1]
    try:
        conn, addr = sock.accept()
        if args.verbose: print(f'Relay board connection from {addr[0]}:{addr[1]} accepted.')
        if args.verbose: print(f'Sending payload 00 {hi}{lo} ff')
        conn.send(bytes.fromhex(f'00 {hi}{lo} ff'))
        if args.verbose: print('Disconnecting from relay board...')
        conn.close()
    except socket.timeout:
        if args.verbose: print('Relay did not connect for the required period.')
        exit(errno.ETIMEDOUT)
if args.verbose: print('All operations completed.')
exit(0)
