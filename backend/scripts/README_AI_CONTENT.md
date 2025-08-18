# AI Content Generation for Musical Instruments

This project provides multiple scripts for generating comprehensive AI content for musical instrument products in the database. The content follows a detailed structure that includes technical analysis, purchase decision guidance, usage recommendations, maintenance care, and professional assessments.

## Available Scripts

### 1. `generate_ai_content.py` - Standard Processing
- **Best for**: Small to medium datasets (up to 100 products)
- **Processing**: Sequential processing with individual API calls
- **Cost**: Standard OpenAI API pricing
- **Speed**: Slower but more reliable for small batches

### 2. `generate_ai_content_batch.py` - Concurrent Batch Processing
- **Best for**: Medium to large datasets (100-1000 products)
- **Processing**: Concurrent processing with configurable batch sizes
- **Cost**: Standard OpenAI API pricing with optimized concurrency
- **Speed**: Faster than standard processing with better error handling

### 3. `generate_ai_content_openai_batch.py` - OpenAI Batch API
- **Best for**: Large datasets (1000+ products)
- **Processing**: Uses OpenAI's official batch API for maximum cost efficiency
- **Cost**: Significantly cheaper (up to 50% cost reduction)
- **Speed**: Asynchronous processing with 24-hour completion window

## Features

- **Comprehensive Content Structure**: Generates detailed content following the specified JSON format
- **Background Processing**: Runs as admin scripts, not part of the website API
- **Flexible Filtering**: Can process all products, specific categories, brands, or individual products
- **Multiple Processing Options**: Choose the best approach for your dataset size
- **Error Handling**: Robust error handling with detailed logging and retry logic
- **Results Export**: Saves processing results to JSON files with timestamps
- **Progress Tracking**: Real-time progress updates and statistics

## Content Structure

The generated content includes:

### Basic Information
- Product overview (2-3 sentences)
- Key features (3-5 features)
- Target skill level (Beginner/Intermediate/Advanced/Professional)
- Country of origin
- Release year

### Technical Analysis
- **Sound Characteristics**: Tonal profile, output level, best genres, pickup positions
- **Build Quality**: Construction type, hardware quality, finish quality, expected durability
- **Playability**: Neck profile, action setup, comfort rating, weight category

### Purchase Decision Guidance
- **Why Buy**: Benefits and advantages
- **Why Not Buy**: Limitations and drawbacks
- **Best For**: Ideal user types and reasons
- **Not Ideal For**: User types who should avoid this product

### Usage Guidance
- Recommended amplifiers
- Suitable music styles (excellent/good/limited)
- Skill development (learning curve, growth potential)

### Maintenance Care
- Maintenance level (Low/Medium/High)
- Common issues
- Care instructions (daily/weekly/monthly/annual)
- Upgrade potential and recommended budget

### Professional Assessment
- Expert ratings (1-10 scale for build quality, sound quality, value, versatility)
- Standout features
- Notable limitations
- Competitive position in the market

### Content Metadata
- Generation timestamp
- Content version
- SEO keywords
- Readability score
- Word count

## Usage

### Prerequisites

1. Ensure you have the required environment variables set:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export DATABASE_URL="your-database-url"
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Prerequisites

1. Ensure you have the required environment variables set:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export DATABASE_URL="your-database-url"
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Script Selection Guide

| Dataset Size | Recommended Script | Command Example |
|--------------|-------------------|-----------------|
| 1-100 products | `generate_ai_content.py` | `python generate_ai_content.py --all` |
| 100-1000 products | `generate_ai_content_batch.py` | `python generate_ai_content_batch.py --all --batch-size 50` |
| 1000+ products | `generate_ai_content_openai_batch.py` | `python generate_ai_content_openai_batch.py --all --batch-size 100` |

### Standard Processing (`generate_ai_content.py`)

#### Basic Commands

