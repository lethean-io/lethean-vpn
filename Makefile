PASS=1234
CN=ItnsVPNFakeCN
DOCKER=docker

-include env.mk

all:
env.mk:
	@if [ "$(MAKECMDGOALS)" != "docker" ]; then \
	    if ! [ -f env.mk ]; then echo "You must configure first!" ; ./configure.sh --help; exit 1; fi; \
	    echo "Seems to be configured. Run make install."; \
	fi
	

install: env.mk
	chmod +x install.sh
	INSTALL_PREFIX=$(INSTALL_PREFIX) \
	FORCE=$(FORCE) \
	LTHN_PREFIX=$(LTHN_PREFIX) \
	OPENVPN_BIN=$(OPENVPN_BIN) \
	PYTHON_BIN=$(PYTHON_BIN) \
	PIP_BIN=$(PIP_BIN) \
	SUDO_BIN=$(SUDO_BIN) \
	HAPROXY_BIN=$(HAPROXY_BIN) \
	OPENSSL_BIN=$(OPENSSL_BIN) \
	LTHN_USER=$(LTHN_USER) \
	LTHN_GROUP=$(LTHN_GROUP) \
	CLIENT=$(CLIENT) \
	SERVER=$(SERVER) \
	./install.sh
	
install-client:
	@$(MAKE) install CLIENT=y
	
install-server:
	@$(MAKE) install SERVER=y

clean:
	@echo Note this cleans only build directory. If you want to uninstall package, do it manually by removing files from install location.
	@echo Your last install dir is $(LTHN_PREFIX)
	rm -rf build

ca: build/ca/index.txt
	
build/ca/index.txt: env.mk
	./configure.sh --generate-ca --with-capass "$(PASS)" --with-cn "$CN"

docker-img:
	docker build --load -t lthn/vpn:dev .

docker: docker-img

docker-clean:
	docker rm -v lthn/vpn:dev

docker-shell:
	mkdir -p build/etc
	mkdir -p build/bcdata
	docker run -i -t \
	  --mount type=bind,source=$$(pwd)/build/etc,target=/opt/lthn/etc \
   	  --mount type=bind,source=$$(pwd)/build/bcdata,target=/home/lthn \
	  lthn/vpn:dev sh

lthnvpnc:
	mkdir bin
	@echo pyinstaller --add-data "lib;lib" --add-data "conf;conf" \
	  --add-data "bin/cygwin1.dll;bin" --add-data "bin/cygcrypto-1.0.0.dll;bin" --add-data "bin/cygz.dll;bin" \
	  --add-data "bin/liblzo2-2.dll;bin" --add-data "bin/libpkcs11-helper-1.dll;bin" \
	  --add-data "bin/cygpcre-1.dll;bin" --add-data "bin/cygssl-1.0.0.dll;bin" \
	  --add-binary "bin/openvpn.exe;bin" --add-binary "bin/tstunnel.exe;bin" --add-binary "bin/haproxy.exe;bin" \
	  -p lib -p 'C:\Python37\Lib\site-packages' \
	  --noconfirm --log-level=WARN --onefile --nowindow \
	  client/lthnvpnc.py

	