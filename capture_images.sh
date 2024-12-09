#!/bin/bash

# Define the directory and filename
DIRECTORY="/home/admin/Desktop/test_pic"
FILENAME="image.jpg"

# Create the directory if it does not exist
mkdir -p "$DIRECTORY"

# Infinite loop to capture an image every second
while true; do
    # Capture the image and overwrite the previous one
    libcamera-still -o "$DIRECTORY/$FILENAME" --width 1280 --height 720 -n

    # Avoid overloading and harming SD
    sleep 0.1
done