```bash
cd backend/scripts

# Generate content for all products
python generate_ai_content.py --all

# Generate content for specific products
python generate_ai_content.py --product-ids "1,2,3,4,5"

# Generate content with limits
python generate_ai_content.py --all --limit 10

# Force regeneration of existing content
python generate_ai_content.py --all --force

# Filter by category
python generate_ai_content.py --all --category "electric-guitars"

# Filter by brand
python generate_ai_content.py --all --brand "fender"

# Combine filters
python generate_ai_content.py --all --category "electric-guitars" --brand "fender" --limit 5
```

#### Command Line Options

- `--all`: Generate content for all active products
- `--product-ids`: Comma-separated list of specific product IDs
- `--limit`: Maximum number of products to process
- `--force`: Force regeneration even if content already exists
- `--category`: Filter by category slug
- `--brand`: Filter by brand slug

### Concurrent Batch Processing (`generate_ai_content_batch.py`)

#### Basic Commands

```bash
cd backend/scripts

# Process all products with default settings
python generate_ai_content_batch.py --all

# Process with custom batch size and concurrency
python generate_ai_content_batch.py --all --batch-size 100 --max-concurrent 10

# Process specific products
python generate_ai_content_batch.py --product-ids "1,2,3,4,5" --batch-size 25

# Process with custom delays
python generate_ai_content_batch.py --all --delay-batches 5.0 --delay-requests 1.0
```

#### Command Line Options

- `--all`: Generate content for all active products
- `--product-ids`: Comma-separated list of specific product IDs
- `--category`: Filter by category slug
- `--brand`: Filter by brand slug
- `--force`: Force regeneration even if content already exists
- `--batch-size`: Number of products per batch (default: 50)
- `--max-concurrent`: Maximum concurrent requests (default: 5)
- `--delay-batches`: Delay between batches in seconds (default: 2.0)
- `--delay-requests`: Delay between requests in seconds (default: 0.5)
- `--max-retries`: Maximum retry attempts (default: 3)
- `--output-dir`: Output directory for results (default: "batch_results")

### OpenAI Batch API (`generate_ai_content_openai_batch.py`)

#### Basic Commands

```bash
cd backend/scripts

# Process all products with OpenAI batch API
python generate_ai_content_openai_batch.py --all

# Process with custom batch size
python generate_ai_content_openai_batch.py --all --batch-size 200

# Process specific category
python generate_ai_content_openai_batch.py --all --category "electric-guitars" --batch-size 150
```

#### Command Line Options

- `--all`: Generate content for all active products
- `--category`: Filter by category slug
- `--brand`: Filter by brand slug
- `--force`: Force regeneration even if content already exists
- `--batch-size`: Number of products per batch (default: 100)
- `--poll-interval`: Poll interval for batch status in seconds (default: 60)
- `--output-dir`: Output directory for results (default: "openai_batch_results")

### Output

The script provides:
- Real-time progress updates in the console
- Processing statistics (processed, successful, failed, skipped)
- JSON file with detailed results (saved with timestamp)
- Error handling for individual products

### Example Output

#### Standard Processing
```
🎯 Found 25 products to process
🤖 Generating AI content for: Fender Player Stratocaster MIM
✅ Successfully generated content for: Fender Player Stratocaster MIM
⏭️  Skipping Gibson Les Paul Standard (content already exists)
🤖 Generating AI content for: Yamaha P-45 Digital Piano
✅ Successfully generated content for: Yamaha P-45 Digital Piano

==================================================
📊 PROCESSING STATISTICS
==================================================
Total processed: 25
Successful: 20
Failed: 2
Skipped: 3
==================================================
💾 Results saved to: ai_content_generation_20241201_143022.json
```

#### Concurrent Batch Processing
```
🎯 Found 500 products to process
📦 Processing 10 batches of 50 products each

🔄 Processing batch 1/10
🔄 Processing batch 1 with 50 products...
✅ Successfully generated content for: Fender Player Stratocaster MIM
✅ Successfully generated content for: Gibson Les Paul Standard
⏭️  Skipping Yamaha P-45 Digital Piano (content already exists)
⏳ Waiting 2.0s before next batch...

==================================================
📊 BATCH PROCESSING STATISTICS
==================================================
Total products: 500
Processed: 500
Successful: 450
Failed: 30
Skipped: 20
Retries: 15
Processing time: 1800.50 seconds
Products per minute: 16.67
==================================================
```

