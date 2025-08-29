# Exclusive Store Feature - How It Works

## 🎯 Overview

The exclusive store feature ensures that certain brands are only shown in specific stores, preventing conflicts and ensuring proper brand representation.

## 🏗️ Database Structure

### BrandExclusivity Table
```sql
CREATE TABLE brand_exclusivities (
    id SERIAL PRIMARY KEY,
    brand_name VARCHAR(100) NOT NULL,
    store_id INTEGER NOT NULL REFERENCES affiliate_stores(id),
    is_exclusive BOOLEAN DEFAULT TRUE,
    regions TEXT[], -- NULL = all regions, ['US', 'EU'] = specific regions
    priority_boost INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(brand_name, store_id)
);
```

## ⚙️ Configuration Examples

### 1. Exclusive Brands (Only One Store)
```python
# Harley Benton is EXCLUSIVE to Thomann only
{
    "brand_name": "Harley Benton",
    "store_slug": "thomann",
    "is_exclusive": True,  # This makes it EXCLUSIVE
    "regions": None,       # All regions
    "priority_boost": 50,
}

# Donner is EXCLUSIVE to Donner store only
{
    "brand_name": "Donner", 
    "store_slug": "donner",
    "is_exclusive": True,  # This makes it EXCLUSIVE
    "regions": None,       # All regions
    "priority_boost": 50,
}
```

### 2. Preferred Brands (Multiple Stores, But Prioritized)
```python
# Fender is PREFERRED in Sweetwater
{
    "brand_name": "Fender",
    "store_slug": "sweetwater", 
    "is_exclusive": False,  # This makes it PREFERRED (not exclusive)
    "regions": None,        # All regions (regional control is at store level)
    "priority_boost": 20,
}

# Gibson is PREFERRED in Guitar Center
{
    "brand_name": "Gibson",
    "store_slug": "guitarcenter",
    "is_exclusive": False,  # This makes it PREFERRED (not exclusive)
    "regions": None,        # All regions (regional control is at store level)
    "priority_boost": 15,
}
```

## 🔄 How It Works Step by Step

### Step 1: Get Brand Exclusivity Rules
```python
# Query all exclusivity rules for the product's brand
exclusivity_query = select(BrandExclusivity).where(
    BrandExclusivity.brand_name == product.brand.name
)
exclusivity_result = await self.db.execute(exclusivity_query)
brand_exclusivities = {ex.store_id: ex for ex in exclusivity_result.scalars().all()}
```

### Step 2: Check Each Store
```python
for store in all_stores:
    # Get exclusivity rule for this store
    exclusivity = brand_exclusivities.get(store.id)
    
    # If brand is EXCLUSIVE to this store, only show this store
    if exclusivity and exclusivity.is_exclusive:
        if not self._is_exclusive_store_only(brand_exclusivities, store.id):
            continue  # Skip other stores if this is exclusive
```

### Step 3: Exclusive Store Logic
```python
def _is_exclusive_store_only(self, brand_exclusivities: Dict, store_id: int) -> bool:
    """Check if this is the only exclusive store for the brand"""
    exclusive_stores = [ex for ex in brand_exclusivities.values() if ex.is_exclusive]
    return len(exclusive_stores) == 1 and exclusive_stores[0].store_id == store_id
```

### Step 4: Final Filtering
```python
# Sort by priority score
eligible_stores.sort(key=lambda x: x['priority_score'], reverse=True)

# If exclusive store exists, ONLY return that one
exclusive_stores = [s for s in eligible_stores if s['is_exclusive']]
if exclusive_stores:
    return exclusive_stores  # Only exclusive stores

return eligible_stores  # All eligible stores (if no exclusives)
```

## 📊 Real-World Examples

### Example 1: Harley Benton Product
**Product:** Harley Benton Guitar  
**Brand:** Harley Benton  
**User Region:** US

**Result:**
```json
{
  "affiliate_stores": [
    {
      "name": "Thomann",
      "is_exclusive": true,
      "priority_score": 160,
      "affiliate_url": "https://www.thomann.de/gb/harley-benton-guitar?affiliate=123&redir=1"
    }
  ]
}
```
**Explanation:** Only Thomann is shown because Harley Benton is EXCLUSIVE to Thomann.

### Example 2: Fender Product (US User)
**Product:** Fender Stratocaster  
**Brand:** Fender  
**User Region:** US

