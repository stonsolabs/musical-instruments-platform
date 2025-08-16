#!/usr/bin/env node

const crypto = require('crypto');

// Generate a secure API key
const apiKey = crypto.randomBytes(32).toString('hex');

console.log('🔑 Generated API Key:');
console.log('='.repeat(50));
console.log(apiKey);
console.log('='.repeat(50));

console.log('\n📋 Next Steps:');
console.log('1. Copy this API key');
console.log('2. Set it in your Render backend environment variables as API_KEY');
console.log('3. Set it in your Vercel frontend environment variables as API_KEY');
console.log('4. Deploy both services');
console.log('5. Test the connection with: node test-api-connection.js');

console.log('\n⚠️  Security Notes:');
console.log('- Keep this key secret and secure');
console.log('- Never commit it to version control');
console.log('- Use different keys for development and production');
console.log('- Rotate the key periodically for security');

console.log('\n🔧 Environment Variables to Set:');
console.log('\nRender Backend:');
console.log(`API_KEY=${apiKey}`);

console.log('\nVercel Frontend:');
console.log(`API_KEY=${apiKey}`);
console.log('NEXT_PUBLIC_API_BASE_URL=https://musical-instruments-platform.onrender.com');
