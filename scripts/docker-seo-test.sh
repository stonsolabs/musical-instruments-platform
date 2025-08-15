#!/bin/bash

# SEO Testing Script - Test server-side rendering and SEO features

set -e

echo "🔍 SEO Testing for Musical Instruments Platform"
echo ""

# Check if services are running
if ! curl -s http://localhost:3000/api/health > /dev/null; then
    echo "❌ Frontend is not running. Please start with:"
    echo "   ./scripts/docker-dev.sh or ./scripts/docker-prod-test.sh"
    exit 1
fi

if ! curl -s http://localhost:8000/health > /dev/null && ! curl -s http://localhost:10000/health > /dev/null; then
    echo "❌ Backend is not running. Please start with:"
    echo "   ./scripts/docker-dev.sh or ./scripts/docker-prod-test.sh"
    exit 1
fi

# Determine backend port
BACKEND_PORT=8000
if curl -s http://localhost:10000/health > /dev/null; then
    BACKEND_PORT=10000
fi

echo "✅ Services are running!"
echo "   Frontend: http://localhost:3000"
echo "   Backend: http://localhost:$BACKEND_PORT"
echo ""

# Test 1: Homepage SSR
echo "🏠 Testing homepage server-side rendering..."
HOMEPAGE_RESPONSE=$(curl -s -H "User-Agent: Googlebot" http://localhost:3000/)
if echo "$HOMEPAGE_RESPONSE" | grep -q "<title>"; then
    echo "✅ Homepage has title tag"
else
    echo "❌ Homepage missing title tag"
fi

if echo "$HOMEPAGE_RESPONSE" | grep -q 'meta.*description'; then
    echo "✅ Homepage has meta description"
else
    echo "❌ Homepage missing meta description"
fi

# Test 2: Products page SSR
echo ""
echo "🎸 Testing products page server-side rendering..."
PRODUCTS_RESPONSE=$(curl -s -H "User-Agent: Googlebot" http://localhost:3000/products)
if echo "$PRODUCTS_RESPONSE" | grep -q "<title>"; then
    echo "✅ Products page has title tag"
else
    echo "❌ Products page missing title tag"
fi

# Test 3: API connectivity from frontend
echo ""
echo "🔗 Testing API connectivity..."
HEALTH_RESPONSE=$(curl -s http://localhost:3000/api/health)
if echo "$HEALTH_RESPONSE" | grep -q '"status":"healthy"'; then
    echo "✅ Frontend health check passes"
    
    BACKEND_STATUS=$(echo "$HEALTH_RESPONSE" | grep -o '"backend":{"url":"[^"]*","status":"[^"]*"}' | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
    if [ "$BACKEND_STATUS" = "healthy" ]; then
        echo "✅ Backend connectivity from frontend: $BACKEND_STATUS"
    else
        echo "⚠️  Backend connectivity from frontend: $BACKEND_STATUS"
    fi
else
    echo "❌ Frontend health check fails"
fi

# Test 4: Backend API directly
echo ""
echo "🔧 Testing backend API directly..."
BACKEND_HEALTH=$(curl -s http://localhost:$BACKEND_PORT/health)
if echo "$BACKEND_HEALTH" | grep -q '"status":"healthy"'; then
    echo "✅ Backend API health check passes"
else
    echo "❌ Backend API health check fails"
fi

# Test 5: Check for hydration (client-side JavaScript)
echo ""
echo "🌊 Testing client-side hydration..."
if echo "$HOMEPAGE_RESPONSE" | grep -q '_next/static'; then
    echo "✅ Next.js static assets found (hydration enabled)"
else
    echo "❌ Next.js static assets missing"
fi

# Test 6: Response time
echo ""
echo "⏱️  Testing response times..."
FRONTEND_TIME=$(curl -o /dev/null -s -w "%{time_total}" http://localhost:3000/)
BACKEND_TIME=$(curl -o /dev/null -s -w "%{time_total}" http://localhost:$BACKEND_PORT/health)

echo "   Frontend response time: ${FRONTEND_TIME}s"
echo "   Backend response time: ${BACKEND_TIME}s"

if (( $(echo "$FRONTEND_TIME < 2.0" | bc -l) )); then
    echo "✅ Frontend response time is good"
else
    echo "⚠️  Frontend response time is slow"
fi

echo ""
echo "🎉 SEO testing complete!"
echo ""
echo "💡 Tips for better SEO:"
echo "   - Ensure all product pages render server-side"
echo "   - Add structured data (JSON-LD) for products"
echo "   - Optimize images with proper alt tags"
echo "   - Generate XML sitemap"
echo "   - Add Open Graph and Twitter Card meta tags"
