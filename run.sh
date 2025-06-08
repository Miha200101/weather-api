#!/bin/bash

# Schimbă directorul în locația scriptului
cd "$(dirname "$0")"

# Activează mediul virtual
source venv/bin/activate

# Rulează aplicația Flask
python3 main.py

