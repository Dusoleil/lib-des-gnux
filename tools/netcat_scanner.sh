#!/bin/sh
nc -v -n -z -w1 "$1" 1-65535
