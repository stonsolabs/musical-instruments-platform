"""
Azure App Service Authentication middleware
"""

from fastapi import Request, HTTPException
from typing import Optional
import os
import logging

logger = logging.getLogger(__name__)

class AzureAuthMiddleware:
    """
    Middleware para validar autenticação do Azure App Service
    """
    
    def __init__(self):
        self.admin_email = os.getenv('ADMIN_EMAIL', 'admin@getyourmusicgear.com')
        self.is_local_dev = os.getenv('ENVIRONMENT') == 'development'
    
    async def get_user_info(self, request: Request) -> Optional[dict]:
        """
        Extrai informações do usuário dos headers do Azure App Service
        """
        if self.is_local_dev:
            # Em desenvolvimento, simula usuário admin
            return {
                'email': self.admin_email,
                'name': 'Admin User',
                'is_admin': True
            }
        
        # Headers injetados pelo Azure App Service Authentication
        user_email = request.headers.get('X-MS-CLIENT-PRINCIPAL-NAME')
        user_id = request.headers.get('X-MS-CLIENT-PRINCIPAL-ID')
        user_claims = request.headers.get('X-MS-CLIENT-PRINCIPAL')
        
        if not user_email:
            return None
        
        # Verifica se é o admin
        is_admin = user_email.lower() == self.admin_email.lower()
        
        return {
            'email': user_email,
            'id': user_id,
            'claims': user_claims,
            'is_admin': is_admin
        }
    
    async def require_admin(self, request: Request) -> dict:
        """
        Requer que o usuário seja admin autenticado
        """
        user_info = await self.get_user_info(request)
        
        if not user_info:
            raise HTTPException(
                status_code=401, 
                detail="Authentication required. Please login through Azure AD."
            )
        
        if not user_info.get('is_admin', False):
            raise HTTPException(
                status_code=403,
                detail=f"Admin access required. Contact administrator if you believe this is an error."
            )
        
        logger.info(f"Admin access granted to {user_info['email']} from IP: {request.client.host}")
        return user_info
    
    async def get_optional_user(self, request: Request) -> Optional[dict]:
        """
        Retorna informações do usuário se autenticado, None caso contrário
        """
        try:
            return await self.get_user_info(request)
        except:
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