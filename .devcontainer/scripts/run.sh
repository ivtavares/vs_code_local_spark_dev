#! /bin/bash
if ! test -f /usr/local/bin/pip; then ln -s /usr/local/bin/pip3 /usr/local/bin/pip; fi
pip3 install poetry
poetry install --with=dev