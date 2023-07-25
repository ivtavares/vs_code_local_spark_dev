#!/bin/bash
if ! test -f /usr/bin/pip; then ln -s /usr/bin/pip3 /usr/bin/pip; fi
cp /workspace/.devcontainer/scripts/.bashrc ~/.bashrc
/usr/bin/pip3 install -r /workspace/requirements.txt