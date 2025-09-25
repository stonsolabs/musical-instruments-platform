from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse

from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import AffiliateStore, Product, BrandExclusivity


class EnhancedAffiliateService:
    """Enhanced affiliate service with brand exclusivity, regional preferences, and automatic URL generation"""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def get_affiliate_stores_for_product(
        self, 
        product: Product, 
        user_region: Optional[str] = None,
        store_links: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Get affiliate stores for a product with advanced filtering:
        - Brand exclusivity rules
        - Regional preferences
        - Store link availability
        - Automatic affiliate URL generation
        """
        
        # Get all active stores with affiliate programs
        query = select(AffiliateStore).where(
            and_(
                AffiliateStore.is_active.is_(True),
                AffiliateStore.has_affiliate_program.is_(True),
                AffiliateStore.show_affiliate_buttons.is_(True)
            )
        )
        
        result = await self.db.execute(query)
        all_stores = result.scalars().all()
        
        # Get brand exclusivity rules
        exclusivity_query = select(BrandExclusivity).where(
            BrandExclusivity.brand_name == product.brand.name
        )
        exclusivity_result = await self.db.execute(exclusivity_query)
        brand_exclusivities = {ex.store_id: ex for ex in exclusivity_result.scalars().all()}
        
        # Filter and score stores
        eligible_stores = []
        
        for store in all_stores:
            # Check brand exclusivity
            exclusivity = brand_exclusivities.get(store.id)
            
            # Check if this brand has exclusive stores
            has_exclusive_stores = any(ex.is_exclusive for ex in brand_exclusivities.values())
            if has_exclusive_stores:
                # If brand has exclusive stores, only show the exclusive store(s)
                if not (exclusivity and exclusivity.is_exclusive):
                    continue  # Skip non-exclusive stores when exclusive stores exist
            
            # Check regional availability
            if not self._is_store_available_in_region(store, user_region):
                continue
            
            # Check if product has store link (if provided)
            has_store_link = True
            original_url = None
            if store_links and store.slug in store_links:
                original_url = store_links[store.slug].get('product_url')
                has_store_link = bool(original_url)
            
            # Calculate priority score
            priority_score = self._calculate_priority_score(
                store, 
                user_region, 
                exclusivity,
                has_store_link
            )
            
            # Generate affiliate URL
            affiliate_url = self._generate_affiliate_url(store, original_url, product)
            
            eligible_stores.append({
                "id": store.id,
                "name": store.name,
                "slug": store.slug,
                "logo_url": store.logo_url,
                "website_url": store.website_url,
                "priority_score": priority_score,
                "commission_rate": float(store.commission_rate) if store.commission_rate else None,
                "original_url": original_url,
                "affiliate_url": affiliate_url,
                "has_store_link": has_store_link,
                "is_exclusive": exclusivity.is_exclusive if exclusivity else False,
                "is_preferred": exclusivity and not exclusivity.is_exclusive,
                "region": user_region,
            })
        
        # Sort by priority score (highest first)
        eligible_stores.sort(key=lambda x: x['priority_score'], reverse=True)
        
        # If exclusive store exists, only return that one
        exclusive_stores = [s for s in eligible_stores if s['is_exclusive']]
        if exclusive_stores:
            return exclusive_stores
        
        return eligible_stores
    
    def _is_store_available_in_region(self, store: AffiliateStore, user_region: Optional[str]) -> bool:
        """Check if store is available in user's region"""
        if not user_region:
            return True  # If no region specified, show all stores
        
        if not store.available_regions:
            return True  # If no regions specified, available everywhere
        
        return user_region in store.available_regions
    
    def _calculate_priority_score(
        self, 
        store: AffiliateStore, 
        user_region: Optional[str],
        exclusivity: Optional[BrandExclusivity],
        has_store_link: bool
    ) -> int:
        """Calculate priority score for store ordering"""
        score = store.priority or 0
        
        # Regional priority boost
        if user_region and store.regional_priority:
            regional_boost = store.regional_priority.get(user_region, 0)
            score += regional_boost
        
        # Brand exclusivity boost
        if exclusivity:
            score += exclusivity.priority_boost
        
        # Store link availability boost
        if has_store_link:
            score += 100  # Significant boost for stores with product links
        
        # Primary region boost
        if user_region and store.primary_region == user_region:
            score += 50
        
        return score
    
    def _generate_affiliate_url(self, store: AffiliateStore, original_url: Optional[str], product: Product) -> Optional[str]:
        """Generate affiliate URL for the store"""
        if not store.affiliate_id:
            return original_url
        
        # If we have original URL, add affiliate parameters
        if original_url:
            return self._add_affiliate_parameters(store, original_url)
        
        # If no original URL but store has fallback enabled
        if store.use_store_fallback:
            fallback_url = store.store_fallback_url or store.website_url
            return self._add_affiliate_parameters(store, fallback_url)
        
        return None
    
    def _add_affiliate_parameters(self, store: AffiliateStore, url: str) -> str:
        """Add affiliate parameters to URL with domain-specific affiliate IDs"""
        # Special handling for Thomann URLs to use /intl/ path for better international compatibility
        if store.slug == "thomann":
            url = self._normalize_thomann_url(url)
        
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)
        
        # Handle domain-specific affiliate IDs
        affiliate_id = self._get_domain_specific_affiliate_id(store, parsed.netloc)
        if affiliate_id:
            query_params[affiliate_id] = ['1']
        
        # Add custom affiliate parameters
        if store.affiliate_parameters:
            for key, value in store.affiliate_parameters.items():
                if isinstance(value, str):
                    query_params[key] = [value]
                elif isinstance(value, (list, tuple)):
                    query_params[key] = [str(v) for v in value]
                else:
                    query_params[key] = [str(value)]
        
        # Special handling for Thomann's manual affiliate system
        if store.slug == "thomann":
            # Using manual affiliate format with /intl/ for automatic regional display
            # The /intl/ path ensures users see the correct regional website based on their location
            # This provides localized experience without requiring RediR™
            pass
        
        # Reconstruct URL with affiliate parameters
        new_query = urlencode(query_params, doseq=True)
        affiliate_url = urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment
        ))
        
        return affiliate_url
    
    def _normalize_thomann_url(self, url: str) -> str:
        """Normalize Thomann URLs to use /intl/ path for better international compatibility"""
        parsed = urlparse(url)
        
        # Process all Thomann domains (thomann.de, thomann.co.uk, etc.)
        if not parsed.netloc or 'thomann' not in parsed.netloc:
            return url
        
        # Convert regional paths to /intl/ for better international compatibility
        # Examples:
        # /gb/product/123 -> /intl/product/123
        # /de/product/456 -> /intl/product/456
        # /fr/product/789 -> /intl/product/789
        path = parsed.path
        
        # Replace regional paths with /intl/
        regional_patterns = ['/gb/', '/de/', '/fr/', '/it/', '/es/', '/nl/', '/be/', '/at/', '/ch/', '/us/']
        for pattern in regional_patterns:
            if path.startswith(pattern):
                path = path.replace(pattern, '/intl/', 1)
                break
        
        # If it's already /intl/ or doesn't have a regional prefix, keep as is
        if not path.startswith('/intl/') and not any(path.startswith(p) for p in regional_patterns):
            # For root paths or other paths, ensure they use /intl/
            if path == '/' or path == '':
                path = '/intl/'
            elif not path.startswith('/intl/'):
                # Convert direct product paths to /intl/ for better international compatibility
                path = '/intl' + path
        
        # Reconstruct URL
        return urlunparse((
            parsed.scheme,
            parsed.netloc,
            path,
            parsed.params,
            parsed.query,
            parsed.fragment
        ))
    
    def _get_domain_specific_affiliate_id(self, store: AffiliateStore, domain: str) -> Optional[str]:
        """Get domain-specific affiliate ID based on the URL domain"""
        # Check if store has domain-specific affiliate IDs
        if hasattr(store, 'domain_affiliate_ids') and store.domain_affiliate_ids:
            # Extract country/region from domain
            domain_lower = domain.lower()
            
            # Map common domains to regions
            domain_mapping = {
                'thomann.de': 'DE',
                'thomann.co.uk': 'UK',
                'thomann.fr': 'FR',
                'thomann.it': 'IT',
                'thomann.es': 'ES',
                'thomann.nl': 'NL',
                'thomann.be': 'BE',
                'thomann.at': 'AT',
                'thomann.ch': 'CH',
                'amazon.com': 'US',
                'amazon.co.uk': 'UK',
                'amazon.de': 'DE',
                'amazon.fr': 'FR',
                'amazon.it': 'IT',
                'amazon.es': 'ES',
                'amazon.ca': 'CA',
                'amazon.jp': 'JP',
                'gear4music.com': 'UK',
                'gear4music.de': 'DE',
                'gear4music.fr': 'FR',
                'sweetwater.com': 'US',
                'guitarcenter.com': 'US',
                'donnerdeal.com': 'US',
            }
            
            # Get region from domain
            region = domain_mapping.get(domain_lower, 'DEFAULT')
            
            # Return domain-specific affiliate ID or fallback to default
            return store.domain_affiliate_ids.get(region, store.affiliate_id)
        
        # Fallback to default affiliate ID
        return store.affiliate_id
    
    async def get_brand_exclusivity_rules(self, brand_name: str) -> List[Dict]:
        """Get exclusivity rules for a brand"""
        query = select(BrandExclusivity).where(BrandExclusivity.brand_name == brand_name)
        result = await self.db.execute(query)
        exclusivities = result.scalars().all()
        
        return [
            {
                "id": ex.id,
                "brand_name": ex.brand_name,
                "store_id": ex.store_id,
                "store_name": ex.store.name,
                "is_exclusive": ex.is_exclusive,
                "regions": ex.regions,
                "priority_boost": ex.priority_boost,
            }
            for ex in exclusivities
        ]
    
    async def set_brand_exclusivity(
        self,
        brand_name: str,
        store_id: int,
        is_exclusive: bool = True,
        regions: Optional[List[str]] = None,
        priority_boost: int = 0
    ) -> BrandExclusivity:
        """Set brand exclusivity rule"""
        
        # Check if rule already exists
        query = select(BrandExclusivity).where(
            and_(
                BrandExclusivity.brand_name == brand_name,
                BrandExclusivity.store_id == store_id
            )
        )
        result = await self.db.execute(query)
        existing = result.scalar_one_or_none()
        
        if existing:
            # Update existing rule
            existing.is_exclusive = is_exclusive
            existing.regions = regions
            existing.priority_boost = priority_boost
            existing.updated_at = datetime.utcnow()
        else:
            # Create new rule
            existing = BrandExclusivity(
                brand_name=brand_name,
                store_id=store_id,
                is_exclusive=is_exclusive,
                regions=regions,
                priority_boost=priority_boost
            )
            self.db.add(existing)
        
        await self.db.commit()
        return existing
    
    async def update_store_affiliate_config(self, store_id: int, 
                                          has_affiliate_program: bool = None,
                                          affiliate_base_url: str = None,
                                          affiliate_id: str = None,
                                          domain_affiliate_ids: Dict = None,
                                          affiliate_parameters: Dict = None,
                                          show_affiliate_buttons: bool = None,
                                          priority: int = None) -> AffiliateStore:
        """Update affiliate configuration for a store"""
        
        query = select(AffiliateStore).where(AffiliateStore.id == store_id)
        result = await self.db.execute(query)
        store = result.scalar_one_or_none()
        
        if not store:
            raise ValueError(f"Store with ID {store_id} not found")
        
        # Update only provided fields
        if has_affiliate_program is not None:
            store.has_affiliate_program = has_affiliate_program
        if affiliate_base_url is not None:
            store.affiliate_base_url = affiliate_base_url
        if affiliate_id is not None:
            store.affiliate_id = affiliate_id
        if domain_affiliate_ids is not None:
            store.domain_affiliate_ids = domain_affiliate_ids
        if affiliate_parameters is not None:
            store.affiliate_parameters = affiliate_parameters
        if show_affiliate_buttons is not None:
            store.show_affiliate_buttons = show_affiliate_buttons
        if priority is not None:
            store.priority = priority
        
        await self.db.commit()
        return store
