#!/usr/bin/env python

import socket, os, argparse, errno

parser = argparse.ArgumentParser(description='Controls the QYF-O491V2 ethernet relay board')
relays = list(range(1,9)) + ['all']
commands = list(map(lambda x: str(x)+'+', relays)) + list(map(lambda x: str(x)+'-', relays))
parser.add_argument('command', nargs='*', choices=commands, metavar='N{+|-}', help='turn ON (+) of OFF (-) the desired relay (starting from 1, \'all\' for all relays)')
parser.add_argument('-c', '--client', action='store_true', help='Use TCP client mode instead of server')
parser.add_argument('-i', '--ip', default='guess', type=str, metavar='IPADDR', help='IP address of the local machine to bind to in server mode, or connect to in client mode (default: %(default)s)')
parser.add_argument('-p', '--port', default='guess', type=str, metavar='PORT', help='TCP port to bind to in server mode, or connect to in client mode (default: %(default)s)')
parser.add_argument('-t', '--timeout', default=10, type=int, metavar='SEC', help='seconds to wait for relay board to connect or respond (default: %(default)s)')
parser.add_argument('-v', '--verbose', action='store_true', help='be verbose: tell about what is being done')
args = parser.parse_args()
if args.verbose: print('Commands to execute:', args.command)
if args.ip == 'guess': args.ip = '192.168.1.200' if args.client else '192.168.1.100'
if args.port == 'guess': args.port = '2000' if args.client else '8800'
args.port = int(args.port)

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
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(args.timeout)
        if args.client:
            if args.verbose: print(f'Connecting to {args.ip}:{args.port}, trying for {args.timeout} seconds...')
            conn, addr = sock, (args.ip, args.port)
            sock.connect(addr)
        else:
            if args.verbose: print(f'Waiting for connections at {args.ip}:{args.port} for {args.timeout} seconds...')
            sock.bind((args.ip, args.port))
            sock.listen()
            conn, addr = sock.accept()
        if args.verbose: print(f'Relay board connection from {addr[0]}:{addr[1]} accepted.')
        if args.verbose: print(f'Sending payload 00 {hi}{lo} ff')
        conn.send(bytes.fromhex(f'00 {hi}{lo} ff'))
        if args.verbose: print('Disconnecting from relay board...')
        if not args.client: conn.close()
        sock.close()
    except ConnectionRefusedError:
        if args.verbose: print('Relay refused the connection.')
        exit(errno.ECONNREFUSED)
    except socket.timeout:
        if args.verbose: print('Relay did not connect for the required period.')
        exit(errno.ETIMEDOUT)
if args.verbose: print('All operations completed.')
exit(0)
