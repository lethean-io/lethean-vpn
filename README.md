# lethean-vpn
This repository contains code needed to setup and run an exit node on the Lethean Virtual Private Network (VPN) or to use Lethean service as client in CLI mode.
If you are looking for GUI, please look [here](https://github.com/LetheanMovement/lethean-gui)

**The exit node is currently only supported on Linux.**

# Design
ITNS (aka LTHN) VPN dispatcher is a tool that orchestrates all other modules (proxy, VPN, config, etc.). It does not provide any VPN functionality by itself.
The dispatcher uses system packages whenever possible but it runs all instances manually after invoking.
More info about technical design can be found [here](https://lethean.io/vpn-whitepaper/)

## Client mode
As a client, dispatcher uses global SDP platform to fetch data about provider and connect there. There is no automatic payment functionality inside client. It is up to user to send corresponding payments from wallet to provider.
Client will show only instructions what to pay. We do not want to have any connection from client to your wallet allowing automatic payment.
More information about client mode is [here](CLIENT.md)

## Server mode
As a server, dispatcher helps you to create, publish and run your service as a provider. More info about server mode is [here](SERVER.md)

## FAQ

### Provider

#### Q: Is it legal to be provider?
There can be local laws and legality issues in your country or company. Check your legislative about this. We cannot say universally that something is legal or not.
It can differ in countries over the world but you should follow at last some basic rules:

##### Safe your infrastructure #####
You should not allow user to connect to your own network until you are sure you want to. Please refer to [server](SERVER.md) documentation about access lists.

##### Do not allow bad users to do bad things #####
This is probably most critical and complex part. Primary goal of entire Lethean project is privacy for users. But, of course, somebody can use privacy to harmful somebody other. 
It is your responsibility as a provider to do maximum against these users. Our project is here for good users which needs privacy. We will implement many features how to help you with this filtering.

##### Filter traffic #####
You can filter your traffic for specific sites. Please refer to [server](SERVER.md)
 
#### Q: As a provider, do I need audit log?
If somebody does something harmful, you are responsible as an exit node. It is up to you.

#### Q: What is status of IPv4/IPv6 support?
Both client and server works perfectly on IPv4 network. We are working on full native IPv6 support but for now, see this matrix.

| Client  | Provider | Web        | Support             |
| ------- | -------- | -------    | ------------------- | 
| IPv4    | IPv4     | IPv4/IPv6  | Full                |
| IPv6    | IPv6     | IPv4/IPv6  | No-session-tracking |

### Client

#### Q: Will Lethean project make me anonymous? ####
There are lot of next dependencies which you *MUST* follow to be anonymous. Refer to [tor](https://www.torproject.org/). I a short review, your browser, your OS and all other tools around can be used to identify you. 
At least, use dedicated browser with anonymous mode enabled. 

## Directories

### client
 Everything related to client part. More information [here](CLIENT.md)
 
### conf
 Example config files and config templates.
 
### server
 Code related to VPN server part. More information [here](SERVER.md)

### lib
 Library files

 
