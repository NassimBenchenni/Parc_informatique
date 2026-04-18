#!/bin/bash
host=$(hostname)

epo=$(date +%s)
val=$(ps -e | wc -l)
quoi="PROCESSUS"

echo "$quoi;$host;$epo;$val"