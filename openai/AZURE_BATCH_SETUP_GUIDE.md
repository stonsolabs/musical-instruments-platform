# Azure OpenAI Batch Processing Setup Guide

Based on [Microsoft Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/batch-blob-storage?tabs=python)

## 🎯 **Key Changes Made**

### ✅ **Fixed Batch File Format**
- **URL**: Changed from `/v1/chat/completions` to `/chat/completions`
- **Model**: Uses your deployment name `gpt-4.1`
- **Token Limit**: Reduced to 4000 (reasonable for batch)
- **Prompt Length**: Shortened to 1224 characters

### ✅ **New Azure Blob Storage Approach**
- Uses Azure Blob Storage instead of direct file upload
- Requires managed identity setup
- More reliable and scalable

## 📋 **Prerequisites**

### 1. Azure OpenAI Resource
- ✅ **Endpoint**: `https://getyourmusicgear.openai.azure.com/`
- ✅ **Model Deployment**: `gpt-4.1` (Global-Batch or DataZoneBatch type)
- ✅ **API Version**: `2025-04-01-preview`

### 2. Azure Blob Storage Account
- Create a new Azure Blob Storage account
- Note the storage account name

### 3. Required Containers
Create these containers in your Azure Blob Storage:
- `batch-input` - For input files
- `batch-output` - For output files

## 🔧 **Setup Steps**

### Step 1: Configure Managed Identity

1. Go to [Azure Portal](https://portal.azure.com)
2. Find your Azure OpenAI resource
3. Select **Resource Management** > **Identity** > **System assigned**
4. Set status to **On**
5. Save the changes

### Step 2: Configure Role-Based Access Control

1. Go to your Azure Blob Storage resource
2. Select **Access Control (IAM)** > **Add** > **Add role assignment**
3. Search for **Storage Blob Data Contributor** > **Next**
4. Select **Managed identity** > **+Select members**
5. Select your Azure OpenAI resource's managed identity
6. Complete the assignment

### Step 3: Upload Batch File

1. Upload `batch_files/azure_batch_30_products_20250828_210852.jsonl` to your `batch-input` container
2. Note the exact file name for the script

### Step 4: Update Configuration

Edit `submit_azure_batch_20250828_210852.py` and update these values:

```python
# Configuration - UPDATE THESE VALUES
AZURE_OPENAI_ENDPOINT = "https://getyourmusicgear.openai.azure.com/"  # Your endpoint
STORAGE_ACCOUNT_NAME = "your-storage-account-name"  # Your Azure Blob Storage account
BATCH_INPUT_CONTAINER = "batch-input"
BATCH_OUTPUT_CONTAINER = "batch-output"
BATCH_FILE_NAME = "azure_batch_30_products_20250828_210852.jsonl"  # Your batch file
```

### Step 5: Install Dependencies

```bash
pip install openai azure-identity azure-storage-blob
```

### Step 6: Set Environment Variables

```bash
export AZURE_OPENAI_ENDPOINT="https://getyourmusicgear.openai.azure.com/"
```

### Step 7: Run the Batch Job

```bash
python3 submit_azure_batch_20250828_210852.py
```

## 📊 **Monitoring**

The script will automatically monitor the batch job and show:
- **Status updates** every minute
- **Progress**: completed/total requests
- **Final results**: output and error file locations

## 🔍 **Troubleshooting**

### Common Issues

1. **400 Error - Invalid Format**
   - ✅ **Fixed**: Using correct URL format `/chat/completions`
   - ✅ **Fixed**: Using correct deployment name
   - ✅ **Fixed**: Reasonable token limits

2. **Authentication Errors**
   - Ensure managed identity is enabled
   - Verify role assignments
   - Check Azure CLI login: `az login`

3. **Storage Access Errors**
   - Verify container names match
   - Check file exists in batch-input container
   - Ensure Storage Blob Data Contributor role is assigned

### Error Codes

- **400**: Bad request (format issues) - ✅ **Fixed**
- **401**: Authentication failed
- **403**: Access denied (role issues)
- **404**: File not found (storage issues)

## 📁 **File Structure**

```
openai/
├── batch_files/
│   └── azure_batch_30_products_20250828_210852.jsonl  # ✅ Corrected batch file
├── submit_azure_batch_20250828_210852.py              # ✅ Submission script
├── create_azure_batch.py                              # ✅ Batch file generator
└── AZURE_BATCH_SETUP_GUIDE.md                        # ✅ This guide
```

## 🎉 **Expected Results**

After successful completion:
- **Output file**: `https://{storage-account}.blob.core.windows.net/batch-output/{GUID}/results.jsonl`
- **Error file**: `https://{storage-account}.blob.core.windows.net/batch-output/{GUID}/errors.jsonl` (if any errors)

## 📞 **Support**

If you encounter issues:
1. Check the [Microsoft documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/batch-blob-storage?tabs=python)
2. Verify all prerequisites are met
3. Check Azure portal for detailed error messages

---

**✅ Your batch processing pipeline is now properly configured for Azure OpenAI!** 🎸
