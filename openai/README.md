# Azure OpenAI Batch Processing

This is the official folder for Azure OpenAI batch processing of musical instrument products.

## 📁 **Files Overview**

### 🚀 **Core Batch Processing**
- `create_azure_batch.py` - Generate batch files in correct Azure OpenAI format
- `submit_azure_batch_20250828_210852.py` - Submit batch jobs to Azure OpenAI
- `AZURE_BATCH_SETUP_GUIDE.md` - Complete setup and troubleshooting guide

### 📊 **Data Processing**
- `database.py` - Database connection and models
- `config.py` - Configuration settings
- `process_results.py` - Process batch results and insert into database
- `products_filled_parser.py` - Parse AI-generated content
- `get_config_from_db.py` - Retrieve prompt/schema from database

### 📁 **Batch Files**
- `batch_files/` - Contains generated batch files for Azure OpenAI

### 📋 **Dependencies**
- `requirements.txt` - Python dependencies
- `.env` - Environment configuration

## 🚀 **Quick Start**

### 1. **Generate Batch File**
```bash
python3 create_azure_batch.py 30
```

### 2. **Follow Setup Guide**
Read `AZURE_BATCH_SETUP_GUIDE.md` for complete setup instructions.

### 3. **Submit Batch Job**
```bash
python3 submit_azure_batch_20250828_210852.py
```

### 4. **Process Results**
```bash
python3 process_results.py <results_file>
```

## 📋 **Prerequisites**

1. **Azure OpenAI Resource** with `gpt-4.1` deployment
2. **Azure Blob Storage** account with containers
3. **Managed Identity** configured
4. **Python Dependencies**: `pip install -r requirements.txt`

## 🎯 **Key Features**

- ✅ **Correct Azure OpenAI format** (URL: `/chat/completions`)
- ✅ **Azure Blob Storage integration**
- ✅ **Managed identity authentication**
- ✅ **Automatic monitoring and progress tracking**
- ✅ **Database integration for results processing**
- ✅ **Database configuration retrieval** (prompt/schema from `config_files` table)

## 📞 **Support**

For detailed setup instructions and troubleshooting, see `AZURE_BATCH_SETUP_GUIDE.md`.

---

**✅ Official Azure OpenAI batch processing folder!** 🎸
