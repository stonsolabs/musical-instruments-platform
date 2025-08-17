#!/bin/bash

# Vercel Environment Variables Setup Script
# This script helps you set up the required environment variables for your Vercel deployment

echo "🎵 Musical Instruments Platform - Vercel Environment Setup"
echo "=========================================================="
echo ""

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI is not installed. Please install it first:"
    echo "   npm install -g vercel"
    echo ""
    exit 1
fi

echo "📋 Required Environment Variables:"
echo ""

# Backend API URL
echo "1. NEXT_PUBLIC_API_BASE_URL"
echo "   Description: Your backend API URL (Render app)"
echo "   Example: https://musical-instruments-platform.onrender.com"
echo "   Current value: $(vercel env ls | grep NEXT_PUBLIC_API_BASE_URL | awk '{print $3}' || echo 'Not set')"
echo ""

# API Key
echo "2. API_KEY"
echo "   Description: API key for backend authentication (server-side only)"
echo "   Example: your-api-key-here"
echo "   Current value: $(vercel env ls | grep API_KEY | awk '{print $3}' || echo 'Not set')"
echo ""

# GTM ID
echo "3. NEXT_PUBLIC_GTM_ID"
echo "   Description: Google Tag Manager ID (optional)"
echo "   Example: GTM-XXXXXXX"
echo "   Current value: $(vercel env ls | grep NEXT_PUBLIC_GTM_ID | awk '{print $3}' || echo 'Not set')"
echo ""

# Domain
echo "4. NEXT_PUBLIC_DOMAIN"
echo "   Description: Your domain name"
echo "   Example: getyourmusicgear.com"
echo "   Current value: $(vercel env ls | grep NEXT_PUBLIC_DOMAIN | awk '{print $3}' || echo 'Not set')"
echo ""

echo "🔧 To set these variables, run the following commands:"
echo ""

echo "# Set Backend API URL"
echo "vercel env add NEXT_PUBLIC_API_BASE_URL"
echo ""

echo "# Set API Key"
echo "vercel env add API_KEY"
echo ""

echo "# Set GTM ID (optional)"
echo "vercel env add NEXT_PUBLIC_GTM_ID"
echo ""

echo "# Set Domain"
echo "vercel env add NEXT_PUBLIC_DOMAIN"
echo ""

echo "📝 Or you can set them all at once by copying from env-templates/vercel-env-vars.txt"
echo ""

echo "🚀 After setting the variables, redeploy your app:"
echo "vercel --prod"
echo ""

echo "✅ Make sure your backend is running and accessible at the API_BASE_URL"
echo "✅ Verify that your API_KEY matches the one in your backend configuration"
