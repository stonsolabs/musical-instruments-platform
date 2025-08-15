#!/bin/bash

echo "🚀 Musical Instruments Platform - Simple Deployment"
echo "=================================================="
echo ""
echo "Choose deployment option:"
echo "1. Backend Only (Recommended first)"
echo "2. Full Stack (After backend works)"
echo "3. View current config"
echo ""

read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo "📦 Setting up Backend Only deployment..."
        cp render-backend-only.yaml render.yaml
        echo "✅ Updated render.yaml to use backend-only configuration"
        echo "📝 Dockerfile: ./Dockerfile.simple-backend"
        echo ""
        echo "Next steps:"
        echo "git add ."
        echo "git commit -m 'Deploy backend only'"
        echo "git push"
        ;;
    2)
        echo "📦 Setting up Full Stack deployment..."
        cp render-fullstack.yaml render.yaml
        echo "✅ Updated render.yaml to use full-stack configuration"
        echo "📝 Dockerfile: ./Dockerfile.simple-fullstack"
        echo ""
        echo "Next steps:"
        echo "git add ."
        echo "git commit -m 'Deploy full stack'"
        echo "git push"
        ;;
    3)
        echo "📋 Current render.yaml configuration:"
        echo "=================================="
        cat render.yaml
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "🔗 After deployment, test your app:"
echo "curl https://your-app.onrender.com/health"
echo "curl https://your-app.onrender.com/api/v1/products"
