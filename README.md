# jgsun's code-server docker image

From codercom/code-server:latest, add:
* apt -y install build-essential gdb gcc wget mercurial
* Favorite extensions: cpptools-linux, ms-python.python, plorefice.devicetree, ms-python.python, etc.
* Favorite settings.json and keybinding.json

## build

    docker build -t jgsun/code-server:latest  .

## run

    ./vscode start [u=root or $USER] [p=10086]
    Default user is $USER, if want to start by root, add parameter u=root.

## login

    ./vscode login

## stop

    ./vscode stop
