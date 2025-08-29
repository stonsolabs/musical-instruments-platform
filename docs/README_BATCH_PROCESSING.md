# Azure OpenAI Batch Processing System

This document describes the Azure OpenAI batch processing system for generating AI content for musical instrument products.

## Overview

The batch processing system allows you to:
- Generate comprehensive AI content for products using Azure OpenAI's batch API
- Process multiple products efficiently in batches
- Track processing status and handle errors
- Store generated content in the database

## Architecture

### Components

1. **AzureOpenAIBatchProcessor** (`app/services/azure_openai_batch.py`)
   - Main service for batch processing operations
   - Handles batch file creation, submission, and result processing

2. **Batch Processing API** (`app/api/batch_processing.py`)
   - REST API endpoints for batch operations
   - Status monitoring and result processing

3. **Database Models**
   - `OpenAIBatch`: Tracks batch jobs
   - `Product`: Enhanced with AI content fields

4. **Scripts**
   - `test_azure_openai_batch.py`: Test AI content generation
   - `run_batch_processing.py`: Full pipeline execution

## Setup

### 1. Environment Variables

Add these to your `.env` file:

```bash
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
OPENAI_API_KEY=your-api-key
```

### 2. Database Migration

The system requires the following database fields (already included in models.py):

```sql
-- Products table enhancements
ALTER TABLE products ADD COLUMN IF NOT EXISTS openai_product_id VARCHAR(100);
ALTER TABLE products ADD COLUMN IF NOT EXISTS openai_processing_status VARCHAR(50) DEFAULT 'pending';
ALTER TABLE products ADD COLUMN IF NOT EXISTS openai_batch_id VARCHAR(100);
ALTER TABLE products ADD COLUMN IF NOT EXISTS openai_processed_at TIMESTAMP;
ALTER TABLE products ADD COLUMN IF NOT EXISTS openai_error_message TEXT;

-- OpenAI batches table
CREATE TABLE IF NOT EXISTS openai_batches (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR(100) UNIQUE NOT NULL,
    filename VARCHAR(255) NOT NULL,
    product_count INTEGER DEFAULT 0,
    status VARCHAR(50) DEFAULT 'pending',
    openai_job_id VARCHAR(100),
    result_file VARCHAR(255),
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);
```

## Usage

### 1. Testing AI Content Generation

Before running batch processing, test the AI content generation:

```bash
# Test with 5 products from each category
cd backend
python scripts/test_azure_openai_batch.py

# Test a single product
python scripts/test_azure_openai_batch.py --single
```

This will:
- Generate AI content for test products
- Save results to `test_results/` directory
- Validate JSON schema compliance
- Show success/failure rates

### 2. Creating and Running Batches

#### Option A: Using the Script

```bash
# Run full pipeline (create, submit, monitor, process)
python scripts/run_batch_processing.py --action pipeline --category-limit 3

# Create test batch only
python scripts/run_batch_processing.py --action test

# List all batches
python scripts/run_batch_processing.py --action list

# Check products status
python scripts/run_batch_processing.py --action status
```

#### Option B: Using the API

```bash
# Create batch
curl -X POST "http://localhost:8000/api/v1/batch/create?category_limit=3" \
  -H "X-API-Key: your-api-key"

# Submit batch
curl -X POST "http://localhost:8000/api/v1/batch/submit/{batch_id}" \
  -H "X-API-Key: your-api-key"

# Check status
curl -X GET "http://localhost:8000/api/v1/batch/status/{batch_id}" \
  -H "X-API-Key: your-api-key"

# Process results
curl -X POST "http://localhost:8000/api/v1/batch/process-results/{batch_id}" \
  -H "X-API-Key: your-api-key"
```

### 3. API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/batch/create` | POST | Create new batch |
| `/api/v1/batch/submit/{batch_id}` | POST | Submit batch to Azure OpenAI |
| `/api/v1/batch/status/{batch_id}` | GET | Check batch status |
| `/api/v1/batch/process-results/{batch_id}` | POST | Process batch results |
| `/api/v1/batch/create-test` | POST | Create test batch |
| `/api/v1/batch/list` | GET | List all batches |
| `/api/v1/batch/products/status` | GET | Get products processing status |

## Batch Processing Workflow

### 1. Batch Creation
- Selects products from each category (default: 3 per category)
- Creates batch file in JSONL format
- Records batch in database

### 2. Batch Submission
- Submits batch file to Azure OpenAI
- Updates batch status to 'processing'
- Returns OpenAI job ID

