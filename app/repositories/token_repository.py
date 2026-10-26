from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.oauth_token import OAuthToken


class TokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_token(self, user_id: str, provider: str) -> Optional[OAuthToken]:
        result = await self.session.execute(
            select(OAuthToken).where(
                OAuthToken.user_id == user_id,
                OAuthToken.provider == provider
            )
        )
        return result.scalars().first()

    async def save_or_update_token(
        self, user_id: str, provider: str, access_token: str, refresh_token: Optional[str] = None, **kwargs
    ) -> OAuthToken:
        token = await self.get_token(user_id, provider)
        if not token:
            token = OAuthToken(
                user_id=user_id,
                provider=provider,
                access_token=access_token,
                refresh_token=refresh_token,
                **kwargs
            )
            self.session.add(token)
        else:
            token.access_token = access_token
            if refresh_token:
                token.refresh_token = refresh_token
            for key, val in kwargs.items():
                if hasattr(token, key):
                    setattr(token, key, val)
        await self.session.commit()
        await self.session.refresh(token)
        return token
