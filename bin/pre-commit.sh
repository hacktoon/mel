#!/bin/bash

make lint
retval=$?
if [ $retval -ne 0 ]; then
    echo "Code guidelines problems. Fix them before commiting."
fi

exit $retval
