### Automated install
For fully automated install, please use our easy deploy script. Please note that this script works only if system is clean and sudo is already configured for user which runs this.

* Never run this on a system already configured for lthnvpnd! It will overwrite config files!
* Securing squid is out of scope of this howto. Please take care and set ACLs there to filter traffic generated by VPN users.
* If you will use full VPN node, do not forget to filter traffic by iptables or other packet filtering tools to filter traffic generated by VPN users.
* In theory, you can use any other HTTP proxy instead of squid, but easy deploy works only for squid now.

```bash
wget https://gitlab.com/lethean.io/vpn/lethean-vpn/-/raw/master/server/easy-deploy-node.sh
chmod +x easy-deploy-node.sh
BRANCH=master ./easy-deploy-node.sh

```

You can use more env variables to tune parameters. See script header for available env variables:
```bash
[ -z "$LTHNPREFIX" ] && LTHNPREFIX=/opt/lthn
[ -z "$BRANCH" ] && BRANCH=master
[ -z "$PROVIDERID" ] && PROVIDERID=""
[ -z "$PROVIDERKEY" ] && PROVIDERKEY=""
[ -z "$DAEMON_BIN_URL" ] && DAEMON_BIN_URL="https://itns.s3.us-east-2.amazonaws.com/Cli/Cli_Ubuntu160464bitStaticRelease/640/lethean-cli-linux-64bit-letheanize-617a36c.tar.bz2"
[ -z "$DAEMON_HOST" ] && DAEMON_HOST="sync.lethean.io"
[ -z "$WALLETPASS" ] && WALLETPASS="abcd1234"
[ -z "$WALLETFILE" ] && WALLETFILE="$LTHNPREFIX/etc/vpn"
[ -z "$CAPASS" ] && CAPASS=1234
[ -z "$CACN" ] && CACN=ITNSFakeNode
[ -z "$ENDPOINT" ] && ENDPOINT="1.2.3.4"
[ -z "$PORT" ] && PORT="8080"
[ -z "$PROVTYPE" ] && PROVTYPE="residential"
[ -z "$EMAIL" ] && EMAIL=""
[ -z "$ZABBIX_SERVER" ] && ZABBIX_SERVER=""
[ -z "$ZABBIX_HOSTNAME" ] && ZABBIX_HOSTNAME=$(uname -n)
[ -z "$ZABBIX_META" ] && ZABBIX_META="LETHEANVPN_NODE"

```