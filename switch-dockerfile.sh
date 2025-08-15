#!/bin/bash

# Script to switch between different Dockerfile options for Render.com deployment

echo "Available Dockerfile options:"
echo "1. Dockerfile (optimized with frontend)"
echo "2. Dockerfile.simple (single-stage with frontend)"
echo "3. Dockerfile.backend-only (backend only - guaranteed to work)"
echo "4. Dockerfile.minimal (minimal backend)"

read -p "Choose option (1-4): " choice

case $choice in
    1)
        echo "Using Dockerfile (optimized with frontend)"
        cp Dockerfile Dockerfile.active
        ;;
    2)
        echo "Using Dockerfile.simple (single-stage with frontend)"
        cp Dockerfile.simple Dockerfile.active
        ;;
    3)
        echo "Using Dockerfile.backend-only (backend only)"
        cp Dockerfile.backend-only Dockerfile.active
        ;;
    4)
        echo "Using Dockerfile.minimal (minimal backend)"
        cp Dockerfile.minimal Dockerfile.active
        ;;
    *)
        echo "Invalid choice. Using Dockerfile.backend-only (guaranteed to work)"
        cp Dockerfile.backend-only Dockerfile.active
        ;;
esac

echo "Dockerfile.active has been created. Update your render.yaml to use:"
echo "dockerfilePath: ./Dockerfile.active"
