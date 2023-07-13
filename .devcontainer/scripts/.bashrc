export PATH="/usr/bin/:$PATH"
# export PYTHONPATH="/workspace:$PYTHONPATH"
if ! test -f /usr/bin/pip; then ln -s /usr/bin/pip3 /usr/bin/pip; fi