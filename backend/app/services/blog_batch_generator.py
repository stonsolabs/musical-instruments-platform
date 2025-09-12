"""
Azure OpenAI Batch API Blog Generation Service
"""

import asyncio
import json
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging
import os
from pathlib import Path
import tempfile

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import openai
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import AzureError

from app.blog_ai_schemas import BlogGenerationRequest, BlogGenerationTemplate
from app.services.blog_prompt_templates import BlogPromptBuilder

logger = logging.getLogger(__name__)

class BlogBatchGenerator:
    """
    Gerador de blog posts em lote usando Azure OpenAI Batch API
    """
    
    def __init__(self, db_session: AsyncSession, admin_email: Optional[str] = None):
        self.db = db_session
        self.admin_email = admin_email
        
        # Azure OpenAI configuration
        self.client = openai.AsyncOpenAI(
            api_key=os.getenv('AZURE_OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY'),
            azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
            api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2024-07-01-preview')
        )
        self.deployment_name = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', 'gpt-4.1')
        
        # Azure Storage configuration
        storage_connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        storage_account_name = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
        storage_account_key = os.getenv('AZURE_STORAGE_ACCOUNT_KEY')
        
        if storage_connection_string:
            self.blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
        elif storage_account_name and storage_account_key:
            self.blob_service_client = BlobServiceClient(
                account_url=f"https://{storage_account_name}.blob.core.windows.net",
                credential=storage_account_key
            )
        else:
            logger.warning("Azure Storage credentials not found. Files will be stored locally.")
            self.blob_service_client = None
        
        self.container_name = os.getenv('AZURE_STORAGE_CONTAINER', 'blog-batch-files')
        self.prompt_builder = BlogPromptBuilder()
        
        # Local storage fallback
        self.local_storage_path = Path(tempfile.gettempdir()) / "blog_batch_files"
        self.local_storage_path.mkdir(exist_ok=True)
    
    async def create_batch_generation_request(
        self, 
        generation_requests: List[BlogGenerationRequest],
        batch_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Cria um arquivo de batch para geração de múltiplos blog posts
        """
        try:
            batch_name = batch_name or f"blog_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            batch_id = str(uuid.uuid4())
            
            # Preparar requests para o batch
            batch_requests = []
            generation_metadata = []
            
            for i, request in enumerate(generation_requests):
                # Buscar template e produtos
                template = await self._get_template(request.template_id)
                if not template:
                    logger.error(f"Template {request.template_id} não encontrado")
                    continue
                
                products = await self._select_relevant_products(
                    request.product_ids,
                    template,
                    request.category_id
                )
                
                # Construir prompt
                custom_variables = {
                    'category': request.category_id or 'musical instruments',
                    'product_count': len(products),
                    'year': datetime.now().year
                }
                
                prompt_data = self.prompt_builder.build_prompt(
                    template['template_type'],
                    products,
                    custom_variables,
                    request.target_word_count
                )
                
                # Criar request para batch API
                batch_request = {
                    "custom_id": f"blog_post_{batch_id}_{i}",
                    "method": "POST",
                    "url": "/chat/completions",
                    "body": {
                        "model": self.deployment_name,
                        "messages": [
                            {"role": "system", "content": prompt_data["system_prompt"]},
                            {"role": "user", "content": prompt_data["user_prompt"]}
                        ],
                        "temperature": request.generation_params.get("temperature", 0.7),
                        "max_tokens": request.generation_params.get("max_tokens", 3000),
                        "response_format": {"type": "json_object"}
                    }
                }
                
                batch_requests.append(batch_request)
                
                # Guardar metadata para processamento posterior
                generation_metadata.append({
                    "custom_id": batch_request["custom_id"],
                    "request_index": i,
                    "template_id": request.template_id,
                    "template_type": template['template_type'],
                    "category_id": request.category_id,
                    "products": [{"id": p["id"], "name": p["name"]} for p in products],
                    "original_request": request.dict(),
                    "prompt_used": prompt_data["user_prompt"]
                })
            
            # Preparar dados dos arquivos
            batch_content = '\n'.join([json.dumps(req, ensure_ascii=False) for req in batch_requests])
            
            metadata = {
                "batch_id": batch_id,
                "batch_name": batch_name,
                "created_at": datetime.utcnow().isoformat(),
                "created_by": self.admin_email,
                "total_requests": len(batch_requests),
                "generation_metadata": generation_metadata,
                "deployment_name": self.deployment_name
            }
            
            metadata_content = json.dumps(metadata, indent=2, ensure_ascii=False)
            
            # Salvar arquivos (Azure Storage ou local)
            batch_file_path = await self._save_file(f"{batch_name}.jsonl", batch_content)
            metadata_file_path = await self._save_file(f"{batch_name}_metadata.json", metadata_content)
            
            # Atualizar metadata com paths
            metadata["file_paths"] = {
                "batch_file": batch_file_path,
                "metadata_file": metadata_file_path
            }
            
            # Registrar no banco de dados
            batch_record_id = await self._create_batch_record(
                batch_id, 
                batch_name, 
                len(batch_requests),
                batch_file_path,
                metadata_file_path,
                metadata
            )
            
            logger.info(f"Batch criado: {batch_name} com {len(batch_requests)} requests")
            
            return {
                "success": True,
                "batch_id": batch_id,
                "batch_name": batch_name,
                "batch_record_id": batch_record_id,
                "total_requests": len(batch_requests),
                "batch_file_path": batch_file_path,
                "metadata_file_path": metadata_file_path,
                "next_steps": [
                    "1. Fazer upload do arquivo para Azure OpenAI",
                    "2. Criar batch job no Azure OpenAI",
                    "3. Aguardar processamento",
                    "4. Fazer download dos resultados",
                    "5. Processar resultados com process_batch_results()"
                ]
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar batch: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _save_file(self, filename: str, content: str) -> str:
        """
        Salva arquivo no Azure Storage ou localmente
        """
        try:
            if self.blob_service_client:
                # Salvar no Azure Storage
                blob_name = f"batch_files/{filename}"
                blob_client = self.blob_service_client.get_blob_client(
                    container=self.container_name,
                    blob=blob_name
                )
                
                # Upload do conteúdo
                await asyncio.get_event_loop().run_in_executor(
                    None,
                    blob_client.upload_blob,
                    content.encode('utf-8'),
                    True  # overwrite
                )
                
                return f"azure://{self.container_name}/{blob_name}"
            else:
                # Salvar localmente
                file_path = self.local_storage_path / filename
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return str(file_path)
                
        except Exception as e:
            logger.error(f"Erro ao salvar arquivo {filename}: {e}")
            # Fallback para local
            file_path = self.local_storage_path / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return str(file_path)
    
    async def _load_file(self, file_path: str) -> str:
        """
        Carrega arquivo do Azure Storage ou local
        """
        try:
            if file_path.startswith('azure://'):
                # Carregar do Azure Storage
                container, blob_name = file_path.replace('azure://', '').split('/', 1)
                blob_client = self.blob_service_client.get_blob_client(
                    container=container,
                    blob=blob_name
                )
                
                download_stream = await asyncio.get_event_loop().run_in_executor(
                    None,
                    blob_client.download_blob
                )
                return download_stream.readall().decode('utf-8')
            else:
                # Carregar localmente
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
                    
        except Exception as e:
            logger.error(f"Erro ao carregar arquivo {file_path}: {e}")
            raise
    
    async def _save_binary_file(self, filename: str, content: bytes) -> str:
        """
        Salva arquivo binário no Azure Storage ou localmente
        """
        try:
            if self.blob_service_client:
                # Salvar no Azure Storage
                blob_name = f"batch_results/{filename}"
                blob_client = self.blob_service_client.get_blob_client(
                    container=self.container_name,
                    blob=blob_name
                )
                
                await asyncio.get_event_loop().run_in_executor(
                    None,
                    blob_client.upload_blob,
                    content,
                    True  # overwrite
                )
                
                return f"azure://{self.container_name}/{blob_name}"
            else:
                # Salvar localmente
                file_path = self.local_storage_path / filename
                with open(file_path, 'wb') as f:
                    f.write(content)
                return str(file_path)
                
        except Exception as e:
            logger.error(f"Erro ao salvar arquivo binário {filename}: {e}")
            # Fallback para local
            file_path = self.local_storage_path / filename
            with open(file_path, 'wb') as f:
                f.write(content)
            return str(file_path)

    async def upload_batch_to_azure(self, batch_file_path: str) -> Dict[str, Any]:
        """
        Faz upload do arquivo de batch para Azure OpenAI
        """
        try:
            # Carregar conteúdo do arquivo
            batch_content = await self._load_file(batch_file_path)
            
            # Criar arquivo temporário para upload
            with tempfile.NamedTemporaryFile(mode='w+b', suffix='.jsonl', delete=False) as temp_file:
                temp_file.write(batch_content.encode('utf-8'))
                temp_file_path = temp_file.name
            
            try:
                # Upload do arquivo para OpenAI
                with open(temp_file_path, 'rb') as file:
                    file_upload_response = await self.client.files.create(
                        file=file,
                        purpose="batch"
                    )
            finally:
                # Limpar arquivo temporário
                os.unlink(temp_file_path)
            
            logger.info(f"Arquivo uploadado: {file_upload_response.id}")
            
            return {
                "success": True,
                "file_id": file_upload_response.id,
                "filename": file_upload_response.filename,
                "bytes": file_upload_response.bytes,
                "status": file_upload_response.status
            }
            
        except Exception as e:
            logger.error(f"Erro no upload: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def create_azure_batch_job(self, file_id: str, batch_name: str) -> Dict[str, Any]:
        """
        Cria um job de batch no Azure OpenAI
        """
        try:
            # Criar batch job
            batch_response = await self.client.batches.create(
                input_file_id=file_id,
                endpoint="/chat/completions",
                completion_window="24h",
                metadata={
                    "description": f"Blog post generation batch: {batch_name}",
                    "created_by": "blog_batch_generator"
                }
            )
            
            # Atualizar registro no banco
            await self._update_batch_record_with_job(batch_name, {
                "azure_batch_id": batch_response.id,
                "status": batch_response.status,
                "input_file_id": file_id,
                "created_at": batch_response.created_at
            })
            
            logger.info(f"Batch job criado: {batch_response.id}")
            
            return {
                "success": True,
                "batch_id": batch_response.id,
                "status": batch_response.status,
                "input_file_id": batch_response.input_file_id,
                "created_at": batch_response.created_at,
                "completion_window": batch_response.completion_window
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar batch job: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def check_batch_status(self, azure_batch_id: str) -> Dict[str, Any]:
        """
        Verifica o status de um batch job no Azure
        """
        try:
            batch = await self.client.batches.retrieve(azure_batch_id)
            
            return {
                "success": True,
                "batch_id": batch.id,
                "status": batch.status,
                "created_at": batch.created_at,
                "completed_at": batch.completed_at,
                "failed_at": batch.failed_at,
                "request_counts": {
                    "total": batch.request_counts.total if batch.request_counts else 0,
                    "completed": batch.request_counts.completed if batch.request_counts else 0,
                    "failed": batch.request_counts.failed if batch.request_counts else 0
                },
                "output_file_id": batch.output_file_id,
                "error_file_id": batch.error_file_id
            }
            
        except Exception as e:
            logger.error(f"Erro ao verificar status: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def download_batch_results(self, azure_batch_id: str, output_file_id: str) -> Dict[str, Any]:
        """
        Faz download dos resultados do batch
        """
        try:
            # Download do arquivo de resultados
            file_response = await self.client.files.content(output_file_id)
            
            # Salvar arquivo no Azure Storage ou localmente
            filename = f"results_{azure_batch_id}.jsonl"
            results_file_path = await self._save_binary_file(filename, file_response.content)
            
            # Contar resultados
            results_content = await self._load_file(results_file_path)
            result_count = len([line for line in results_content.split('\n') if line.strip()])
            
            logger.info(f"Resultados baixados: {result_count} respostas em {results_file_path}")
            
            return {
                "success": True,
                "results_file_path": results_file_path,
                "result_count": result_count
            }
            
        except Exception as e:
            logger.error(f"Erro ao baixar resultados: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def process_batch_results(
        self, 
        results_file_path: str, 
        metadata_file_path: str,
        auto_publish: bool = False
    ) -> Dict[str, Any]:
        """
        Processa os resultados do batch e cria os blog posts
        """
        try:
            # Carregar metadata e resultados
            metadata_content = await self._load_file(metadata_file_path)
            metadata = json.loads(metadata_content)
            
            results_content = await self._load_file(results_file_path)
            
            # Processar resultados
            successful_posts = []
            failed_posts = []
            
            for line in results_content.split('\n'):
                if not line.strip():
                    continue
                
                try:
                    result = json.loads(line)
                    custom_id = result["custom_id"]
                    
                    # Encontrar metadata correspondente
                    gen_metadata = next(
                        (m for m in metadata["generation_metadata"] if m["custom_id"] == custom_id),
                        None
                    )
                    
                    if not gen_metadata:
                        logger.error(f"Metadata não encontrada para {custom_id}")
                        continue
                    
                    if result.get("response") and result["response"].get("body"):
                        # Sucesso - processar conteúdo
                        content = result["response"]["body"]["choices"][0]["message"]["content"]
                        parsed_content = json.loads(content)
                        
                        # Criar blog post
                        blog_post_id = await self._create_blog_post_from_batch_result(
                            parsed_content,
                            gen_metadata,
                            auto_publish
                        )
                        
                        successful_posts.append({
                            "custom_id": custom_id,
                            "blog_post_id": blog_post_id,
                            "title": parsed_content.get("title"),
                            "template_type": gen_metadata["template_type"]
                        })
                        
                    else:
                        # Falha
                        error_msg = result.get("error", {}).get("message", "Unknown error")
                        failed_posts.append({
                            "custom_id": custom_id,
                            "error": error_msg,
                            "template_type": gen_metadata.get("template_type")
                        })
                        
                except Exception as e:
                    logger.error(f"Erro ao processar resultado {line[:100]}...: {e}")
                    continue
            
            # Registrar histórico do batch
            await self._record_batch_processing_history(
                metadata["batch_id"],
                len(successful_posts),
                len(failed_posts),
                successful_posts,
                failed_posts
            )
            
            logger.info(f"Batch processado: {len(successful_posts)} sucessos, {len(failed_posts)} falhas")
            
            return {
                "success": True,
                "batch_id": metadata["batch_id"],
                "total_processed": len(successful_posts) + len(failed_posts),
                "successful_posts": successful_posts,
                "failed_posts": failed_posts,
                "success_rate": len(successful_posts) / max(len(successful_posts) + len(failed_posts), 1) * 100
            }
            
        except Exception as e:
            logger.error(f"Erro ao processar batch: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # Métodos auxiliares
    
    async def _get_template(self, template_id: int) -> Optional[Dict[str, Any]]:
        """Busca template do banco de dados"""
        query = """
        SELECT id, name, template_type, base_prompt, system_prompt, 
               product_context_prompt, required_product_types, min_products, 
               max_products, suggested_tags, content_structure
        FROM blog_generation_templates 
        WHERE id = :template_id AND is_active = true
        """
        
        result = await self.db.execute(text(query), {'template_id': template_id})
        row = result.fetchone()
        
        if not row:
            return None
            
        return dict(row._mapping)
    
    async def _select_relevant_products(
        self,
        requested_product_ids: List[int],
        template: Dict[str, Any],
        category_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Seleciona produtos relevantes para o batch"""
        if not requested_product_ids:
            return []
        
        query = """
        SELECT p.id, p.name, p.slug, p.description, p.avg_rating, 
               p.review_count, b.name as brand_name,
               c.name as category_name, c.slug as category_slug
        FROM products p
        LEFT JOIN brands b ON p.brand_id = b.id
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.id = ANY(:product_ids)
        ORDER BY p.featured DESC, p.avg_rating DESC
        """
        
        result = await self.db.execute(text(query), {'product_ids': requested_product_ids})
        return [dict(row._mapping) for row in result.fetchall()]
    
    async def _create_batch_record(
        self, 
        batch_id: str, 
        batch_name: str, 
        request_count: int,
        batch_file_path: str,
        metadata_file_path: str,
        metadata: Dict[str, Any]
    ) -> int:
        """Cria registro do batch no banco"""
        query = """
        INSERT INTO blog_batch_jobs (
            batch_id, batch_name, request_count, status, 
            batch_file_path, metadata_file_path, metadata, 
            created_by_email, created_at
        ) VALUES (
            :batch_id, :batch_name, :request_count, 'created', 
            :batch_file_path, :metadata_file_path, :metadata,
            :created_by_email, :created_at
        ) RETURNING id
        """
        
        result = await self.db.execute(text(query), {
            'batch_id': batch_id,
            'batch_name': batch_name,
            'request_count': request_count,
            'batch_file_path': batch_file_path,
            'metadata_file_path': metadata_file_path,
            'metadata': json.dumps(metadata),
            'created_by_email': self.admin_email,
            'created_at': datetime.utcnow()
        })
        
        batch_record_id = result.scalar()
        await self.db.commit()
        
        return batch_record_id
    
    async def _update_batch_record_with_job(self, batch_name: str, job_data: Dict[str, Any]):
        """Atualiza registro com informações do job Azure"""
        query = """
        UPDATE blog_batch_jobs SET 
            azure_batch_id = :azure_batch_id,
            status = :status,
            input_file_id = :input_file_id,
            azure_created_at = :azure_created_at,
            updated_at = :updated_at
        WHERE batch_name = :batch_name
        """
        
        await self.db.execute(text(query), {
            'batch_name': batch_name,
            'azure_batch_id': job_data['azure_batch_id'],
            'status': job_data['status'],
            'input_file_id': job_data['input_file_id'],
            'azure_created_at': datetime.fromtimestamp(job_data['created_at']),
            'updated_at': datetime.utcnow()
        })
        
        await self.db.commit()
    
    async def _create_blog_post_from_batch_result(
        self,
        parsed_content: Dict[str, Any],
        gen_metadata: Dict[str, Any],
        auto_publish: bool = False
    ) -> int:
        """Cria blog post a partir do resultado do batch"""
        # Gerar slug
        import re
        slug = re.sub(r'[^\w\s-]', '', parsed_content['title'].lower())
        slug = re.sub(r'[\s_-]+', '-', slug).strip('-')
        
        # Inserir blog post
        insert_query = """
        INSERT INTO blog_posts (
            title, slug, excerpt, content, category_id, author_name,
            status, seo_title, seo_description, reading_time, featured,
            generated_by_ai, generation_model, generation_params, ai_notes,
            published_at
        ) VALUES (
            :title, :slug, :excerpt, :content, :category_id, :author_name,
            :status, :seo_title, :seo_description, :reading_time, :featured,
            :generated_by_ai, :generation_model, :generation_params, :ai_notes,
            :published_at
        ) RETURNING id
        """
        
        published_at = datetime.utcnow() if auto_publish else None
        
        result = await self.db.execute(text(insert_query), {
            'title': parsed_content['title'],
            'slug': slug,
            'excerpt': parsed_content.get('excerpt'),
            'content': parsed_content['content'],
            'category_id': gen_metadata.get('category_id'),
            'author_name': 'AI Assistant (Batch)',
            'status': 'published' if auto_publish else 'draft',
            'seo_title': parsed_content.get('seo_title') or parsed_content['title'],
            'seo_description': parsed_content.get('seo_description'),
            'reading_time': parsed_content.get('reading_time', 5),
            'featured': False,
            'generated_by_ai': True,
            'generation_model': 'azure-batch-gpt-4.1',
            'generation_params': json.dumps(gen_metadata.get('original_request', {})),
            'ai_notes': f"Generated via batch processing: {gen_metadata.get('custom_id')}",
            'published_at': published_at
        })
        
        blog_post_id = result.scalar()
        
        # Adicionar produtos se existirem
        if gen_metadata.get('products'):
            for i, product in enumerate(gen_metadata['products']):
                await self.db.execute(text("""
                    INSERT INTO blog_post_products (
                        blog_post_id, product_id, position, context, ai_context
                    ) VALUES (
                        :blog_post_id, :product_id, :position, 'featured', 'Added via batch generation'
                    )
                """), {
                    'blog_post_id': blog_post_id,
                    'product_id': product['id'],
                    'position': i
                })
        
        # Adicionar referência ao batch
        await self.db.execute(text("""
            UPDATE blog_posts SET 
                batch_id = :batch_id, 
                batch_custom_id = :custom_id
            WHERE id = :blog_post_id
        """), {
            'blog_post_id': blog_post_id,
            'batch_id': gen_metadata.get('batch_id'),
            'custom_id': gen_metadata.get('custom_id')
        })
        
        await self.db.commit()
        return blog_post_id
    
    async def _record_batch_processing_history(
        self,
        batch_id: str,
        successful_count: int,
        failed_count: int,
        successful_posts: List[Dict[str, Any]],
        failed_posts: List[Dict[str, Any]]
    ):
        """Registra histórico do processamento do batch"""
        query = """
        INSERT INTO blog_batch_processing_history (
            batch_id, successful_count, failed_count, 
            successful_posts, failed_posts, processed_at
        ) VALUES (
            :batch_id, :successful_count, :failed_count,
            :successful_posts, :failed_posts, :processed_at
        )
        """
        
        await self.db.execute(text(query), {
            'batch_id': batch_id,
            'successful_count': successful_count,
            'failed_count': failed_count,
            'successful_posts': json.dumps(successful_posts),
            'failed_posts': json.dumps(failed_posts),
            'processed_at': datetime.utcnow()
        })
        
        await self.db.commit()