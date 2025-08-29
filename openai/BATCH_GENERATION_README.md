# Batch File Generation for Azure OpenAI

This directory contains scripts to generate Azure OpenAI batch files from all products in the database.

## Overview

The batch files are used to process products through Azure OpenAI's batch processing API, enriching product data with comprehensive information including:

- Brand and category identification
- Technical specifications
- Store links
- Image descriptions
- Localized content (multiple languages)
- Product identifiers
- Metadata

## Files

### Core Scripts

- **`generate_all_batch_files.py`** - Main script to generate batch files from database
- **`batch_summary.py`** - Utility to analyze and summarize generated batch files
- **`create_azure_batch.py`** - Original script for creating small test batches

### Configuration

- **`get_config_from_db.py`** - Retrieves batch prompts and schemas from database
- **`database.py`** - Database connection and models
- **`config.py`** - Configuration settings

### Generated Files

- **`batch_files/`** - Directory containing all generated batch files
- **`batch_results/`** - Directory for processing results

## Usage

### Generate Batch Files

```bash
# Generate all products in batches of 100
python3.11 generate_all_batch_files.py --mode batched --batch-size 100

# Generate single large file with all products
python3.11 generate_all_batch_files.py --mode single

# Generate only first 1000 products
python3.11 generate_all_batch_files.py --max-products 1000

# Use different deployment name
python3.11 generate_all_batch_files.py --deployment gpt-4o-mini
```

### Options

- `--mode`: `batched` (multiple files) or `single` (one large file)
- `--batch-size`: Number of products per batch file (default: 100)
- `--max-products`: Maximum products to process (default: all)
- `--deployment`: Azure OpenAI deployment name (default: gpt-4.1)

### Analyze Batch Files

```bash
# Show complete summary
python3.11 batch_summary.py

# Show only deployment statistics
python3.11 batch_summary.py --deployments-only

# Analyze different directory
python3.11 batch_summary.py --batch-dir /path/to/batch/files
```

## Current Status

### Generated Files (Latest Run)

- **Total Files**: 71
- **Total Requests**: 6,859
- **Total Size**: 26.63 MB
- **Average Requests per File**: 96.6
- **Deployment**: gpt-4.1

### File Structure

Batch files are named with the pattern:
```
azure_batch_{batch_number:03d}_{product_count}_products_{timestamp}.jsonl
```

Example: `azure_batch_001_100_products_20250829_181922.jsonl`

## Batch File Format

Each batch file contains JSONL (JSON Lines) format with one request per line:

```json
{
  "custom_id": "product_sku",
  "method": "POST",
  "url": "/chat/completions",
  "body": {
    "model": "gpt-4.1",
    "messages": [
      {
        "role": "system",
        "content": "System prompt for product enrichment..."
      },
      {
        "role": "user",
        "content": "Process this product: {...}"
      }
    ],
    "response_format": {"type": "json_object"},
    "max_tokens": 4000,
    "temperature": 0.1
  }
}
```

## Processing Workflow

1. **Generate Batch Files**: Use `generate_all_batch_files.py`
2. **Upload to Azure**: Upload JSONL files to Azure Blob Storage
3. **Submit Batch Job**: Submit batch job to Azure OpenAI
4. **Monitor Progress**: Track job status in Azure portal
5. **Download Results**: Download processed results
6. **Process Results**: Use `process_results.py` to handle responses

## Database Requirements

The scripts expect a `products_filled` table with the following columns:
- `id` (primary key)
- `sku` (unique identifier)
- `name` (product name)
- `slug` (URL slug)
- `description` (product description)
- `msrp_price` (price)
- `url` (source URL)

## Environment Setup

Ensure the following environment variables are set:
- `DATABASE_URL`: PostgreSQL connection string
- Azure OpenAI credentials (if using Azure services)

## Troubleshooting

### Common Issues

1. **Database Connection**: Verify `DATABASE_URL` is correct
2. **Permission Errors**: Ensure write permissions to `batch_files/` directory
3. **Memory Issues**: For large datasets, use batched mode instead of single mode
4. **Async Loop Errors**: The script handles async operations automatically

### Performance Tips

- Use batched mode for large datasets to avoid memory issues
- Adjust batch size based on your system capabilities
- Monitor disk space when generating large numbers of files
- Consider using different deployment names for different product categories

## Next Steps

1. Upload batch files to Azure Blob Storage
2. Submit batch processing job to Azure OpenAI
3. Monitor job progress
4. Download and process results
5. Import enriched data back to database

## Support

For issues or questions:
1. Check the generated batch files for format correctness
2. Verify database connectivity
3. Review Azure OpenAI batch processing documentation
4. Check system resources and permissions
