FROM codercom/code-server:latest

USER root
RUN apt -y update && apt -y install gcc wget

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
COPY settings.json /root/.local/share/User/settings.json
COPY keybindings.json /root/.local/share/User/keybindings.json

## copy extensions
RUN mkdir -p /root/.local/share/code-server/extensions
WORKDIR /usr/local/share/code-server/ \
ADD extensions /root/.local/share/code-server/extensions

