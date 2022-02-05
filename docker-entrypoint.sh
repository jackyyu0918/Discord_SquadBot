#!/bin/sh

nohup python ./app/SquadBot.py > output.log &

while true; do sleep 10000; done