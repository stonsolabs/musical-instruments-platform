#!/usr/bin/env node

// Test script to verify API connectivity
const https = require('https');
const http = require('http');

// Configuration - Update these with your actual URLs
const BACKEND_URL = process.env.BACKEND_URL || 'https://musical-instruments-platform.onrender.com';
const API_KEY = process.env.API_KEY || 'your-api-key-here';

console.log('🔍 Testing API Connectivity...\n');

// Test 1: Health check (no API key required)
async function testHealthCheck() {
  console.log('1. Testing health check endpoint...');
  try {
    const response = await fetch(`${BACKEND_URL}/health`);
    if (response.ok) {
      const data = await response.json();
      console.log('✅ Health check passed:', data);
    } else {
      console.log('❌ Health check failed:', response.status, response.statusText);
    }
  } catch (error) {
    console.log('❌ Health check error:', error.message);
  }
}

// Test 2: API endpoint with API key
async function testAPIEndpoint() {
  console.log('\n2. Testing API endpoint with API key...');
  try {
    const response = await fetch(`${BACKEND_URL}/api/v1/products?limit=1`, {
      headers: {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json',
      },
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('✅ API endpoint passed:', {
        status: response.status,
        productsCount: data.products?.length || 0,
        pagination: data.pagination
      });
    } else {
      console.log('❌ API endpoint failed:', response.status, response.statusText);
      const errorText = await response.text();
      console.log('Error details:', errorText);
    }
  } catch (error) {
    console.log('❌ API endpoint error:', error.message);
  }
}

// Test 3: Test without API key (should fail)
async function testWithoutAPIKey() {
  console.log('\n3. Testing API endpoint without API key (should fail)...');
  try {
    const response = await fetch(`${BACKEND_URL}/api/v1/products?limit=1`, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (response.status === 401) {
      console.log('✅ Correctly rejected request without API key');
    } else {
      console.log('❌ Unexpected response:', response.status, response.statusText);
    }
  } catch (error) {
    console.log('❌ Test error:', error.message);
  }
}

// Test 4: Test CORS headers
async function testCORS() {
  console.log('\n4. Testing CORS headers...');
  try {
    const response = await fetch(`${BACKEND_URL}/health`, {
      method: 'OPTIONS',
      headers: {
        'Origin': 'https://getyourmusicgear.vercel.app',
        'Access-Control-Request-Method': 'GET',
        'Access-Control-Request-Headers': 'Content-Type',
      },
    });
    
    const corsHeaders = {
      'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
      'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
      'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
    };
    
    console.log('✅ CORS headers:', corsHeaders);
  } catch (error) {
    console.log('❌ CORS test error:', error.message);
  }
}

// Run all tests
async function runTests() {
  await testHealthCheck();
  await testAPIEndpoint();
  await testWithoutAPIKey();
  await testCORS();
  
  console.log('\n🎯 Test Summary:');
  console.log('- If health check passes: Backend is running');
  console.log('- If API endpoint passes: API key is correct');
  console.log('- If CORS test passes: Frontend can communicate');
  console.log('- If you see errors, check your environment variables and backend configuration');
}

runTests().catch(console.error);
