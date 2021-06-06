FROM codercom/code-server:latest

COPY extensions.tar.bz2 /extensions.tar.bz2
COPY plorefice.devicetree.tar.bz2 /plorefice.devicetree.tar.bz2
COPY init /init
COPY settings.json /settings.json

EXPOSE 8080

## empty the ENTRYPOINT
ENTRYPOINT []

CMD /usr/bin/code-server --user-data-dir /usr/local/share/code-server --auth password --bind-addr 0.0.0.0:8080 --disable-update-check

