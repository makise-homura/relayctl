## QYF-O491V2 ethernet relay board utilities

### relayctl

Controls the QYF-O491V2 ethernet relay board

#### Usage

```
relayctl.py [-h] [-b IPADDR] [-p PORT] [-t SEC] [-v] [N{+|-} ...]
```

##### Positional arguments:

* `N{+|-}` Turn ON (`+`) of OFF (`-`) the desired relay (starting from 0, `all` for all relays)

##### Options:

* `-h`, `--help`: Show help message and exit
* `-b`, `--bind IPADDR`: IP address of the local machine to bind to (default: `192.168.1.100`)
* `-p`, `--port PORT`: TCP port to bind to (default: `8800`)
* `-t`, `--timeout SEC`: Seconds to wait for relay board to connect (default: `10`)
* `-v`, `--verbose`: Be verbose: tell about what is being done

##### Example:

* `relayctl.py 2+`: Turn on relay 2.
* `relayctl.py 4- 6+`: Turn off relay 4, and then turn on relay 6.
* `relayctl.py all- 0+ 7+`: Turn off all relays, and then turn on relays 0 and 7 (the ones at the edges of the 8-relay board).
* `relayctl.py -b 192.168.1.110 0+`: Turn on relay 0 (while local IP address is configured as `192.168.1.110`, and the relay board is configured to connect to it).
* `relayctl.py -t 30 all-`: Wait 30 seconds for relay board to connect, and then turn off all relays.

### relayfind

Searches for QYF-O491V2 ethernet relay board(s)

#### Usage

```
relayfind.py [-h] [-b IPADDR] [-p PORT] [-P PORT] [-t SEC] [-e ENCODING] [-j] [-v]
```

##### Options:

* `-h`, `--help`: Show help message and exit
* `-b`, `--bind IPADDR`: IP address of the local interface to search on (default: `192.168.1.100`)
* `-p`, `--port PORT`: TCP port to send detection packet from (default: `60000`)
* `-P`, `--relayport PORT`: TCP port to send detection packet to (default: `50000`)
* `-t`, `--timeout SEC`: Seconds to wait for relay board to reply (default: `3`)
* `-e`, `--encoding ENCODING`: Encoding to read module name in (default: `utf-8`)
* `-j`, `--json`: Output data in JSON instead of human-readable format (`json` module shall be available)
* `-v`, `--verbose`: Be verbose: tell about what is being done

**Note**: You probably won't need any options, except `-b`, `-t`, and `-j` or `-v`.

### Installation

Make sure `python` 3.x with `socket`, `os`, `argparse`, `errno` (and `json`, if you want JSON output from `relayfind`) modules is available.

Copy `*.py` into your `bin` directory available in `PATH`, e.g. `/usr/local/bin` (you may also rename all scripts removing `.py` extension)

Make sure you have executable permissions on script files.

### Compatible hardware

It seems to be compatible with these relay boards:

* [DC 5V/12V/24V 4/8 Way TCPIP Network Ethernet Relay Module Switch LAN Control Smart Device Remote Control](https://aliexpress.ru/item/1005008684119961.html)
* [DC 5V/12V/24V 4/8 Way TCPIP Network Ethernet Relay Module Switch LAN Control Smart Device Remote Control](https://aliexpress.ru/item/1005008678520411.html)
* [DC 5V/12V/24V 4/8 Channel TCPIP Network Ethernet Relay Module Switch LAN Control Smart Device Remote Control Trigger Relay Module](https://aliexpress.ru/item/1005008707293453.html)
* [4/8 Way Smart Relay Module Ethernet Relay Programmable Smart Switch Smart Home Control Module Remote Wireless Control Switch](https://aliexpress.ru/item/1005009095608998.html)

Although it was tested on just a single sample board marked as "QYF-O491V2".