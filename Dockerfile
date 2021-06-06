FROM codercom/code-server:latest

ENV http_proxy "http://10.158.100.6:8080/"
ENV https_proxy "http://10.158.100.6:8080/"
ENV no_proxy="localhost,127.0.0.1,instance-data,169.254.169.254,nokia.net,.nsn-net.net,.nsn-rdnet.net,.ext.net.nokia.com,.int.net.nokia.com,.inside.nsn.com,.inside.nokiasiemensnetworks.com"

RUN wget https://github.com/microsoft/vscode-cpptools/releases/download/1.4.0/cpptools-linux.vsix
RUN mkdir -p /usr/local/share/code-server
RUN code-server \
	--user-data-dir /usr/local/share/code-server \
	--install-extension golang.go \
	--install-extension ms-python.python \
	--install-extension formulahendry.code-runner \
	--install-extension eamodio.gitlens \
	--install-extension coenraads.bracket-pair-colorizer \
	--install-extension oderwat.indent-rainbow \
	--install-extension windmilleng.vscode-go-autotest \
	--install-extension vscode-icons-team.vscode-icons \
	--install-extension esbenp.prettier-vscode \
	--install-extension ryu1kn.text-marker \
	--install-extension streetsidesoftware.code-spell-checker \
  --install-extension kdarkhan.mips \
  --install-extension plorefice.devicetree \
	--install-extension cpptools-linux.vsix
RUN rm -f cpptools-linux.vsix

## set default settings
COPY settings.json /usr/local/share/code-server/User/settings.json
COPY keybindings.json /usr/local/share/code-server/User/keybindings.json