#### OpenAI Batch API
```
🎯 Found 2000 products to process
📦 Processing 20 batches of 100 products each

🔄 Processing batch 1/20
📝 Created batch input file: openai_batch_results/batch_input.jsonl
🚀 Submitted batch job: batch_abc123
📊 Batch batch_abc123 status: validating
📊 Batch batch_abc123 status: in_progress
🔄 Batch is in progress... (45%)
📊 Batch batch_abc123 status: completed
📥 Downloaded batch results: openai_batch_results/batch_batch_abc123_results.jsonl

==================================================
📊 OPENAI BATCH API PROCESSING STATISTICS
==================================================
Total products: 2000
Batches created: 20
Batches completed: 20
Products processed: 2000
Successful: 1950
Failed: 50
Skipped: 0
Processing time: 3600.00 seconds
Products per minute: 33.33
==================================================
```

## Content Guidelines

The AI content generator follows these guidelines:

- **Professional but accessible tone**
- **Factual and unbiased assessments**
- **Focus on practical benefits and limitations**
- **Use industry-standard terminology correctly**
- **Consider European market preferences**
- **Avoid excessive marketing language**
- **Base assessments on actual specifications provided**

## Error Handling

The script handles various error scenarios:

- **API Rate Limits**: Built-in delays between requests
- **Network Issues**: Automatic retry logic
- **Invalid Product Data**: Graceful handling of missing information
- **Database Errors**: Transaction rollback on failures
- **Interruption**: Clean shutdown with statistics

## Monitoring and Logging

- Progress is displayed in real-time
- Detailed error messages for failed products
- Processing statistics are shown at completion
- Results are saved to timestamped JSON files
- Console output includes emojis for easy scanning

## Performance Considerations

### Standard Processing
- 1-second delay between API calls to avoid rate limits
- Sequential processing for reliability
- Best for small datasets where cost is not a major concern

### Concurrent Batch Processing
- Configurable delays between requests and batches
- Concurrent processing with semaphore limits
- Retry logic for failed requests
- Progress saving at regular intervals
- Best for medium datasets with cost optimization

### OpenAI Batch API
- **Significantly cheaper** (up to 50% cost reduction)
- Asynchronous processing with 24-hour completion window
- No rate limiting concerns
- Best for large datasets (1000+ products)
- Requires OpenAI batch API access

## Integration with Website

The generated content is stored in the `ai_generated_content` JSON field of the Product model and is automatically included in API responses. The website can access this content through the existing product endpoints.

## Troubleshooting

### Common Issues

1. **OpenAI API Key**: Ensure your API key is valid and has sufficient credits
2. **Database Connection**: Verify your database URL is correct
3. **Product Data**: Ensure products have sufficient information (specifications, brand, category)
4. **Rate Limits**: The standard and concurrent scripts include delays, but you may need to adjust for your API tier
5. **Batch API Access**: The OpenAI batch API script requires batch API access (contact OpenAI support)

### Debug Mode

For detailed debugging, you can modify the scripts to include more verbose logging by setting debug flags in the respective generator classes.

### Cost Optimization Tips

1. **Use the right script for your dataset size**:
   - Small datasets (<100): Use standard processing
   - Medium datasets (100-1000): Use concurrent batch processing
   - Large datasets (1000+): Use OpenAI batch API

2. **Batch API Benefits**:
   - Up to 50% cost reduction
   - No rate limiting
   - Asynchronous processing
   - Better for large-scale operations

3. **Monitor API Usage**:
   - Check your OpenAI dashboard for usage statistics
   - Set up billing alerts
   - Use the progress tracking features to monitor costs

## Future Enhancements

- Support for content versioning
- Content quality scoring
- Automated content review workflows
- Integration with content management systems
- Support for multiple AI providers
