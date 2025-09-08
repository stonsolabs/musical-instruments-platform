"""
Azure App Service Authentication middleware
"""

from fastapi import Request, HTTPException
from typing import Optional
import os
import logging
import base64
import json

logger = logging.getLogger(__name__)

class AzureAuthMiddleware:
    """
    Middleware para validar autenticação do Azure App Service
    """
    
    def __init__(self):
        self.admin_email = os.getenv('ADMIN_EMAIL', 'admin@getyourmusicgear.com')
        self.is_local_dev = os.getenv('ENVIRONMENT') == 'development'
        self.allowed_admins = os.getenv('ADMIN_EMAILS', self.admin_email).split(',')
        self.allowed_admins = [email.strip().lower() for email in self.allowed_admins]
    
    async def get_user_info(self, request: Request) -> Optional[dict]:
        """
        Extrai informações do usuário dos headers do Azure App Service
        """
        if self.is_local_dev:
            # Em desenvolvimento, simula usuário admin
            return {
                'email': self.admin_email,
                'name': 'Local Admin User',
                'provider': 'local',
                'is_admin': True
            }
        
        # Headers injetados pelo Azure App Service Authentication
        principal_header = request.headers.get('X-MS-CLIENT-PRINCIPAL')
        principal_name = request.headers.get('X-MS-CLIENT-PRINCIPAL-NAME')
        principal_id = request.headers.get('X-MS-CLIENT-PRINCIPAL-ID')
        
        if not principal_header and not principal_name:
            return None
        
        user_info = {
            'email': principal_name,
            'id': principal_id,
            'provider': 'azure',
            'is_admin': False
        }
        
        # Tenta decodificar o principal completo se disponível
        if principal_header:
            try:
                # O header vem em base64
                decoded_principal = base64.b64decode(principal_header).decode('utf-8')
                principal_data = json.loads(decoded_principal)
                
                user_info.update({
                    'name': principal_data.get('name', principal_name),
                    'email': principal_data.get('email', principal_name),
                    'provider': principal_data.get('typ', 'azure'),
                    'claims': principal_data.get('claims', [])
                })
            except Exception as e:
                logger.warning(f"Could not decode principal header: {e}")
        
        # Verifica se é admin
        user_email = user_info.get('email', '').lower()
        user_info['is_admin'] = user_email in self.allowed_admins
        
        return user_info
    
    async def require_admin(self, request: Request) -> dict:
        """
        Requer que o usuário seja admin autenticado
        """
        user_info = await self.get_user_info(request)
        
        if not user_info:
            raise HTTPException(
                status_code=401, 
                detail={
                    "error": "authentication_required",
                    "message": "Please login to access this area",
                    "login_url": "/.auth/login/aad" if not self.is_local_dev else "/admin/login"
                }
            )
        
        if not user_info.get('is_admin', False):
            logger.warning(f"Non-admin user {user_info.get('email')} attempted admin access from IP: {request.client.host}")
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "admin_required", 
                    "message": f"Admin access required. Current user: {user_info.get('email')}",
                    "contact": "Contact the site administrator for access"
                }
            )
        
        logger.info(f"Admin access granted to {user_info['email']} from IP: {request.client.host}")
        return user_info
    
    async def get_optional_user(self, request: Request) -> Optional[dict]:
        """
        Retorna informações do usuário se autenticado, None caso contrário
        """
        try:
            return await self.get_user_info(request)
        except Exception as e:
            logger.debug(f"Could not get user info: {e}")
            return None

# Instância global do middleware
azure_auth = AzureAuthMiddleware()

# Dependency functions para uso nos endpoints
async def require_azure_admin(request: Request) -> dict:
    """Dependency que requer admin autenticado via Azure AD"""
    return await azure_auth.require_admin(request)

async def get_azure_user(request: Request) -> Optional[dict]:
    """Dependency que retorna usuário se autenticado"""
    return await azure_auth.get_optional_user(request)