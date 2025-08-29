#!/usr/bin/env python3
"""
Simple Product Crawler
Crawls products from pre-filtered Thomann URLs and downloads one image per product
"""

import asyncio
import aiohttp
import json
import re
import time
import uuid
import os
from typing import List, Dict, Any, Optional, Set
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, parse_qs
import logging
from dataclasses import dataclass
from loguru import logger

# Import existing managers
from database_manager import DatabaseManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class ProductData:
    """Product data structure"""
    name: str
    brand: str
    price: Optional[str]
    url: str
    sku: str
    category: str
    image_url: Optional[str] = None
    description: Optional[str] = None
    specifications: Optional[Dict] = None

class SimpleProductCrawler:
    """Simple crawler that works with pre-filtered URLs"""
    
    def __init__(self, max_concurrent: int = 20, test_mode: bool = False, max_test_products: int = 5):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.session = None
        self.db = None
        self.test_mode = test_mode
        self.max_test_products = max_test_products
        self.products_crawled = 0
        
        # Proxy configuration (load from .env file)
        from dotenv import load_dotenv
        load_dotenv()
        
        self.proxy_url = os.getenv('IPROYAL_PROXY_URL')
        if not self.proxy_url:
            raise ValueError("IPROYAL_PROXY_URL environment variable is required")
        
        # Enhanced Thomann-specific selectors for better accuracy
        self.selectors = {
            # Focus on product-specific selectors first, fallback to general ones
            'product_links': '.product__content.no-underline a, .product__content a, .product-item a, .product-card a, .fx-product-card a, .search-result-product-card a, .product-tile a, [data-testid*="product"] a, .fx-product-tile a',
            'pagination': '.pagination a, .page-numbers a, [data-testid="pagination"] a, .pager a, .pagination__link',
            'product_name': 'h1.fx-product-headline__title, h1.product__title, h1, .product-name, .product-title, .product__name, [data-testid="product-name"]',
            'product_price': '.fx-price, .price, .product-price, .price__value, .product__price, [data-testid="price"], .price-current',
            'product_brand': '.fx-product-headline__brand, .brand, .product-brand, .manufacturer, .product__brand, [data-testid="brand"]',
            'product_image': '.navigator__item-image, .fx-image, .product-image img, .gallery-image img, .product__image img, .main-image img',
            'product_description': '.fx-product-description, .fx-product-text, .description, .product-description, .product__description, .product-details, [data-testid="description"]',
            'product_sku': '.sku, .product-sku, .article-number, .item-number, [data-testid="sku"]'
        }
    
    async def __aenter__(self):
        """Async context manager entry"""
        # Setup session with optimized settings for headless scraping
        connector = aiohttp.TCPConnector(
            limit=50,           # Reduced from 100 to be more conservative
            limit_per_host=10,  # Reduced from 30 to avoid rate limiting
            ttl_dns_cache=300,  # Cache DNS for 5 minutes
            use_dns_cache=True,
            keepalive_timeout=30,
            enable_cleanup_closed=True
        )
        timeout = aiohttp.ClientTimeout(total=25, connect=8, sock_read=15)
        
        # Optimized headers for bandwidth efficiency
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',  # Removed image formats to save bandwidth
                'Accept-Language': 'en-US,en;q=0.5',  # Simplified
                'Accept-Encoding': 'gzip, deflate',    # Removed br to save processing
                'Connection': 'keep-alive',
                'Cache-Control': 'no-cache',            # Prevent caching issues
                'DNT': '1',                             # Do Not Track for privacy
                'Upgrade-Insecure-Requests': '1',
            }
        )
        
        # Initialize managers
        self.db = DatabaseManager()
        await self.db.__aenter__()
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
        if self.db:
            await self.db.__aexit__(exc_type, exc_val, exc_tb)
    
    async def load_urls_from_file(self, file_path: str = "thomann_urls.txt") -> List[str]:
        """Load URLs from the thomann_urls.txt file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip()]
            
            logger.info(f"✅ Loaded {len(urls)} URLs from {file_path}")
            return urls
        except FileNotFoundError:
            logger.error(f"❌ File {file_path} not found")
            return []
        except Exception as e:
            logger.error(f"❌ Error loading URLs: {e}")
            return []
    
    async def crawl_all_products(self) -> Dict[str, List[ProductData]]:
        """Crawl all products from the pre-filtered URLs"""
        urls = await self.load_urls_from_file()
        if not urls:
            logger.error("❌ No URLs to crawl")
            return {}
        
        # Filter URLs based on assigned categories for this replica
        assigned_categories = os.getenv('ASSIGNED_CATEGORIES', '')
        if assigned_categories:
            try:
                category_indices = [int(x.strip()) for x in assigned_categories.split(',')]
                urls = [urls[i] for i in category_indices if i < len(urls)]
                logger.info(f"📋 REPLICA MODE: Processing categories {category_indices} ({len(urls)} URLs)")
            except Exception as e:
                logger.warning(f"⚠️ Invalid ASSIGNED_CATEGORIES format: {e}. Processing all URLs.")
        
        all_products = {}
        total_products = 0
        
        if self.test_mode:
            logger.info(f"🧪 TEST MODE: Crawling max {self.max_test_products} products...")
        else:
            logger.info(f"🚀 Starting to crawl {len(urls)} category URLs...")
        
        for i, category_url in enumerate(urls):
            try:
                # Extract category name from URL
                category_name = self._extract_category_name(category_url)
                
                # Get the correct category_id based on assigned categories
                if assigned_categories:
                    # Use the actual category index from the assigned categories
                    category_indices = [int(x.strip()) for x in assigned_categories.split(',')]
                    category_id = category_indices[i] if i < len(category_indices) else 0
                else:
                    # Fallback to original logic
                    category_id = i
                
                logger.info(f"📦 [{i+1}/{len(urls)}] Crawling category: {category_name} (ID: {category_id})")
                
                # Set current category ID for database operations
                self.db.current_category_id = category_id
                
                # Get start page from environment variable
                start_from_page = int(os.getenv('START_FROM_PAGE', '1'))
                
                # Crawl products from this category
                products = await self._crawl_category_products(category_url, category_name, start_from_page)
                
                if products:
                    all_products[category_name] = products
                    total_products += len(products)
                    logger.info(f"✅ {category_name}: {len(products)} products found")
                else:
                    logger.warning(f"⚠️ {category_name}: No products found")
                
                # Check if we've reached the test limit
                if self.test_mode and total_products >= self.max_test_products:
                    logger.info(f"🧪 Test limit reached ({self.max_test_products} products). Stopping...")
                    break
                
                # Respectful delay between categories
                await asyncio.sleep(2)  # Increased delay
                
            except Exception as e:
                logger.error(f"❌ Error crawling category {category_url}: {e}")
                continue
        
        logger.info(f"🎯 Total products crawled: {total_products}")
        return all_products
    
    def _extract_category_name(self, url: str) -> str:
        """Extract category name from URL"""
        try:
            # Try to extract from URL path
            parsed = urlparse(url)
            path = parsed.path
            
            # Remove common prefixes and suffixes
            path = path.replace('/all-products-from-the-category-', '')
            path = path.replace('.html', '')
            path = path.replace('/', '')
            path = path.replace('_', ' ')
            path = path.replace('-', ' ')
            
            # Capitalize words
            category_name = ' '.join(word.capitalize() for word in path.split())
            
            # Handle special cases
            if 'electric-guitars' in url:
                return 'Electric Guitars'
            elif 'acoustic-guitars' in url:
                return 'Acoustic Guitars'
            elif 'bass-guitars' in url or 'electric-basses' in url:
                return 'Bass Guitars'
            elif 'digital-pianos' in url:
                return 'Digital Pianos'
            elif 'stage-pianos' in url:
                return 'Stage Pianos'
            elif 'synthesizer' in url:
                return 'Synthesizers'
            elif 'midi' in url:
                return 'MIDI Controllers'
            elif 'turntables' in url:
                return 'Turntables'
            elif 'organs' in url:
                return 'Electric Organs'
            elif 'keyboards' in url:
                return 'Keyboards'
            
            return category_name if category_name else 'Unknown Category'
            
        except Exception:
            return 'Unknown Category'
    
    async def _crawl_category_products(self, category_url: str, category_name: str, start_from_page: int = 1) -> List[ProductData]:
        """Crawl all products from a category URL"""
        products = []
        page = start_from_page
        max_pages = 500  # Increased limit for very large categories
        consecutive_empty_pages = 0
        max_consecutive_empty = 3  # Stop after 3 consecutive empty pages
        
        if start_from_page > 1:
            logger.info(f"   🚀 Starting from page {start_from_page}")
        
        while page <= max_pages and consecutive_empty_pages < max_consecutive_empty:
            try:
                # Add page parameter to URL
                page_url = self._add_page_parameter(category_url, page)
                
                logger.info(f"   📄 Page {page}: {page_url}")
                
                # Get page content and check pagination
                async with self.semaphore:
                    page_result = await self._crawl_page_products(page_url, category_name)
                
                if not page_result['total_found']:
                    consecutive_empty_pages += 1
                    logger.info(f"   ⏹️ No products found on page {page} (empty page #{consecutive_empty_pages})")
                else:
                    consecutive_empty_pages = 0  # Reset counter
                    products.extend(page_result['products'])
                    logger.info(f"   ✅ Page {page}: {page_result['total_found']} products found ({len(page_result['products'])} new)")
                
                # Check if we've reached the last page
                if page_result['is_last_page']:
                    logger.info(f"   🏁 Reached last page ({page})")
                    break
                
                page += 1
                await asyncio.sleep(1.5)  # Increased delay between pages for bandwidth conservation
                
            except Exception as e:
                logger.error(f"   ❌ Error on page {page}: {e}")
                consecutive_empty_pages += 1
                page += 1
                continue
        
        if consecutive_empty_pages >= max_consecutive_empty:
            logger.info(f"   🛑 Stopped after {max_consecutive_empty} consecutive empty pages")
        
        logger.info(f"   📊 Total products from {category_name}: {len(products)}")
        return products
    
    def _add_page_parameter(self, url: str, page: int) -> str:
        """Add page parameter to URL for Thomann"""
        separator = '&' if '?' in url else '?'
        
        # Extract existing ls parameter if present, otherwise default to 100
        import re
        ls_match = re.search(r'[?&]ls=(\d+)', url)
        ls_value = ls_match.group(1) if ls_match else '100'
        
        if page == 1:
            # For page 1, add ls parameter if not already present
            if not ls_match:
                return f"{url}{separator}ls={ls_value}"
            return url
        else:
            # For other pages, add both pg and ls parameters
            if not ls_match:
                return f"{url}{separator}pg={page}&ls={ls_value}"
            else:
                # Replace existing ls parameter
                return re.sub(r'[?&]ls=\d+', f'&ls={ls_value}', url) + f"&pg={page}"
    
    def _is_last_page(self, soup: BeautifulSoup, current_url: str) -> bool:
        """Check if this is the last page by analyzing pagination elements"""
        try:
            # Extract ls (products per page) from URL
            import re
            ls_match = re.search(r'[?&]ls=(\d+)', current_url)
            ls_value = int(ls_match.group(1)) if ls_match else 100
            
            # Method 1: Check for "next" button - if disabled or not present, it's the last page
            next_buttons = soup.select('.pagination .next, .pagination .next-page, [data-testid="next-page"], .pager .next, .pagination-next')
            if next_buttons:
                for button in next_buttons:
                    # Check if button is disabled
                    if button.get('disabled') or 'disabled' in button.get('class', []):
                        return True
                    # Check if button has no href or points to current page
                    href = button.get('href')
                    if not href or href == current_url:
                        return True
                    # Check if button text indicates it's disabled
                    button_text = button.get_text(strip=True).lower()
                    if 'next' not in button_text or 'disabled' in button_text:
                        return True
            
            # Method 2: Check pagination numbers - if current page is the highest, it's the last page
            page_numbers = soup.select('.pagination a, .page-numbers a, [data-testid="page-number"], .pager a, .pagination-page')
            if page_numbers:
                current_page_num = self._extract_page_number(current_url)
                max_page_num = current_page_num
                
                for link in page_numbers:
                    href = link.get('href')
                    if href:
                        page_num = self._extract_page_number(href)
                        if page_num and page_num > max_page_num:
                            max_page_num = page_num
                
                if current_page_num and max_page_num and current_page_num >= max_page_num:
                    return True
            
            # Method 3: Check for "last" button
            last_buttons = soup.select('.pagination .last, .pagination .last-page, [data-testid="last-page"], .pager .last')
            if last_buttons:
                for button in last_buttons:
                    href = button.get('href')
                    if href and href == current_url:
                        return True
            
            # Method 4: Check if there are no pagination elements at all (single page)
            pagination_elements = soup.select('.pagination, .page-numbers, [data-testid="pagination"], .pager')
            if not pagination_elements:
                # If no pagination elements, check if we have a reasonable number of products
                product_links = soup.select('.product__content.no-underline, .fx-product-list-entry .product__content.no-underline')
                if len(product_links) >= ls_value * 0.8:  # If we have 80%+ of expected products, there might be more pages
                    return False
                return True
            
            # Method 5: Check for "no results" or "end of results" messages
            no_results = soup.select('.no-results, .no-products, .empty-results, [data-testid="no-results"], .search-no-results')
            if no_results:
                return True
            
            # Method 6: Check for Thomann-specific pagination patterns
            # Look for "showing X to Y of Z results" - if Y == Z, we're on the last page
            result_info = soup.select('.results-info, .pagination-info, .search-results-info')
            for info in result_info:
                text = info.get_text().lower()
                if 'showing' in text and 'of' in text:
                    # Extract numbers from "showing X to Y of Z"
                    numbers = re.findall(r'\d+', text)
                    if len(numbers) >= 3:
                        showing_to = int(numbers[1])  # Y
                        total = int(numbers[2])       # Z
                        if showing_to >= total:
                            return True
            
            # Method 7: Check if current page number is very high (likely last page)
            current_page_num = self._extract_page_number(current_url)
            if current_page_num and current_page_num > 200:  # Increased limit for large categories
                return True
            
            # Method 8: IMPROVED - Check if we have fewer products than expected (likely last page)
            product_links = soup.select('.product__content.no-underline, .fx-product-list-entry .product__content.no-underline')
            if len(product_links) < ls_value * 0.5:  # If we have less than 50% of expected products, likely last page
                logger.info(f"📄 Last page detected: {len(product_links)} products found (expected ~{ls_value})")
                return True
            
            # Method 9: Check if we have significantly fewer products than ls (strong indicator of last page)
            if len(product_links) < ls_value * 0.8 and len(product_links) > 0:
                logger.info(f"📄 Likely last page: {len(product_links)} products found (expected ~{ls_value})")
                return True
            
            return False
            
        except Exception as e:
            logger.warning(f"Error checking if last page: {e}")
            return False
    
    def _extract_page_number(self, url: str) -> Optional[int]:
        """Extract page number from URL for Thomann"""
        try:
            # Parse URL parameters
            parsed = urlparse(url)
            query_params = parse_qs(parsed.query)
            
            # Check for 'pg' parameter (Thomann's pagination parameter)
            if 'pg' in query_params:
                page_str = query_params['pg'][0]
                return int(page_str)
            
            # Fallback to 'page' parameter for compatibility
            if 'page' in query_params:
                page_str = query_params['page'][0]
                return int(page_str)
            
            return None
        except Exception:
            return None
    
    async def _crawl_page_products(self, page_url: str, category_name: str) -> Dict[str, Any]:
        """Crawl products from a single page and check pagination"""
        try:
            # Make request with proxy - optimized for headless scraping and bandwidth
            proxy = self.proxy_url
            
            # Add request parameters for better performance and bandwidth efficiency
            request_headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Cache-Control': 'no-cache, no-store',  # Prevent caching issues
            }
            
            async with self.session.get(
                page_url, 
                proxy=proxy,
                headers=request_headers,
                timeout=aiohttp.ClientTimeout(total=15, connect=5),
                allow_redirects=True,
                max_redirects=2,
                compress=True  # Enable compression
            ) as response:
                if response.status != 200:
                    logger.warning(f"HTTP {response.status} for {page_url}")
                    return {'products': [], 'is_last_page': True}
                
                # Only get text content, skip images and other resources
                html = await response.text()
                
                # Log response size for debugging
                content_length = len(html)
                logger.debug(f"Received {content_length} bytes from {page_url}")
            
            # Parse HTML
            soup = BeautifulSoup(html, 'html.parser')
            
            # Check if this is the last page
            is_last_page = self._is_last_page(soup, page_url)
            
            # Find product links - try multiple Thomann-specific selectors in order of preference
            product_links = []
            
            # Priority list of selectors to try (most specific first)
            selectors_to_try = [
                '.product__content.no-underline',    # This is the correct selector for Thomann
                '.fx-product-list-entry .product__content.no-underline',  # More specific version
                '.fx-product-card a',
                '.fx-product-tile a', 
                '.product-tile a',
                '.search-result-product-card a',
                '.product__content a',
                '.product-item a',
                '.product-card a'
            ]
            
            for selector in selectors_to_try:
                links = soup.select(selector)
                if links:
                    product_links = links
                    logger.debug(f"Found {len(product_links)} product links using {selector}")
                    break
            
            # If no product-specific selectors worked, log the issue for debugging
            if not product_links:
                logger.warning("No product links found with specific selectors, checking page structure...")
                # Let's see what links we do have for debugging
                all_links = soup.find_all('a', href=True)[:10]  # First 10 links for debugging
                for i, link in enumerate(all_links):
                    href = link.get('href', '')
                    classes = ' '.join(link.get('class', []))
                    logger.debug(f"Sample link {i+1}: {href[:50]}... (classes: {classes})")
            
            if not product_links:
                logger.warning(f"No product links found on {page_url}")
                # Log some debug info about the page structure
                all_links = soup.find_all('a')
                logger.debug(f"Page has {len(all_links)} total links")
                if all_links:
                    sample_links = all_links[:5]
                    for link in sample_links:
                        href = link.get('href', '')
                        classes = ' '.join(link.get('class', []))
                        logger.debug(f"Sample link: {href[:50]}... (classes: {classes})")
                return {'products': [], 'is_last_page': is_last_page}
            
            # Extract product URLs
            product_urls = []
            logger.debug(f"Processing {len(product_links)} product links...")
            
            for i, link in enumerate(product_links[:5]):  # Log first 5 links for debugging
                href = link.get('href', '')
                classes = ' '.join(link.get('class', []))
                logger.debug(f"Link {i+1}: {href[:100]}... (classes: {classes})")
            
            for link in product_links:
                href = link.get('href')
                if href:
                    # Make URL absolute
                    if href.startswith('/'):
                        href = f"https://www.thomann.co.uk{href}"
                    elif not href.startswith('http'):
                        href = urljoin(page_url, href)
                    
                    # Strict URL filtering for Thomann - only accept actual product URLs  
                    # Accept URLs that contain .html or .htm (even with query parameters)
                    if 'thomann.co.uk' in href and ('.html' in href or '.htm' in href):
                        # Clean the URL by removing query parameters for consistency
                        clean_url = href.split('?')[0]
                        
                        # Get the filename (last part of URL) - handle both .html and .htm
                        filename = clean_url.split('/')[-1].replace('.html', '').replace('.htm', '')
                        
                        # Filter OUT various non-product URLs (but allow ?type=category since those are product URLs)
                        exclude_patterns = [
                            '/all-products-from-the-category/', '/cat_GK_', '/cat_BF_', '/cat_brand_',
                            'compinfo_', 'helpdesk_', 'mythomann', 'wishlist', 'basket',
                            'hotdeals', 'prodnews', 'topseller', 'blowouts', 'gift_voucher',
                            'newsletter', 'onlineexpert', 'classified', 'browse_wallpapers',
                            'guitars_and_basses', 'drums_and_percussion', 'studio_equipment',
                            'software', 'equipment_for_pa', 'lighting_and_stage', 'dj_equipment',
                            'broadcast_video', 'microphones', 'effects_and_signal_processors',
                            'wind_instruments', 'traditional_instruments', 'sheetmusic_books_dvds',
                            'cases_racks_bags', 'cables_and_plugs', 'accessories', 'keys.html',
                            '/intl/', 'special_downloaddeals', 'electric_guitars.html'
                        ]
                        
                        # Check if URL should be excluded
                        should_exclude = any(pattern in clean_url.lower() for pattern in exclude_patterns)
                        
                        # Accept URLs that:
                        # 1. Don't match exclusion patterns
                        # 2. Have reasonable length filenames (product names are usually descriptive)
                        # 3. Contain underscores or specific patterns typical of Thomann product URLs
                        # 4. Or are from known product patterns like manufacturer_model_variant.htm
                        if (not should_exclude and 
                            len(filename) > 5 and  # Product names are usually longer than 5 chars
                            (filename.count('_') >= 2 or  # Most products have at least 2 underscores (brand_model_variant)
                             any(char.isdigit() for char in filename) or  # Or contain numbers
                             len(filename) > 15)):  # Or are long descriptive names
                            product_urls.append(clean_url)
                            logger.debug(f"Added product URL: {clean_url[:80]}...")
                        else:
                            logger.debug(f"Filtered out non-product URL: {href[:80]}... (filename: {filename})")
                    else:
                        logger.debug(f"Filtered out non-Thomann/non-HTML URL: {href[:80]}...")
            
            # Remove duplicates
            product_urls = list(set(product_urls))
            
            if not product_urls:
                logger.warning(f"No valid product URLs found on {page_url}")
                return {'products': [], 'is_last_page': is_last_page}
            
            # Crawl each product with retry logic
            products = []
            products_found_on_page = 0  # Count all products found on page (existing + new)
            for product_url in product_urls:
                try:
                    products_found_on_page += 1  # Count this product as found on page
                    
                    # Check if product already exists (use clean URL)
                    clean_product_url = product_url.split('?')[0]
                    if await self.db.product_exists(clean_product_url):
                        logger.debug(f"Product already exists: {clean_product_url}")
                        continue
                    
                    # Check test mode limit
                    if self.test_mode and self.products_crawled >= self.max_test_products:
                        logger.info(f"🧪 Test limit reached ({self.max_test_products} products). Stopping...")
                        break
                    
                    # Crawl product details with retry
                    product_data = None
                    max_retries = 2  # Try once, retry once if failed
                    
                    for attempt in range(max_retries):
                        try:
                            product_data = await self._crawl_product_details(product_url, category_name)
                            if product_data:
                                break  # Success, exit retry loop
                        except Exception as e:
                            if attempt < max_retries - 1:
                                logger.warning(f"⚠️ Attempt {attempt + 1} failed for {product_url[:80]}...: {e}. Retrying...")
                                await asyncio.sleep(2.0)  # Wait before retry
                            else:
                                logger.error(f"❌ All attempts failed for {product_url[:80]}...: {e}. Skipping product.")
                    
                    if product_data:
                        products.append(product_data)
                        # Save to database (use clean URL)
                        saved = await self.db.save_product(
                            clean_product_url, 
                            product_data.name,
                            product_data.brand,
                            product_data.description,
                            product_data.specifications,
                            [product_data.image_url] if product_data.image_url else [],
                            product_data.price,
                            {}  # json_ld - empty for now
                        )
                        
                        if saved:
                            self.products_crawled += 1
                        
                        # Image downloading disabled - will be handled by OpenAI later
                        # if product_data.image_url:
                        #     await self.image_manager.download_and_store_image(
                        #         product_data.image_url, 
                        #         product_data.sku, 
                        #         self.session
                        #     )
                    else:
                        logger.warning(f"⚠️ Skipping product after all retry attempts: {product_url[:80]}...")
                    
                    await asyncio.sleep(0.8)  # Respectful delay between product requests
                    
                except Exception as e:
                    logger.error(f"Error crawling product {product_url}: {e}")
                    continue
            
            # Return the count of all products found on page for pagination logic
            # but only return the new products for saving
            return {'products': products, 'is_last_page': is_last_page, 'total_found': products_found_on_page}
            
        except Exception as e:
            logger.error(f"Error crawling page {page_url}: {e}")
            return {'products': [], 'is_last_page': True}
    
    async def _crawl_product_details(self, product_url: str, category_name: str) -> Optional[ProductData]:
        """Crawl detailed information from a product page"""
        try:
            # Make request with proxy - optimized for product pages and bandwidth
            proxy = self.proxy_url
            
            # Optimized headers for product pages
            request_headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Cache-Control': 'no-cache, no-store',
                'Referer': 'https://www.thomann.co.uk/',  # Add referer for better acceptance
            }
            
            async with self.session.get(
                product_url, 
                proxy=proxy,
                headers=request_headers,
                timeout=aiohttp.ClientTimeout(total=20, connect=8, sock_read=12),
                allow_redirects=True,
                max_redirects=2,
                compress=True
            ) as response:
                if response.status != 200:
                    logger.warning(f"HTTP {response.status} for {product_url}")
                    return None
                
                # Only get text content, skip images and other resources
                html = await response.text()
                
                # Log response size for debugging
                content_length = len(html)
                logger.debug(f"Received {content_length} bytes from product page {product_url}")
            
            # Parse HTML
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract product information with better handling
            name = self._extract_text(soup, self.selectors['product_name'])
            if name:
                # Clean product name by removing ratings and extra text
                import re
                name = re.sub(r'\d+\.\d+\s+out\s+of\s+\d+\s+stars.*$', '', name).strip()
                name = re.sub(r'\(\d+\).*$', '', name).strip()
            
            price = self._extract_text(soup, self.selectors['product_price'])
            brand = self._extract_text(soup, self.selectors['product_brand'])
            
            # Try multiple selectors for description to get comprehensive info
            description = self._extract_comprehensive_description(soup)
            
            # Extract SKU from URL
            sku = self._extract_sku_from_url(product_url)
            
            # Extract image URL
            image_url = self._extract_image_url(soup)
            
            # Extract specifications
            specifications = self._extract_specifications(soup)
            
            if not name:
                logger.warning(f"No product name found for {product_url}")
                return None
            
            # Clean up data
            name = self._clean_text(name)
            brand = self._clean_text(brand) if brand else 'Unknown'
            price = self._clean_text(price) if price else None
            description = self._clean_text(description) if description else None
            
            return ProductData(
                name=name,
                brand=brand,
                price=price,
                url=product_url,
                sku=sku,
                category=category_name,
                image_url=image_url,
                description=description,
                specifications=specifications
            )
            
        except Exception as e:
            logger.error(f"Error extracting product details from {product_url}: {e}")
            return None
    
    def _extract_text(self, soup: BeautifulSoup, selector: str) -> Optional[str]:
        """Extract text from element using selector"""
        try:
            element = soup.select_one(selector)
            return element.get_text(strip=True) if element else None
        except Exception:
            return None
    
    def _extract_comprehensive_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract comprehensive product description for OpenAI processing"""
        try:
            description_parts = []
            
            # Try multiple selectors to get comprehensive description
            description_selectors = [
                '.fx-product-description',
                '.fx-product-text', 
                '.product-description',
                '.product-details',
                '.fx-product-highlights',
                '.product-features',
                '.product-summary',
                '[data-testid="description"]'
            ]
            
            for selector in description_selectors:
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text(strip=True)
                    if text and len(text) > 20 and text not in description_parts:
                        description_parts.append(text)
            
            # Also try to get key product details from structured data
            key_details = []
            
            # Look for product specifications or bullet points
            specs_selectors = ['.product-specs li', '.features li', '.highlights li', '.fx-list li']
            for selector in specs_selectors:
                elements = soup.select(selector)
                for element in elements[:5]:  # Limit to first 5 specs
                    text = element.get_text(strip=True)
                    if text and len(text) > 10:
                        key_details.append(text)
            
            # Combine all description parts
            final_description = []
            
            if description_parts:
                final_description.extend(description_parts)
            
            if key_details:
                final_description.append("Key features: " + "; ".join(key_details))
            
            if final_description:
                full_text = " | ".join(final_description)
                # Limit to reasonable length for OpenAI processing
                return full_text[:1500] if len(full_text) > 1500 else full_text
            
            return None
            
        except Exception as e:
            logger.warning(f"Error extracting comprehensive description: {e}")
            return None
    
    def _extract_sku_from_url(self, url: str) -> str:
        """Extract SKU from product URL - optimized for Thomann URLs"""
        try:
            # Thomann URLs typically end with the product identifier
            # e.g., https://www.thomann.co.uk/hemingway_dp_501_mkii_at.html
            clean_url = url.split('?')[0].split('#')[0]  # Remove query params and fragments
            
            # Extract filename without .html/.htm
            filename = clean_url.split('/')[-1].replace('.html', '').replace('.htm', '')
            
            # Use the filename as SKU (it's unique for each product on Thomann)
            if filename and len(filename) > 3:
                return filename
            
            # Fallback: use a hash of the URL
            return f"sku_{abs(hash(clean_url)) % 10000000}"  # 7-digit SKU
            
        except Exception:
            return f"sku_{str(uuid.uuid4())[:8]}"
    
    def _extract_image_url(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract main product image URL - optimized for Thomann"""
        try:
            # Priority selectors for Thomann product images
            selectors_priority = [
                '.navigator__item-image.fx-image',  # Main product navigator image
                '.navigator__item-image',           # Navigator images
                '.fx-image[src*="static-thomann"]', # Any Thomann image
                '.product-image img',               # Generic product images
                '.gallery-image img',               # Gallery images
                'img[src*="static-thomann"]'       # Any img with Thomann URL
            ]
            
            for selector in selectors_priority:
                img = soup.select_one(selector)
                if img:
                    src = img.get('src') or img.get('data-src')
                    if src and 'static-thomann' in src:
                        # Make URL absolute
                        if src.startswith('//'):
                            src = f"https:{src}"
                        elif src.startswith('/'):
                            src = f"https://www.thomann.co.uk{src}"
                        # Convert thumbnail to larger image if possible
                        if 'thumb80x80' in src:
                            src = src.replace('thumb80x80', 'original')
                        elif '_800.jpg' in src:
                            src = src  # Keep 800px version
                        return src
            
            # Fallback: try to find any product image
            all_images = soup.select('img[src*="static-thomann"], img[src*="thomann"]')
            for img in all_images:
                src = img.get('src')
                if src and any(keyword in src for keyword in ['product', 'pics', 'bdb']):
                    if src.startswith('//'):
                        src = f"https:{src}"
                    elif src.startswith('/'):
                        src = f"https://www.thomann.co.uk{src}"
                    return src
                        
            return None
        except Exception as e:
            logger.warning(f"Error extracting image URL: {e}")
            return None
    
    def _extract_specifications(self, soup: BeautifulSoup) -> Optional[Dict]:
        """Extract product specifications"""
        try:
            specs = {}
            
            # Look for specification tables or lists
            spec_tables = soup.select('.specifications table, .product-specs table, .tech-specs table')
            for table in spec_tables:
                rows = table.select('tr')
                for row in rows:
                    cells = row.select('td, th')
                    if len(cells) >= 2:
                        key = cells[0].get_text(strip=True)
                        value = cells[1].get_text(strip=True)
                        if key and value:
                            specs[key] = value
            
            # Look for specification lists
            spec_lists = soup.select('.specifications li, .product-specs li, .tech-specs li')
            for item in spec_lists:
                text = item.get_text(strip=True)
                if ':' in text:
                    key, value = text.split(':', 1)
                    specs[key.strip()] = value.strip()
            
            return specs if specs else None
            
        except Exception:
            return None
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove common unwanted characters
        text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        
        return text.strip()

async def main():
    """Main function to run the crawler"""
    try:
        logger.info("🚀 Starting Simple Product Crawler...")
        
        async with SimpleProductCrawler() as crawler:
            results = await crawler.crawl_all_products()
            
            # Show results
            logger.info("\n✅ CRAWLING CONCLUÍDO!")
            logger.info("=" * 50)
            
            total_products = 0
            for category, products in results.items():
                logger.info(f"📦 {category}: {len(products)} produtos")
                total_products += len(products)
                
                # Show some examples
                for product in products[:3]:
                    logger.info(f"   - {product.name} ({product.brand}) - {product.price or 'N/A'}")
                if len(products) > 3:
                    logger.info(f"   ... e mais {len(products) - 3} produtos")
                logger.info("")
            
            logger.info(f"🎯 TOTAL: {total_products} produtos crawleados!")
            logger.info("=" * 50)
            
    except KeyboardInterrupt:
        logger.info("\n⏹️ Crawler interrompido pelo usuário")
    except Exception as e:
        logger.error(f"\n❌ Erro durante o crawling: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
