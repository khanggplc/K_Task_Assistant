from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.integrations.gmail.oauth import GmailOAuthManager
from app.repositories.token_repository import TokenRepository
from app.core.logging import logger

router = APIRouter()


@router.get("/google/login")
async def google_login():
    """Generates Google OAuth URL for user consent."""
    oauth = GmailOAuthManager()
    url, state = oauth.get_authorization_url()
    return {"authorization_url": url, "state": state}


@router.get("/google/callback")
async def google_callback(
    code: str = Query(...),
    state: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """Handles Google OAuth callback and stores tokens."""
    try:
        oauth = GmailOAuthManager()
        token_data = oauth.exchange_code_for_token(code)

        # In production, extract user_id from state or JWT session
        user_id = state or "default_user"
        token_repo = TokenRepository(db)
        await token_repo.save_or_update_token(
            user_id=user_id,
            provider="google",
            access_token=token_data["access_token"],
            refresh_token=token_data.get("refresh_token"),
            scopes=str(token_data.get("scopes", "")),
        )
        return {"status": "success", "message": "Google account connected successfully"}
    except Exception as e:
        logger.error("OAuth exchange failed: %s", e)
        raise HTTPException(status_code=400, detail=f"OAuth exchange failed: {str(e)}")
