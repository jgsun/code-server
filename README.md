# jgsun's code-server docker image

From codercom/code-server:latest, https://github.com/coder/code-server
Add:
* apt -y install build-essential gdb gcc wget mercurial
* Favorite extensions: cpptools-linux, ms-python.python, plorefice.devicetree, ms-python.python, etc.
* Favorite settings.json and keybinding.json


## build
    git clone https://github.com/jgsun/code-server
    cd code-server`
    docker build --build-arg UID=$(id -u) --build-arg GID=$(id -g) -t jgsun/code-server:latest .

## run
    Change PROJECT_CFG_PATH in vscode to the path of this repo and run:
    ./vscode start [u=root] [p=10086]
    Default user is $USER, if want to start by root, add parameter u=root.
    Recommend taking $USER to let all file system operations occur as your user outside the container

## login
    ./vscode login

## stop
    ./vscode stop
