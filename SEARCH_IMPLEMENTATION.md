# Product Search Implementation

This document describes the complete product search functionality implemented for the Musical Instruments Platform.

## Features

### Backend (FastAPI + PostgreSQL + Redis)

1. **PostgreSQL Full-Text Search**
   - Uses `to_tsvector` and `plainto_tsquery` for efficient text search
   - Searches across product name, description, brand, and category
   - Ranking by relevance and popularity
   - Optimized with GIN indexes

2. **Redis Caching**
   - 5-minute cache for search results
   - Reduces database load for repeated queries
   - Automatic cache invalidation

3. **API Endpoints**
   - `GET /api/search/autocomplete?q={query}&limit={limit}` - Real-time autocomplete
   - `GET /api/search/suggestions?q={query}&limit={limit}` - Search suggestions
   - `POST /api/search/cache/clear` - Clear search cache (admin)

### Frontend (Next.js + TypeScript)

1. **SearchAutocomplete Component**
   - Debounced input (300ms delay)
   - Real-time suggestions as user types
   - Keyboard navigation (arrow keys, enter, escape)
   - Click outside to close
   - Loading states and error handling

2. **Integration Points**
   - Header component (desktop and mobile)
   - Homepage hero section
   - Products page search bar

## Setup Instructions

### 1. Backend Setup

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Start PostgreSQL and Redis
docker-compose up -d postgres redis

# Run database migrations and add search indexes
python scripts/add_search_indexes.py

# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup

```bash
# Install dependencies
cd frontend
npm install

# Start the development server
npm run dev
```

### 3. Database Indexes

The search indexes are automatically created by running:

```bash
python backend/scripts/add_search_indexes.py
```

This script creates:
- GIN indexes for full-text search
- Composite indexes for common queries
- Triggers for automatic search vector updates

## API Usage

### Autocomplete Search

```typescript
// Frontend usage
const response = await apiClient.searchAutocomplete('fender', 8);
console.log(response.results); // Array of SearchAutocompleteProduct
```

**Response Format:**
```json
{
  "query": "fender",
  "results": [
    {
      "id": 1,
      "name": "Fender Stratocaster",
      "slug": "fender-stratocaster",
      "brand": { "id": 1, "name": "Fender", "slug": "fender" },
      "category": { "id": 1, "name": "Electric Guitars", "slug": "electric" },
      "avg_rating": 4.5,
      "review_count": 125,
      "best_price": {
        "price": 699.99,
        "currency": "EUR",
        "store": { "id": 1, "name": "Thomann", "slug": "thomann" },
        "affiliate_url": "https://..."
      },
      "rank": 0.85,
      "search_highlight": "Fender <mark>Stratocaster</mark>"
    }
  ],
  "total": 1
}
```

### Search Suggestions

```typescript
const response = await apiClient.getSearchSuggestions('guitar', 5);
console.log(response.suggestions); // Array of strings
```

## Performance Optimizations

### Database Level
- **GIN Indexes**: Fast full-text search queries
- **Composite Indexes**: Optimized for common filter combinations
- **Search Vectors**: Pre-computed text vectors for faster matching

### Application Level
- **Redis Caching**: 5-minute cache for repeated queries
- **Debounced Input**: Reduces API calls during typing
- **Connection Pooling**: Efficient database connections

### Query Optimization
- **Limit Results**: Max 8 autocomplete suggestions
- **Eager Loading**: Single query for product + brand + category
- **Index Hints**: Database uses optimal indexes

## Search Ranking

Results are ranked by:
1. **Text Relevance**: PostgreSQL `ts_rank` score
2. **Rating**: Higher rated products first
3. **Review Count**: More reviews = higher ranking
4. **Recency**: Newer products get slight boost

## Error Handling

### Backend
- Graceful handling of malformed queries
- Fallback to simple LIKE queries if full-text search fails
- Redis connection error handling

### Frontend
- Network error handling with retry logic
- Empty state handling
- Loading states and timeouts

## Monitoring

### Cache Performance
```bash
# Check Redis cache hit rate
redis-cli info stats | grep keyspace_hits
redis-cli info stats | grep keyspace_misses
```

### Database Performance
```sql
-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
WHERE indexname LIKE '%search%';
```

## Troubleshooting

### Common Issues

1. **Slow Search Results**
   - Check if indexes are created: `python scripts/add_search_indexes.py`
   - Verify Redis is running: `docker-compose ps`
   - Check database connection pool

2. **No Search Results**
   - Ensure sample data is loaded
   - Check product `is_active` status
   - Verify search query length (min 2 characters)

3. **Cache Issues**
   - Clear Redis cache: `POST /api/search/cache/clear`
   - Check Redis memory usage
   - Verify cache TTL settings

### Debug Mode

Enable debug logging in `backend/app/config.py`:
```python
DEBUG: bool = True
```

## Future Enhancements

1. **Advanced Search Features**
   - Fuzzy matching for typos
   - Synonym expansion
   - Category-specific search weights

2. **Performance Improvements**
   - Elasticsearch integration for large datasets
   - CDN caching for static results
   - GraphQL for flexible queries

3. **User Experience**
   - Search history
   - Popular searches
   - Search analytics

## Security Considerations

1. **Input Validation**
   - Query length limits (2-100 characters)
   - SQL injection prevention via parameterized queries
   - XSS prevention in search highlights

2. **Rate Limiting**
   - Consider implementing rate limits for search endpoints
   - Monitor for abuse patterns

3. **Data Privacy**
   - Search queries are not logged by default
   - Consider GDPR compliance for search analytics
