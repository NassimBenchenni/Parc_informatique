#!/bin/bash
host=$(hostname)

epo=$(date +%s)
val=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
quoi="DISQUE"

echo "$quoi;$host;$epo;$val"
