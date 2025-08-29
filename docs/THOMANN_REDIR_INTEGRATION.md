# Thomann RediR™ Integration

## Overview

Thomann uses the **RediR™** redirect system developed by Sunlab, which is available exclusively to Clickfire users. This system automatically handles regional redirects to the correct Thomann domain based on the user's location.

## How RediR™ Works

According to the [RediR™ FAQ page](https://intercom.help/clickfire/en/collections/2455555-redir-faq-page-for-clickfire-users), RediR™ is a link-redirect-tool that:

1. **Automatic Regional Redirects** - Redirects users to their local Thomann store
2. **Domain Management** - Handles different Thomann domains (thomann.de, thomann.co.uk, thomann.fr, etc.)
3. **Clickfire Integration** - Works seamlessly with Clickfire affiliate tracking

## Integration in Our System

### Affiliate Parameters

When configuring Thomann in our system, we include the `redir` parameter:

```python
"affiliate_parameters": {
    "partner": "your-thomann-partner-id",
    "redir": "1"  # Enable RediR™ redirect system
}
```

### URL Generation

Our system generates Thomann affiliate URLs like this:

```
https://www.thomann.de/gb/product/123?your-thomann-uk-affiliate-id=1&partner=your-partner-id&redir=1
```

**Domain-specific affiliate IDs are automatically selected based on the URL domain:**
- `thomann.de` → German affiliate ID
- `thomann.co.uk` → UK affiliate ID  
- `thomann.fr` → French affiliate ID
- etc.

### How It Works

1. **User clicks affiliate link** → Thomann URL with affiliate parameters
2. **RediR™ processes the request** → Detects user's location
3. **Automatic redirect** → User lands on their local Thomann store
4. **Affiliate tracking maintained** → All parameters preserved through redirect

## Benefits

### For Users
- **Localized Experience** - Users see prices in their currency
- **Regional Shipping** - Shipping costs and delivery times for their region
- **Local Support** - Customer service in their language

### For Affiliates
- **Simplified Management** - One URL works for all regions
- **Better Conversion** - Users more likely to buy from local store
- **Automatic Optimization** - RediR™ handles regional logic

## Configuration

### Required Setup

1. **Clickfire Account** - RediR™ is exclusive to Clickfire users
2. **Thomann Partnership** - Must have Thomann affiliate partnership
3. **RediR™ Activation** - Enable RediR™ in your Clickfire dashboard

### Our System Integration

```python
# Thomann store configuration with domain-specific affiliate IDs
{
    "name": "Thomann",
    "slug": "thomann",
    "affiliate_id": "your-thomann-default-affiliate-id",
    "domain_affiliate_ids": {
        "DE": "your-thomann-de-affiliate-id",
        "UK": "your-thomann-uk-affiliate-id",
        "FR": "your-thomann-fr-affiliate-id",
        "IT": "your-thomann-it-affiliate-id",
        "ES": "your-thomann-es-affiliate-id",
        "US": "your-thomann-us-affiliate-id"
    },
    "affiliate_parameters": {
        "partner": "your-thomann-partner-id",
        "redir": "1"  # Enable RediR™
    }
}
```

## Example URLs

### Before RediR™ (Manual Regional URLs)
- US: `https://www.thomann.de/us/product/123?affiliate=123`
- UK: `https://www.thomann.de/gb/product/123?affiliate=123`
- DE: `https://www.thomann.de/de/product/123?affiliate=123`

### After RediR™ (Single URL)
- All regions: `https://www.thomann.de/gb/product/123?affiliate=123&redir=1`
- RediR™ automatically redirects to correct regional domain

## Regional Domains Supported

RediR™ supports redirects to these Thomann domains:
- `thomann.de` (Germany)
- `thomann.co.uk` (United Kingdom)
- `thomann.fr` (France)
- `thomann.it` (Italy)
- `thomann.es` (Spain)
- `thomann.nl` (Netherlands)
- `thomann.be` (Belgium)
- `thomann.at` (Austria)
- `thomann.ch` (Switzerland)
- And more...

## Testing

To test RediR™ integration:

1. **Generate affiliate URL** using our system
2. **Click the link** from different regions
3. **Verify redirect** to correct regional domain
4. **Check affiliate tracking** is maintained

## Troubleshooting

### Common Issues

1. **No redirect happening** - Check if RediR™ is enabled in Clickfire
2. **Wrong regional domain** - Verify user location detection
3. **Affiliate tracking lost** - Ensure all parameters are preserved

### Support

For RediR™ specific issues, contact:
- **Clickfire Support** - For RediR™ functionality
- **Thomann Support** - For affiliate partnership issues

## References

- [RediR™ FAQ Page](https://intercom.help/clickfire/en/collections/2455555-redir-faq-page-for-clickfire-users)
- [Clickfire Documentation](https://clickfire.com)
- [Thomann Affiliate Program](https://www.thomann.de/affiliate)