### 3. Status Monitoring
- Polls Azure OpenAI for batch status
- Updates database with current status
- Handles completion, failure, or expiration

### 4. Result Processing
- Downloads result file from Azure OpenAI
- Parses JSON responses
- Updates products with AI content
- Handles errors and retries

## AI Content Structure

The generated AI content follows this structure:

```json
{
  "product_input": {
    "name": "Product Name",
    "slug": "product-slug",
    "brand": "Brand Name",
    "category": "Category Name",
    "description": "Product description",
    "msrp_price": 999.99,
    "url_source": "Source URL",
    "image_uri": "Image URL",
    "specs": {},
    "store_links": {
      "thomann": {"product_url": null, "ref_id": null},
      "gear4music": {"product_url": null, "ref_id": null},
      // ... other stores
    }
  },
  "images": {
    "front_view": {"source": "source", "page_url": "url", "image_url": "url"},
    "back_view": {"source": "source", "page_url": "url", "image_url": "url"},
    "official_image": {"source": "source", "page_url": "url", "image_url": "url"}
  },
  "ai_generated_content": {
    "en-US": {
      "basic_info": {},
      "technical_analysis": {},
      "purchase_decision": {},
      "usage_guidance": {},
      "maintenance_care": {},
      "professional_assessment": {}
    },
    "en-GB": {},
    "es-ES": {},
    "fr-FR": {},
    "de-DE": {},
    "it-IT": {},
    "pt-PT": {}
  },
  "customer_reviews": {},
  "content_metadata": {},
  "qa": {}
}
```

## Configuration

### Batch File Format

The system creates batch files in JSONL format:

```json
{"custom_id": "prod-1", "method": "POST", "url": "/v1/chat/completions", "body": {...}}
{"custom_id": "prod-2", "method": "POST", "url": "/v1/chat/completions", "body": {...}}
```

### Azure OpenAI Configuration

- **Model**: Uses the deployment specified in `AZURE_OPENAI_DEPLOYMENT_NAME`
- **Max Tokens**: 4000
- **Temperature**: 0.7
- **Response Format**: JSON Schema validation
- **Completion Window**: 24 hours

## Monitoring and Troubleshooting

### 1. Check Batch Status

```bash
# Using script
python scripts/run_batch_processing.py --action list

# Using API
curl -X GET "http://localhost:8000/api/v1/batch/list" \
  -H "X-API-Key: your-api-key"
```

### 2. Check Products Status

```bash
# Using script
python scripts/run_batch_processing.py --action status

# Using API
curl -X GET "http://localhost:8000/api/v1/batch/products/status" \
  -H "X-API-Key: your-api-key"
```

### 3. Common Issues

#### Batch Submission Fails
- Check Azure OpenAI endpoint and API key
- Verify deployment name exists
- Check file size limits

#### Processing Fails
- Check JSON schema compliance
- Verify product data completeness
- Review error messages in database

#### Results Processing Fails
- Check result file availability
- Verify JSON parsing
- Review individual product errors

### 4. Logs and Debugging

- Check application logs for detailed error messages
- Review generated batch files in `batch_files/` directory
- Examine test results in `test_results/` directory

## Best Practices

### 1. Testing
- Always test with a small batch first
- Use the test script to validate AI content quality
- Review generated content before full processing

### 2. Batch Sizing
- Start with 3 products per category
- Monitor processing times and costs
- Adjust batch sizes based on performance

### 3. Error Handling
- Monitor failed products and retry
- Review error messages for patterns
- Implement retry logic for transient failures

### 4. Cost Management
- Monitor Azure OpenAI usage
- Use appropriate model tiers
- Implement rate limiting if needed

## Integration with Frontend

The generated AI content is stored in the `ai_generated_content` field of the Product model and can be accessed through the existing product API endpoints.

The content includes:
- Multi-language support (7 locales)
- Comprehensive product analysis
- Purchase guidance
- Technical specifications
- Professional assessments

## Security Considerations

- API keys are stored in environment variables
- Batch files are stored locally and cleaned up
- Database access is properly authenticated
- Error messages don't expose sensitive information

## Performance Optimization

- Batch processing reduces API calls
- Async processing for better throughput
- Database indexing on batch and product fields
- Efficient JSON parsing and validation

## Future Enhancements

- Real-time status updates via WebSocket
- Automatic retry mechanisms
- Content quality scoring
- A/B testing for different prompts
- Integration with affiliate link generation
