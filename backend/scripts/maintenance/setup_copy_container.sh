#!/bin/bash

# Setup script for container copy configuration
echo "🔧 Setting up container copy configuration"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "config.py" ]; then
    echo "❌ config.py not found! Please run this from the maintenance directory."
    exit 1
fi

# Test configuration
echo "🔧 Testing configuration..."
python3.11 -c "from config import print_config; print_config()"
if [ $? -ne 0 ]; then
    echo "❌ Configuration test failed!"
    exit 1
fi

# Get current configuration from config module
echo "📋 Current Configuration from .env files:"
SOURCE_ACCOUNT=$(python3.11 -c "from config import AZURE_STORAGE_ACCOUNT; print(AZURE_STORAGE_ACCOUNT)")
SOURCE_CONTAINER=$(python3.11 -c "from config import AZURE_STORAGE_CONTAINER; print(AZURE_STORAGE_CONTAINER)")

echo "   Source Account: $SOURCE_ACCOUNT"
echo "   Source Container: $SOURCE_CONTAINER"

# Set destination defaults
if [ -z "$DEST_ACCOUNT" ]; then
    export DEST_ACCOUNT="$SOURCE_ACCOUNT"
    echo "⚠️  DEST_ACCOUNT not set, using source account: $DEST_ACCOUNT"
else
    echo "✅ DEST_ACCOUNT set to: $DEST_ACCOUNT"
fi

if [ -z "$DEST_CONTAINER" ]; then
    export DEST_CONTAINER="product-images-backup"
    echo "✅ DEST_CONTAINER set to: $DEST_CONTAINER"
else
    echo "✅ DEST_CONTAINER set to: $DEST_CONTAINER"
fi

echo ""
echo "📋 Current Configuration:"
echo "   Source: $SOURCE_ACCOUNT/$SOURCE_CONTAINER"
echo "   Destination: $DEST_ACCOUNT/$DEST_CONTAINER"
echo ""

# Check if Azure CLI is available
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI not found! Please install it first:"
    echo "   https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
else
    echo "✅ Azure CLI found"
fi

# Check if azcopy is available (optional)
if command -v azcopy &> /dev/null; then
    echo "✅ azcopy found (will be used as fallback)"
else
    echo "⚠️  azcopy not found (only Azure CLI copy will be used)"
    echo "   Install azcopy for better performance: https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10"
fi

# Check Azure login
echo ""
echo "🔐 Checking Azure authentication..."
az account show &> /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Azure CLI authenticated"
    echo "   Current account: $(az account show --query 'name' -o tsv)"
else
    echo "❌ Azure CLI not authenticated. Please login:"
    echo "   az login"
    exit 1
fi

echo ""
echo "🚀 Ready to run the container copy script!"
echo "Run: python3.11 copy_images_to_container.py"
echo ""
echo "💡 To customize settings, set these environment variables:"
echo "export SOURCE_ACCOUNT='your-source-account'"
echo "export SOURCE_CONTAINER='your-source-container'"
echo "export DEST_ACCOUNT='your-destination-account'"
echo "export DEST_CONTAINER='your-destination-container'"
echo ""
echo "⚠️  WARNING: This will copy ALL images from the database to the destination container!"
echo "   Make sure you have sufficient storage and permissions."
