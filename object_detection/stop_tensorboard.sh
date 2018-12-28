#!/bin/bash

if [ -e '/tmp/tfb.run' ]; then
    kill -9 `cat /tmp/tfb.run`
    rm -rf /tmp/tfb.run
fi
echo "Stop Tensorboard."