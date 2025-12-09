#!/usr/bin/env python

import socket, os, argparse, errno

parser = argparse.ArgumentParser(description='Searches for QYF-O491V2 ethernet relay board(s)')
relays = list(range(8)) + ['all']
commands = list(map(lambda x: str(x)+'+', relays)) + list(map(lambda x: str(x)+'-', relays))
parser.add_argument('-b', '--bind', default='192.168.1.100', type=str, metavar='IPADDR', help='IP address of the local interface to search on (default: %(default)s)')
parser.add_argument('-p', '--port', default=60000, type=int, metavar='PORT', help='TCP port to send detection packet from (default: %(default)s)')
parser.add_argument('-P', '--relayport', default=50000, type=int, metavar='PORT', help='TCP port to send detection packet to (default: %(default)s)')
parser.add_argument('-t', '--timeout', default=10, type=int, metavar='SEC', help='seconds to wait for relay board to reply (default: %(default)s)')
parser.add_argument('-e', '--encoding', default='utf-8', type=str, metavar='ENCODING', help='encoding to read module name in (default: %(default)s)')
parser.add_argument('-j', '--json', action='store_true', help='output data in JSON instead of human-readable format (json module shall be available)')
parser.add_argument('-v', '--verbose', action='store_true', help='be verbose: tell about what is being done')
args = parser.parse_args()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
if args.verbose: print(f'Sending broadcast UDP detection packet {args.bind}:{args.port} to port {args.relayport}...')
sock.bind((args.bind,args.port))
payload = b'CH9120_CFG_FLAG\0\4' + bytes(268)
sock.sendto(payload, ('255.255.255.255', args.relayport))
if args.verbose: print(f'Waiting for a reply for {args.timeout} seconds...')

sock.settimeout(args.timeout)
if args.json: import json
try:
    data, addr = sock.recvfrom(1024)
    if args.verbose: print(f'Reply is received from {addr[0]}:{addr[1]}')
    if data[0:16] != b'CH9120_CFG_FLAG\0':
        if args.verbose: print(f'Wrong payload data:', data[0:16].hex(' '))
        if args.json: print(json.dumps({"error": errno.EINVAL}))
        exit(errno.EINVAL)
    namelen = int(data[29])
    mac, ip, name, version = data[17:23].hex(':'), '.'.join(f'{c}' for c in data[30:34]), data[34:29+namelen].decode(args.encoding), int(data[30+namelen])
    if args.json:
        import json
        print(json.dumps({"error": 0, "mac": mac, "ip": ip, "name": name, "version": version}))
    else:
        print('  MAC address:     ', mac)
        print('  IP Address:      ', ip)
        print('  Module name:     ', name)
        print('  Firmware vesrion:', version)
    exit(0)
except socket.timeout:
    if args.verbose: print('Relay did not reply for the required period.')
    if args.json: print(json.dumps({"error": errno.ETIMEDOUT}))
    exit(errno.ETIMEDOUT)
