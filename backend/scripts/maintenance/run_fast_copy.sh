#!/bin/bash

# Fast Threaded Copy Script
echo "🚀 FAST THREADED IMAGE COPY"
echo "============================"

# Set destination container
export DEST_CONTAINER="product-images-correct"

# Configure threading - much more aggressive for speed
export MAX_WORKERS=100  # Increased to 100 threads for maximum speed

echo "📊 Configuration:"
echo "   Destination: $DEST_CONTAINER"
echo "   Threads: $MAX_WORKERS"
echo ""

# Run the threaded copy

echo "🚀 Starting fast copy with $MAX_WORKERS threads..."
python3.11 copy_images_to_container.py

echo ""
echo "✅ Copy operation completed!"
echo "📊 Check results in the generated log files"
