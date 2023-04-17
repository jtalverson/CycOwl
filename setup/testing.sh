#!/bin/bash

sudo sed -n 's/%sudo	ALL=(ALL:ALL) ALL/%sudo	ALL=(ALL:ALL) NOPASSWD: ALL/' ./testSudo