**Result:**
```json
{
  "affiliate_stores": [
    {
      "name": "Sweetwater",
      "is_exclusive": false,
      "is_preferred": true,
      "priority_score": 127,
      "affiliate_url": "https://www.sweetwater.com/fender-stratocaster?affiliate=456"
    },
    {
      "name": "Guitar Center", 
      "is_exclusive": false,
      "is_preferred": true,
      "priority_score": 122,
      "affiliate_url": "https://www.guitarcenter.com/fender-stratocaster?affiliate=789"
    },
    {
      "name": "Amazon",
      "is_exclusive": false,
      "is_preferred": false,
      "priority_score": 105,
      "affiliate_url": "https://www.amazon.com/fender-stratocaster?affiliate=abc"
    }
  ]
}
```
**Explanation:** Multiple stores shown because Fender is PREFERRED (not exclusive), but Sweetwater and Guitar Center get priority boosts.

### Example 3: Fender Product (EU User)
**Product:** Fender Stratocaster  
**Brand:** Fender  
**User Region:** EU

**Result:**
```json
{
  "affiliate_stores": [
    {
      "name": "Thomann",
      "is_exclusive": false,
      "is_preferred": false,
      "priority_score": 110,
      "affiliate_url": "https://www.thomann.de/gb/fender-stratocaster?affiliate=123&redir=1"
    },
    {
      "name": "Amazon",
      "is_exclusive": false,
      "is_preferred": false,
      "priority_score": 105,
      "affiliate_url": "https://www.amazon.com/fender-stratocaster?affiliate=abc"
    }
  ]
}
```
**Explanation:** Sweetwater and Guitar Center are not shown because their **store-level regional settings** only allow them in US region.

## 🎯 Priority Scoring with Exclusivity

### Base Priority Score Calculation
```python
score = store.priority or 0

# Regional priority boost
if user_region and store.regional_priority:
    score += store.regional_priority.get(user_region, 0)

# Brand exclusivity boost
if exclusivity:
    score += exclusivity.priority_boost  # +50 for exclusive, +20/+15 for preferred

# Store link availability boost
if has_store_link:
    score += 100  # Significant boost for stores with product links

# Primary region boost
if user_region and store.primary_region == user_region:
    score += 50
```

### Example Priority Scores
- **Thomann (Harley Benton exclusive):** 10 + 50 + 100 + 50 = 210
- **Sweetwater (Fender preferred):** 7 + 20 + 100 + 50 = 177
- **Amazon (generic):** 5 + 100 = 105

## 🔧 Configuration Options

### 1. Global Exclusive (All Regions)
```python
{
    "brand_name": "Harley Benton",
    "store_slug": "thomann",
    "is_exclusive": True,
    "regions": None,  # All regions
}
```

### 2. Regional Exclusive (Rare Use Case)
```python
{
    "brand_name": "Local Brand",
    "store_slug": "local_store",
    "is_exclusive": True,
    "regions": ["US"],  # Only in US (rare use case)
}
```

### 3. Preferred with Priority Boost
```python
{
    "brand_name": "Fender",
    "store_slug": "sweetwater",
    "is_exclusive": False,
    "regions": None,  # All regions (regional control is at store level)
    "priority_boost": 20,
}
```

### 4. Multiple Preferred Stores
```python
# Fender preferred in Sweetwater
{"brand_name": "Fender", "store_slug": "sweetwater", "is_exclusive": False, "regions": None}
# Fender also preferred in Guitar Center  
{"brand_name": "Fender", "store_slug": "guitarcenter", "is_exclusive": False, "regions": None}
```

## 🚀 Benefits

### For Brands
- **Exclusive brands** get dedicated store representation
- **Preferred brands** get priority positioning
- **Brand-level control** over store availability

### For Users
- **No confusion** about where to buy exclusive brands
- **Clear preferences** for preferred brands
- **Regional relevance** in store selection (handled at store level)

### For You
- **Automatic filtering** - no manual configuration needed
- **Flexible rules** - exclusive or preferred
- **Store-level regional control** - regional availability handled by store settings
- **Priority management** - control store ordering

## 📝 Summary

The exclusive store feature works by:

1. **Checking brand exclusivity rules** for each product
2. **Filtering stores** based on exclusivity and store-level regional availability  
3. **Calculating priority scores** with exclusivity boosts
4. **Returning only exclusive stores** if any exist, otherwise all eligible stores
5. **Respecting store-level regional restrictions** (not brand-level)

**Key Point:** Regional control is handled at the **store level** (in AffiliateStore model), not at the brand level. Brand exclusivity rules focus on which stores can show which brands, while regional availability is determined by each store's `available_regions` setting.

This ensures that Harley Benton products only show Thomann, Donner products only show Donner store, while other brands can show multiple stores with appropriate priority ordering.
