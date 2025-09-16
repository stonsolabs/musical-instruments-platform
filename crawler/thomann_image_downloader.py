#!/usr/bin/env python3
"""
Thomann Image Downloader Service
Downloads product images from Thomann product pages and uploads them to Azure Storage
Updates the database with the image paths
"""

import asyncio
import aiohttp
import json
import os
import time
import uuid
import random
import subprocess
import re
from typing import List, Dict, Any, Optional, Tuple, Set
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Import existing managers
from database_manager import DatabaseManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ThomannImageDownloader:
    """Downloads product images from Thomann and uploads to Azure Storage"""
    
    def __init__(self, max_concurrent: int = 10, test_mode: bool = False):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.session = None
        self.db = None
        self.test_mode = test_mode
        self.images_downloaded = 0
        self.images_uploaded = 0
        self.successful_downloads = 0
        self.failed_downloads = 0
        self.errors = 0
        
        # Load environment variables
        load_dotenv()
        
        # Proxy configuration
        self.proxy_url = os.getenv('IPROYAL_PROXY_URL')
        if not self.proxy_url:
            raise ValueError("IPROYAL_PROXY_URL environment variable is required")
        
        # Azure Storage configuration - use AZURE_BLOB_CONTAINER from .env
        self.azure_connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        self.azure_container_name = os.getenv('AZURE_BLOB_CONTAINER', 'product-images')
        
        if not self.azure_connection_string:
            raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable is required")
        
        # Initialize Azure Blob Service
        self.blob_service_client = BlobServiceClient.from_connection_string(self.azure_connection_string)
        self.container_client = self.blob_service_client.get_container_client(self.azure_container_name)
        
        # Image selectors for Thomann pages
        self.image_selectors = [
            'picture.ZoomImagePicture img.ZoomCurrentImage',  # Primary selector
            'picture.ZoomImagePicture img',  # Fallback to any img in ZoomImagePicture
            '.spotlight__item-image',  # Alternative selector
            '.fx-image',  # Another alternative
            'meta[property="og:image"]',  # Open Graph meta tag
        ]
        
        # Anti-blocking configuration
        self.delay_min = 2.0  # Minimum delay between requests
        self.delay_max = 5.0  # Maximum delay between requests
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0'
        ]
        
        logger.info(f"🔧 Image Downloader initialized with {max_concurrent} concurrent downloads")
        logger.info(f"📦 Azure Storage Container: {self.azure_container_name}")
        logger.info(f"🛡️  Anti-blocking delays: {self.delay_min}-{self.delay_max}s between requests")
        
        # Cache for existing product IDs in blob storage
        self.existing_blob_products: Optional[Set[int]] = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        # Setup session with proxy support
        connector = aiohttp.TCPConnector(
            limit=50,
            limit_per_host=10,
            ttl_dns_cache=300,
            use_dns_cache=True,
            keepalive_timeout=30,
            enable_cleanup_closed=True
        )
        timeout = aiohttp.ClientTimeout(total=30, connect=10, sock_read=20)
        
        # Configure proxy
        proxy = None
        if self.proxy_url:
            proxy = self.proxy_url
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9,de;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0',
            }
        )
        
        # Initialize database connection
        self.db = DatabaseManager()
        await self.db.__aenter__()
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
        if self.db:
            await self.db.__aexit__(exc_type, exc_val, exc_tb)
    
    def load_existing_blob_products(self) -> Set[int]:
        """Load product IDs that already have images in blob storage"""
        if self.existing_blob_products is not None:
            return self.existing_blob_products
        
        logger.info("📋 Loading existing products from blob storage...")
        
        try:
            # Use Azure CLI to list blobs (faster than SDK for this use case)
            result = subprocess.run([
                'az', 'storage', 'blob', 'list',
                '--container-name', self.azure_container_name,
                '--account-name', 'getyourmusicgear',
                '--query', '[].name',
                '--output', 'json'
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode != 0:
                logger.warning(f"⚠️ Could not load blob storage (using empty set): {result.stderr}")
                self.existing_blob_products = set()
                return self.existing_blob_products
            
            blob_names = json.loads(result.stdout)
            existing_ids = set()
            
            for blob_name in blob_names:
                if blob_name.startswith('thomann/'):
                    filename = blob_name[8:]  # Remove 'thomann/' prefix
                    
                    # Extract product ID using pattern: {product_id}_{timestamp}.jpg
                    match = re.match(r'^(\d+)_', filename)
                    if match:
                        product_id = int(match.group(1))
                        existing_ids.add(product_id)
            
            self.existing_blob_products = existing_ids
            logger.info(f"✅ Found {len(existing_ids)} products with existing images in blob storage")
            return existing_ids
            
        except Exception as e:
            logger.warning(f"⚠️ Error loading blob storage (using empty set): {e}")
            self.existing_blob_products = set()
            return self.existing_blob_products
    
    def load_existing_blob_files(self) -> Set[str]:
        """Load all existing blob file names from Azure storage"""
        logger.info("📋 Loading existing blob files from storage...")
        
        try:
            result = subprocess.run([
                'az', 'storage', 'blob', 'list',
                '--container-name', self.azure_container_name,
                '--account-name', 'getyourmusicgear',
                '--query', '[].name',
                '--output', 'json'
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode != 0:
                logger.warning(f"⚠️ Could not load blob files (using empty set): {result.stderr}")
                return set()
            
            blob_names = json.loads(result.stdout)
            blob_files = set(blob_names)
            logger.info(f"✅ Found {len(blob_files)} total blob files in storage")
            return blob_files
            
        except Exception as e:
            logger.warning(f"⚠️ Error loading blob files (using empty set): {e}")
            return set()
    
    def product_needs_image_processing(self, product_row, existing_blob_files: Set[str]) -> bool:
        """Check if a product needs image processing (no images OR broken links)"""
        product_id = product_row['id']
        images = product_row['images']
        
        # Case 1: No images in database
        if (images is None or 
            images == '{}' or 
            images == 'null' or 
            (isinstance(images, dict) and not images) or
            (isinstance(images, dict) and not images.get('thomann_main'))):
            return True
        
        # Case 2: Images in database but check if files exist in blob storage
        if isinstance(images, str):
            try:
                images = json.loads(images)
            except:
                return True  # Corrupted JSON = needs processing
        
        if isinstance(images, dict):
            thomann_main = images.get('thomann_main')
            if thomann_main:
                # Handle case where thomann_main might be a dict or string
                image_url = thomann_main
                if isinstance(thomann_main, dict):
                    image_url = thomann_main.get('url', '')
                
                if isinstance(image_url, str) and image_url:
                    # Extract blob name from URL
                    match = re.search(r'/product-images/(.+)$', image_url)
                    if match:
                        blob_name = match.group(1)
                        if blob_name in existing_blob_files:
                            return False  # Image exists, no processing needed
                        else:
                            return True   # Broken link, needs processing
                    else:
                        return True  # Invalid URL format
                else:
                    return True  # Invalid image URL
            else:
                return True  # No thomann_main field
        else:
            return True  # Invalid images format
    
    async def get_products_with_thomann_links(self) -> List[Dict[str, Any]]:
        """Get products that need image processing (no images OR broken image links)"""
        if not self.db.conn:
            logger.error("❌ Database connection not available")
            return []
        
        # Load existing blob files (not just product IDs)
        existing_blob_files = self.load_existing_blob_files()
        
        try:
            # Query ALL products with Thomann links (including those with existing image records)
            query = """
                SELECT p.id, p.sku, p.name, p.content, p.images
                FROM products p
                WHERE p.content->>'store_links' IS NOT NULL
                AND p.content->'store_links'->>'Thomann' IS NOT NULL
                ORDER BY p.updated_at DESC
            """
            
            rows = await self.db.conn.fetch(query)
            products = []
            skipped_valid_images = 0
            skipped_no_url_count = 0
            
            for row in rows:
                product_id = row['id']
                
                # Parse content if it's a string, otherwise use as dict
                content = row['content'] or {}
                if isinstance(content, str):
                    try:
                        content = json.loads(content)
                    except (json.JSONDecodeError, TypeError):
                        content = {}
                
                store_links = content.get('store_links', {})
                thomann_url = store_links.get('Thomann')
                
                if not thomann_url:
                    skipped_no_url_count += 1
                    continue
                
                # Check if product needs processing
                needs_processing = self.product_needs_image_processing(row, existing_blob_files)
                
                if needs_processing:
                    products.append({
                        'id': row['id'],
                        'sku': row['sku'],
                        'name': row['name'],
                        'thomann_url': thomann_url,
                        'content': content,
                        'images': row['images'] or {}
                    })
                else:
                    skipped_valid_images += 1
            
            logger.info(f"📊 ENHANCED PRODUCT FILTERING RESULTS:")
            logger.info(f"   🎯 Total products from DB: {len(rows)}")
            logger.info(f"   ✅ Valid images (skipped): {skipped_valid_images}")
            logger.info(f"   ❌ No Thomann URL: {skipped_no_url_count}")
            logger.info(f"   📥 Need processing: {len(products)}")
            
            return products
            
        except Exception as e:
            logger.error(f"❌ Error querying products: {e}")
            return []
    
    def _get_random_headers(self, referer: str = None) -> Dict[str, str]:
        """Generate random headers to avoid detection"""
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,de;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
        }
        
        if referer:
            headers['Referer'] = referer
        
        return headers
    
    async def _add_random_delay(self):
        """Add random delay between requests to avoid rate limiting"""
        delay = random.uniform(self.delay_min, self.delay_max)
        await asyncio.sleep(delay)
    
    async def download_product_image(self, product: Dict[str, Any]) -> Optional[Tuple[bytes, str]]:
        """
        Download the main product image from Thomann
        
        Args:
            product: Product dictionary with thomann_url
            
        Returns:
            Tuple of (image_data, image_url) or None if failed
        """
        thomann_url = product['thomann_url']
        product_name = product['name']
        
        async with self.semaphore:
            try:
                logger.info(f"🔍 Downloading image for: {product_name}")
                
                # Add random delay to avoid rate limiting
                await self._add_random_delay()
                
                # First, simulate browsing from Thomann homepage to avoid direct access detection
                thomann_homepage = "https://www.thomann.co.uk"
                homepage_headers = self._get_random_headers()
                
                logger.info(f"🏠 Simulating browse from homepage to: {thomann_url}")
                
                # Fetch the product page with proper referer and headers
                page_headers = self._get_random_headers(thomann_homepage)
                
                async with self.session.get(thomann_url, headers=page_headers, proxy=self.proxy_url) as response:
                    if response.status != 200:
                        logger.warning(f"⚠️  HTTP {response.status} for {thomann_url}")
                        return None
                    
                    html_content = await response.text()
                
                # Parse the HTML
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Find the main product image
                image_url = None
                for selector in self.image_selectors:
                    if selector.startswith('meta'):
                        meta_tag = soup.select_one(selector)
                        if meta_tag and meta_tag.get('content'):
                            image_url = meta_tag['content']
                            break
                    else:
                        img_tag = soup.select_one(selector)
                        if img_tag and img_tag.get('src'):
                            image_url = img_tag['src']
                            break
                
                if not image_url:
                    logger.warning(f"⚠️  No image found for {product_name}")
                    return None
                
                # Make sure we have an absolute URL
                if not image_url.startswith('http'):
                    image_url = urljoin(thomann_url, image_url)
                
                logger.info(f"✅ Found image URL: {image_url}")
                
                # Add another small delay before downloading image
                await asyncio.sleep(random.uniform(1.0, 2.0))
                
                # Download the image with proper referer to simulate coming from the product page
                img_headers = self._get_random_headers(thomann_url)
                img_headers.update({
                    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                    'Sec-Fetch-Dest': 'image',
                    'Sec-Fetch-Mode': 'no-cors',
                    'Sec-Fetch-Site': 'cross-site',
                })
                
                async with self.session.get(image_url, headers=img_headers, proxy=self.proxy_url) as img_response:
                    if img_response.status != 200:
                        logger.warning(f"⚠️  Failed to download image: HTTP {img_response.status}")
                        return None
                    
                    image_data = await img_response.read()
                    logger.info(f"⬇️  Downloaded {len(image_data)} bytes for {product_name}")
                    
                    return image_data, image_url
                    
            except Exception as e:
                logger.error(f"❌ Error downloading image for {product_name}: {e}")
                return None
    
    async def upload_to_azure_storage(self, image_data: bytes, product: Dict[str, Any]) -> Optional[str]:
        """
        Upload image to Azure Blob Storage
        
        Args:
            image_data: Raw image data
            product: Product dictionary
            
        Returns:
            Blob URL if successful, None otherwise
        """
        try:
            # Generate unique blob name using product ID for easy database association
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            product_id = product['id']
            file_extension = 'jpg'  # Default to jpg
            
            # Use product ID in filename for easy database association
            blob_name = f"thomann/{product_id}_{timestamp}.{file_extension}"
            
            # Get blob client
            blob_client = self.container_client.get_blob_client(blob_name)
            
            # Upload the image
            blob_client.upload_blob(image_data, overwrite=True, content_settings=None)
            
            # Get the blob URL
            blob_url = blob_client.url
            
            logger.info(f"☁️  Uploaded image to Azure: {blob_name}")
            logger.info(f"🔗 Easy DB association: product_id={product_id}")
            return blob_url
            
        except Exception as e:
            logger.error(f"❌ Error uploading to Azure Storage: {e}")
            return None
    
    async def update_database_image_path(self, product_id: int, image_url: str, thomann_url: str) -> bool:
        """
        Update the database with the new image path
        
        Args:
            product_id: Product ID in database
            image_url: Azure blob URL
            thomann_url: Original Thomann URL for reference
            
        Returns:
            True if successful, False otherwise
        """
        if not self.db.conn:
            logger.error("❌ Database connection not available")
            return False
        
        try:
            # Update the images column with the new image
            update_query = """
                UPDATE products 
                SET images = jsonb_set(
                    COALESCE(images, '{}'::jsonb), 
                    '{thomann_main}', 
                    $1::jsonb
                ),
                updated_at = NOW()
                WHERE id = $2
            """
            
            image_data = json.dumps({
                "url": image_url,
                "source": "thomann",
                "source_url": thomann_url,
                "downloaded_at": datetime.utcnow().isoformat(),
                "type": "main"
            })
            
            await self.db.conn.execute(update_query, image_data, product_id)
            
            logger.info(f"💾 Updated database for product {product_id} with image path")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error updating database: {e}")
            return False
    
    async def process_single_product(self, product: Dict[str, Any]) -> bool:
        """
        Process a single product: download image, upload to Azure, update database
        
        Args:
            product: Product dictionary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Download image
            image_result = await self.download_product_image(product)
            if not image_result:
                return False
            
            image_data, original_image_url = image_result
            self.images_downloaded += 1
            
            # Upload to Azure Storage
            azure_url = await self.upload_to_azure_storage(image_data, product)
            if not azure_url:
                return False
            
            self.images_uploaded += 1
            
            # Update database
            success = await self.update_database_image_path(
                product['id'], 
                azure_url, 
                product['thomann_url']
            )
            
            if success:
                logger.info(f"✅ Successfully processed {product['name']}")
                return True
            else:
                return False
                
        except Exception as e:
            logger.error(f"❌ Error processing product {product['name']}: {e}")
            self.errors += 1
            return False
    
    async def worker(self, name: str, queue: asyncio.Queue):
        """
        Worker that processes products from the queue
        """
        logger.info(f"🔧 {name} started")
        
        while True:
            try:
                # Get a product from the queue with timeout
                product = await asyncio.wait_for(queue.get(), timeout=1.0)
                
                logger.info(f"🔨 {name} processing: {product['name'][:50]}...")
                
                success = await self.process_single_product(product)
                
                if success:
                    self.successful_downloads += 1
                    logger.info(f"✅ {name} completed: {product['name'][:50]}...")
                else:
                    self.failed_downloads += 1
                    logger.error(f"❌ {name} failed: {product['name'][:50]}...")
                
                # Mark task as done
                queue.task_done()
                
            except asyncio.TimeoutError:
                # No more work available, exit gracefully
                logger.info(f"🏁 {name} finished - no more work")
                break
            except asyncio.CancelledError:
                logger.info(f"🛑 {name} cancelled")
                break
            except Exception as e:
                logger.error(f"❌ {name} error: {e}")
                queue.task_done()
    
    async def auto_scale_down(self):
        """Scale down the Container App to 0 replicas when done"""
        try:
            logger.info("📉 Auto-scaling Container App to 0 replicas...")
            
            import subprocess
            result = subprocess.run([
                'az', 'containerapp', 'update',
                '--name', 'thomann-image-downloader',
                '--resource-group', 'getyourmusicgear',
                '--min-replicas', '0'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ Successfully scaled down to 0 replicas")
            else:
                logger.warning(f"⚠️ Failed to scale down: {result.stderr}")
                
        except Exception as e:
            logger.warning(f"⚠️ Auto-scale down failed: {e}")
    
    async def run(self, max_products: Optional[int] = None):
        """
        Main run method to process all products with proper concurrency control
        
        Args:
            max_products: Maximum number of products to process (None for all)
        """
        logger.info("🚀 Starting Thomann Image Downloader")
        
        # Get products that need images (only those without images)
        products = await self.get_products_with_thomann_links()
        
        if not products:
            logger.info("✅ No products found that need images")
            await self.auto_scale_down()
            return
        
        if max_products:
            products = products[:max_products]
            logger.info(f"🔢 Processing first {max_products} products")
        
        logger.info(f"📋 Processing {len(products)} products with {self.max_concurrent} concurrent workers")
        
        # Use asyncio.Queue for proper work distribution
        work_queue = asyncio.Queue()
        
        # Add all products to the queue
        for product in products:
            await work_queue.put(product)
        
        # Create worker tasks that will consume from the queue
        workers = []
        for i in range(min(self.max_concurrent, len(products))):
            worker = asyncio.create_task(self.worker(f"worker-{i+1}", work_queue))
            workers.append(worker)
        
        # Wait for all work to be done
        await work_queue.join()
        
        # Cancel all workers
        for worker in workers:
            worker.cancel()
        
        # Wait for workers to finish cancellation
        await asyncio.gather(*workers, return_exceptions=True)
        
        logger.info("🏁 Image downloader completed!")
        logger.info(f"📊 Summary:")
        logger.info(f"   ✅ Successful: {self.successful_downloads}")
        logger.info(f"   ❌ Failed: {self.failed_downloads}")
        logger.info(f"   📥 Total downloaded: {self.images_downloaded}")
        
        # Auto-scale down when done
        await self.auto_scale_down()
        logger.info(f"   ☁️  Uploaded: {self.images_uploaded}")
        logger.info(f"   🚫 Errors: {self.errors}")

async def main():
    """Main function for production"""
    # Read environment variables
    max_concurrent = int(os.getenv('MAX_CONCURRENT_DOWNLOADS', '10'))
    test_mode = os.getenv('TEST_MODE', 'false').lower() == 'true'
    max_products = int(os.getenv('MAX_TEST_PRODUCTS', '0')) if test_mode else None
    
    logger.info(f"🚀 Starting with max_concurrent={max_concurrent}, test_mode={test_mode}")
    
    async with ThomannImageDownloader(max_concurrent=max_concurrent, test_mode=test_mode) as downloader:
        await downloader.run(max_products=max_products)

if __name__ == "__main__":
    asyncio.run(main())
