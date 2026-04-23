#!/bin/bash

journalctl -b | grep suspend | tail -n 20
