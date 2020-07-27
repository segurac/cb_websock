#!/bin/bash

ps aux | grep launch_db | grep -v grep | awk '{print $2}' | xargs kill
:
