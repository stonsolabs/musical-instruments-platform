#!/bin/bash

# Domain Testing Script - Test Cloudflare + Vercel + Render setup

set -e

DOMAIN="getyourmusicgear.com"
API_DOMAIN="api.getyourmusicgear.com"

echo "🌐 Testing Domain Setup for Musical Instruments Platform"
echo "   Main: $DOMAIN"
echo "   API: $API_DOMAIN"
echo ""

# Test 1: DNS Resolution
echo "🔍 Testing DNS resolution..."
echo "   Main domain:"
dig +short $DOMAIN || echo "❌ DNS resolution failed for $DOMAIN"

echo "   WWW subdomain:"
dig +short www.$DOMAIN || echo "❌ DNS resolution failed for www.$DOMAIN"

echo "   API subdomain:"
dig +short $API_DOMAIN || echo "❌ DNS resolution failed for $API_DOMAIN"

echo ""

# Test 2: HTTP/HTTPS Response
echo "🌐 Testing HTTP responses..."

echo "   Main domain HTTPS:"
if curl -s -o /dev/null -w "%{http_code}" https://$DOMAIN | grep -q "200\|301\|302"; then
    echo "✅ Main domain responds"
else
    echo "❌ Main domain not responding"
fi

echo "   WWW subdomain HTTPS:"
if curl -s -o /dev/null -w "%{http_code}" https://www.$DOMAIN | grep -q "200\|301\|302"; then
    echo "✅ WWW subdomain responds"
else
    echo "❌ WWW subdomain not responding"
fi

echo "   API subdomain HTTPS:"
if curl -s -o /dev/null -w "%{http_code}" https://$API_DOMAIN/health | grep -q "200"; then
    echo "✅ API subdomain responds"
else
    echo "❌ API subdomain not responding"
fi

echo ""

# Test 3: SSL Certificates
echo "🔒 Testing SSL certificates..."

echo "   Main domain SSL:"
if openssl s_client -connect $DOMAIN:443 -servername $DOMAIN </dev/null 2>/dev/null | grep -q "Verify return code: 0"; then
    echo "✅ SSL certificate valid for main domain"
else
    echo "❌ SSL certificate issue for main domain"
fi

echo "   API subdomain SSL:"
if openssl s_client -connect $API_DOMAIN:443 -servername $API_DOMAIN </dev/null 2>/dev/null | grep -q "Verify return code: 0"; then
    echo "✅ SSL certificate valid for API domain"
else
    echo "❌ SSL certificate issue for API domain"
fi

echo ""

# Test 4: CORS Configuration
echo "🔄 Testing CORS configuration..."
CORS_RESPONSE=$(curl -s -H "Origin: https://$DOMAIN" \
     -H "Access-Control-Request-Method: GET" \
     -X OPTIONS \
     https://$API_DOMAIN/api/v1/products 2>/dev/null | head -1)

if echo "$CORS_RESPONSE" | grep -q "200\|204"; then
    echo "✅ CORS configured correctly"
else
    echo "❌ CORS configuration issue"
fi

echo ""

# Test 5: Frontend-Backend Connectivity
echo "🔗 Testing frontend-backend connectivity..."

# Check if frontend health endpoint can reach backend
HEALTH_RESPONSE=$(curl -s https://$DOMAIN/api/health 2>/dev/null || echo "failed")
if echo "$HEALTH_RESPONSE" | grep -q '"status":"healthy"'; then
    echo "✅ Frontend can reach backend"
    
    BACKEND_STATUS=$(echo "$HEALTH_RESPONSE" | grep -o '"backend":{"url":"[^"]*","status":"[^"]*"}' | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
    echo "   Backend status: $BACKEND_STATUS"
else
    echo "❌ Frontend cannot reach backend"
fi

echo ""

# Test 6: Performance Check
echo "⚡ Testing performance..."

MAIN_TIME=$(curl -o /dev/null -s -w "%{time_total}" https://$DOMAIN/ 2>/dev/null || echo "failed")
API_TIME=$(curl -o /dev/null -s -w "%{time_total}" https://$API_DOMAIN/health 2>/dev/null || echo "failed")

echo "   Main domain response time: ${MAIN_TIME}s"
echo "   API response time: ${API_TIME}s"

# Performance recommendations
if (( $(echo "$MAIN_TIME > 2.0" | bc -l 2>/dev/null || echo "0") )); then
    echo "⚠️  Main domain is slow (>2s)"
fi

if (( $(echo "$API_TIME > 1.0" | bc -l 2>/dev/null || echo "0") )); then
    echo "⚠️  API is slow (>1s)"
fi

echo ""

# Test 7: SEO Check
echo "🔍 Testing SEO (Server-Side Rendering)..."
SSR_RESPONSE=$(curl -s -H "User-Agent: Googlebot" https://$DOMAIN/products 2>/dev/null || echo "failed")

if echo "$SSR_RESPONSE" | grep -q "<title>"; then
    echo "✅ Server-side rendering working (title tag found)"
else
    echo "❌ Server-side rendering issue (no title tag)"
fi

if echo "$SSR_RESPONSE" | grep -q 'meta.*description'; then
    echo "✅ Meta description found"
else
    echo "❌ Meta description missing"
fi

echo ""
echo "🎉 Domain testing complete!"
echo ""
echo "💡 Next steps if issues found:"
echo "   - Check Cloudflare DNS settings"
echo "   - Verify Vercel domain configuration"
echo "   - Check Render environment variables"
echo "   - Wait for DNS propagation (up to 48h)"
echo "   - Review CORS settings in backend"
