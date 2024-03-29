# Author: Sun Jianguo
# Build command: 
# docker build --build-arg UID=$(id -u) --build-arg GID=$(id -g) -t jgsun/code-server:latest .
FROM codercom/code-server:latest

ARG UID=1000
ARG GID=1000

## Set proxy if build from internal subnet
# ENV http_proxy "http://135.251.33.15:8080"
# ENV https_proxy "https://135.251.33.15:8080"
# ENV no_proxy="localhost,127.0.0.1"

USER root
RUN apt -y update && apt -y install build-essential gdb gcc wget mercurial && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs > rust-init && \
    chmod 755 rust-init && ./rust-init -y && \
    mv ~/.cargo /home/coder/ && \
    mv ~/.rustup /home/coder/ && \
    echo ". "/home/coder/.cargo/env"" >> /home/coder/.bashrc
#    snap install rustup --classic

## The latest version don't release vsix file in the github, so we download vsix from Microsoft
## https://marketplace.visualstudio.com/VSCode and copy them into container when building.
## RUN wget https://github.com/microsoft/vscode-cpptools/releases/download/1.7.1/cpptools-linux.vsix
COPY --chown=$UID:$GID vsix/* /home/coder/

## change owner and group for /home/coder, or else hit "error EACCES: permission denied, mkdir '/home/coder/.config'"
## change owner and group for /home/coder/.cargo as well, or else rust-analizer don't work because of permission,
## we can also give "chmod -R 777" as well.
RUN chown $UID:$GID  /home/coder && chown $UID:$GID /home/coder/.cargo
# RUN chown $UID:$GID  /home/coder && chmod -R 777 /home/coder/.cargo
# RUN ls /home/coder && pwd
# recursive chown is too slow, take COPY --chown=$UID:$GID instead, but /home/coder is indetified as home/coder, tell me why??
# COPY --chown=$UID:$GID /home/coder/.cargo .cargoo
# COPY --chown=$UID:$GID /home/coder/.rustup .rustupp

## The USER instruction sets the user name (or UID) and optionally the user group (or GID) to use when running the image
## and for any RUN, CMD and ENTRYPOINT instructions that follow it in the Dockerfile
## from https://docs.docker.com/engine/reference/builder/#user

## We have to install extensions as host UID:GID so the code-server can only identify the extensions when we start
## the container by forwarding host UID/GID later.
USER $UID:$GID
## Because of taking user by $UID:$GID, container can't identify the HOME(~) variable, so we need to
## declare HOME explicitely, or else hit err "info  Wrote default config file to ~/.config/code-server/config.yaml"
RUN HOME=/home/coder code-server \
	--user-data-dir=/home/coder/.local/share/code-server \
	--install-extension ms-python.python \
	--install-extension formulahendry.code-runner \
	--install-extension eamodio.gitlens \
	--install-extension oderwat.indent-rainbow \
	--install-extension vscode-icons-team.vscode-icons \
	--install-extension esbenp.prettier-vscode \
	--install-extension streetsidesoftware.code-spell-checker \
	--install-extension kdarkhan.mips \
	--install-extension dan-c-underwood.arm \
	--install-extension yzhang.markdown-all-in-one \
	--install-extension eamodio.gitlens \
	--install-extension maelvalais.autoconf \
	--install-extension dan-c-underwood.arm \
	--install-extension rust-lang.rust-analyzer \
	--install-extension tamasfe.even-better-toml \
	--install-extension usernamehw.errorlens \
	--install-extension zhuangtongfa.Material-theme \
	--install-extension vadimcn.vscode-lldb \
	--install-extension plorefice.devicetree \
	--install-extension tomoki1207.pdf \
	--install-extension webfreak.debug \
	--install-extension ms-vscode.cpptools.vsix \
	--install-extension EugenWiens.bitbake.vsix \
	--install-extension whiteout2.arm64.vsix \
	--install-extension slevesque.vscode-hexdump.vsix \
	--install-extension walonli.edk2-vscode.vsix

###	--install-extension ms-vscode.cpptools.Microsoft \
###	--install-extension EugenWiens.bitbake \
###	--install-extension whiteout2.arm64 \
###	--install-extension slevesque.vscode-hexdump \
###	--install-extension walonli.edk2-vscode

##	--install-extension ms-vscode.cpptools@linux-x64.vsix \
##	--install-extension EugenWiens.bitbake.vsix \
##	--install-extension whiteout2.arm64.vsix \
##	--install-extension slevesque.vscode-hexdump.vsix \
##	--install-extension walonli.edk2-vscode.vsix \

RUN rm -f *.vsix && rm -rf /home/coder/.local/share/code-server/CachedExtensionVSIXs

## The user and group will be root and the setting won't go into effect before changing user:group to $UID:$GID or changing
## the file mode bits to 777.
# COPY settings.json /home/$USER/.local/share/code-server/User/settings.json
# COPY keybindings.json /home/$USER/.local/share/code-server/User/keybindings.json

COPY --chown=$UID:$GID settings.json /home/coder/.local/share/code-server/User/settings.json
COPY --chown=$UID:$GID keybindings.json /home/coder/.local/share/code-server/User/keybindings.json
# COPY --chown=4089805:200 settings.json /home/coder/.local/share/code-server/User/settings.json
# COPY --chown=4089805:200 keybindings.json /home/coder/.local/share/code-server/User/keybindings.json

# The chown or chmod executing time will be long ...
# RUN chmod 777 -R /home/coder/.local/share/code-server/User && chown 4089805:200 -R /home/coder/.local/share/code-server/extensions
# RUN chown 4089805:200 -R /home/coder/.local/share/code-server/extensions
# RUN chown $UID:$GID -R /home/coder/.local/share/code-server/extensions

## Don't need to overwrite entrypoint.sh any more since we change user and group to host at building time.
# COPY entrypoint.sh /usr/bin/entrypoint.sh

# Allow user Entrypoint scripts #5194 https://github.com/coder/code-server/pull/5194
# ENV ENTRYPOINTD=${HOME}/entrypoint.d

