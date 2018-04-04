#!/bin/sh

. build/env.sh

if [ -z "$ITNS_PREFIX" ]; then
    echo "You must configure intense-vpn!"
    exit 1
fi

install_dir() {
    install $2 $3 $4 $5 $6 -o "$ITNS_USER" -g "$ITNS_GROUP" -d "$INSTALL_PREFIX/$ITNS_PREFIX/$1"
}

# Create directories
install_dir 
install_dir bin
install_dir etc
install_dir var -m 770
install_dir var/ha -m 770
install_dir var/ovpn -m 770
install_dir lib
install_dir dev/net

# Install tun device
"$OPENVPN_BIN" --mktun --dev $ITNS_PREFIX/dev/tun0 --dev-type tun --user $ITNS_USER --group $ITNS_GROUP

# Copy bin files
install -o "$ITNS_USER" -g "$ITNS_GROUP" -m 770 ./server/dispatcher/itnsdispatcher.py $INSTALL_PREFIX/$ITNS_PREFIX/bin/itnsdispatcher

# Copy lib files
for f in authids.py  config.py sdp.py  services.py  sessions.py  util.py; do
    install -o "$ITNS_USER" -g "$ITNS_GROUP" -m 440 ./server/dispatcher/$f $INSTALL_PREFIX/$ITNS_PREFIX/lib/
done

# Copy configs
(cd conf; for f in *tmpl *cfg *ips *doms *http; do
    install -C -o "$ITNS_USER" -g "$ITNS_GROUP" -m 440 ./$f $INSTALL_PREFIX/$ITNS_PREFIX/etc/ 
done)
if ! [ -f $INSTALL_PREFIX/$ITNS_PREFIX/etc/dispatcher.json ]; then
    echo "You have to create $INSTALL_PREFIX/$ITNS_PREFIX/etc/dispatcher.json"
    echo "You can use conf/dispatcher_example.json as source"
fi

if ! [ -f $INSTALL_PREFIX/$ITNS_PREFIX/etc/sdp.json ]; then
    echo "You have to create $INSTALL_PREFIX/$ITNS_PREFIX/etc/sdp.json"
    echo "Look into conf/sdp_example.json and create your own config" 
fi

if ! [ -f $INSTALL_PREFIX/$ITNS_PREFIX/etc/ca/index.txt ]; then
        if [ -f ./build/ca/index.txt ]; then
            install_dir etc/ca -m 700
            cp -R build/ca/* $INSTALL_PREFIX/$ITNS_PREFIX/etc/ca/
        else
            echo "CA directory $INSTALL_PREFIX/$ITNS_PREFIX/etc/ca/ not prepared! You should generate by configure or use your own CA!"
            exit 3
        fi
fi

if ! [ -f $INSTALL_PREFIX/$ITNS_PREFIX/etc/dhparam.pem ] && [ -f build/dhparam.pem ]; then
    install build/dhparam.pem $INSTALL_PREFIX/$ITNS_PREFIX/etc/
fi

if ! [ -f $INSTALL_PREFIX/$ITNS_PREFIX/etc/openvpn.tlsauth ]; then
    "$OPENVPN_BIN" --genkey --secret $INSTALL_PREFIX/$ITNS_PREFIX/etc/openvpn.tlsauth
fi

chown -R $ITNS_USER:$ITNS_GROUP $INSTALL_PREFIX/$ITNS_PREFIX/etc/
chmod -R 700 $INSTALL_PREFIX/$ITNS_PREFIX/etc/