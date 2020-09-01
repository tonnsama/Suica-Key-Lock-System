#!/bin/bash
KEY_DIR_PATH=$(dirname "$(cd "$(dirname "${BASH_SOURCE:-$0}")" && pwd)")
python $KEY_DIR_PATH/main.py
