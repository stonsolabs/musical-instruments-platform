# Fixing Google Search Console Redirect Errors

## Overview

This document explains how to identify and fix redirect errors reported by Google Search Console (GSC). Redirect errors occur when Googlebot cannot properly crawl a page due to redirect issues.

## Common Causes

Based on the [WooHelpDesk guide](https://www.woohelpdesk.com/blog/how-to-fix-redirect-error-in-google-search-console/), common causes include:

1. **Redirect Loops** - URLs that redirect back to themselves
2. **Long Redirect Chains** - Too many redirects before reaching the final page
3. **HTTP to HTTPS Issues** - Mixed protocol redirects
4. **Redirects to Blocked Pages** - Final destination is blocked by robots.txt or login
5. **Broken Destination URLs** - Redirects to 404 or deleted pages
6. **Trailing Slash Mismatches** - Inconsistent trailing slash usage

## What We Fixed

### 1. Next.js Redirect Configuration

Added proper redirect handling in `frontend/next.config.js`:

- **Trailing Slash Redirects**: Automatically redirects URLs with trailing slashes to non-trailing slash versions (301 permanent redirect)
- **Consistent URL Structure**: Ensures all blog and product URLs follow the same pattern

```javascript
async redirects() {
  return [
    {
      source: '/blog/:slug/',
      destination: '/blog/:slug',
      permanent: true, // 301 redirect
    },
    {
      source: '/products/:slug/',
      destination: '/products/:slug',
      permanent: true,
    },
  ];
}
```

### 2. Sitemap Validation

Updated sitemap generation to:

- **Validate URLs**: Only include valid, properly formatted URLs
- **Filter Invalid Slugs**: Exclude blog posts and products with invalid slug characters
- **Proper URL Encoding**: Ensure slugs are properly encoded in sitemaps
- **Prevent Duplicate Slashes**: Filter out URLs with double slashes or trailing slashes

Files updated:
- `frontend/pages/blog-sitemap.xml.tsx`
- `frontend/pages/sitemap.xml.tsx`

### 3. Redirect Issue Detection Script

Created a diagnostic script to identify redirect issues:

**Location**: `backend/scripts/maintenance/check_redirect_issues.py`

**What it checks**:
- Duplicate blog post slugs
- Invalid slug characters
- Trailing hyphens in slugs
- Duplicate product slugs
- Sitemap URL validation

**Usage**:
```bash
# Make sure you're in the backend directory and have dependencies installed
cd backend

# Install dependencies if needed
pip install -r requirements.txt

# Make sure DATABASE_URL is set in your environment
export DATABASE_URL="postgresql://user:pass@host:port/dbname"

# Run the script
python3 scripts/maintenance/check_redirect_issues.py
```

## How to Use

### Step 1: Run the Diagnostic Script

Run the script to identify potential issues:

```bash
cd backend
python scripts/maintenance/check_redirect_issues.py
```

This will:
- Check all published blog posts for slug issues
- Check all active products for slug issues
- Validate sitemap URLs
- Provide recommendations

### Step 2: Review GSC Data

1. Go to Google Search Console
2. Navigate to **Indexing > Pages**
3. Look for **"Page with redirect"** in the "Why pages aren't indexed" section
4. Click on it to see the specific URLs affected

### Step 3: Identify the Issue Type

For each problematic URL, determine the issue:

- **Redirect Loop**: URL redirects to itself
- **Broken Destination**: Redirects to a 404 page
- **Long Chain**: Multiple redirects before final destination
- **Trailing Slash**: Inconsistent trailing slash usage

### Step 4: Fix the Issues

#### For Blog Posts:

1. **If slug changed**: Create a redirect mapping (if needed, add to Next.js config)
2. **If post deleted**: Remove from sitemap (already handled by validation)
3. **If invalid slug**: Fix the slug in the database

#### For Products:

1. **If slug changed**: Update internal links and sitemap
2. **If product deleted**: Remove from sitemap (already handled)
3. **If invalid slug**: Fix the slug in the database

### Step 5: Validate Fixes

1. Use the URL Inspection Tool in GSC to test specific URLs
2. Use tools like:
   - [Screaming Frog SEO Spider](https://www.screamingfrog.co.uk/seo-spider/)
   - [Redirect Checker](https://httpstatus.io/)
   - [Ahrefs Site Audit](https://ahrefs.com/site-audit)

### Step 6: Request Re-indexing

After fixing issues:

1. Go to GSC
2. Open the **"Page with redirect"** issue
3. Click **"Validate Fix"**
4. Google will re-crawl the affected URLs

## Best Practices

### 1. Use 301 Redirects for Permanent Changes

Always use 301 (permanent) redirects when URLs change permanently. This tells Google the page has moved permanently.

### 2. Keep Redirects Simple

- Avoid redirect chains (A → B → C)
- Redirect directly to the final destination (A → C)
- Limit redirects to 1-2 hops maximum

### 3. Update Internal Links

After changing URLs:
- Update internal links in content
- Update navigation menus
- Update sitemaps
- Update canonical tags

### 4. Monitor Regularly

- Check GSC weekly for new redirect issues
- Run the diagnostic script monthly
- Review sitemap validity after major changes

### 5. Consistent URL Structure

- Use consistent trailing slash policy (we use no trailing slashes)
- Use lowercase URLs
- Use hyphens, not underscores
- Keep URLs short and descriptive

## Troubleshooting

### Issue: Redirect Loop Detected

**Solution**: 
1. Check if URL redirects to itself
2. Remove the redirect rule causing the loop
3. Update the destination URL

### Issue: Too Many Redirects

**Solution**:
1. Identify the redirect chain
2. Update all redirects to point directly to the final destination
3. Remove intermediate redirects

### Issue: Redirect to 404

**Solution**:
1. Find the broken destination URL
2. Either fix the destination URL or remove the redirect
3. Update internal links pointing to the broken URL

### Issue: Trailing Slash Mismatch

**Solution**:
1. Ensure `trailingSlash: false` in `next.config.js` (already set)
2. Add redirect rules for trailing slash URLs (already added)
3. Update sitemaps to use consistent format

## Next Steps

1. ✅ Run the diagnostic script to identify current issues
2. ✅ Review GSC data for specific problematic URLs
3. ✅ Fix identified issues
4. ✅ Validate fixes using URL Inspection Tool
5. ✅ Request re-indexing in GSC
6. ✅ Monitor for new issues

## Additional Resources

- [Google Search Console Help - Redirect Errors](https://support.google.com/webmasters/answer/7440203)
- [WooHelpDesk Guide - Fix Redirect Errors](https://www.woohelpdesk.com/blog/how-to-fix-redirect-error-in-google-search-console/)
- [Next.js Redirects Documentation](https://nextjs.org/docs/app/api-reference/next-config-js/redirects)

## Current Status

Based on your GSC data:
- **Page with redirect**: 3 pages
- **Not found (404)**: 2 pages
- **Crawled - currently not indexed**: 1 page

After implementing these fixes:
1. The redirect rules will handle trailing slash issues
2. Sitemap validation will prevent invalid URLs
3. The diagnostic script will help identify remaining issues

Run the diagnostic script and review the specific URLs in GSC to identify the exact pages causing issues.

