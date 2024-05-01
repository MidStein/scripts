#!/usr/bin/env bash
if [[ $(nmcli radio wifi) == 'disabled' ]]; then
  nmcli radio wifi on
else
  nmcli radio wifi off
fi
