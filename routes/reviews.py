from contextlib import contextmanager
from fastapi import APIRouter, Depends, HTTPException

from schemas.review import ReviewCreation, ReviewType
from services import UserService
from services.reviews import ReviewsService
from services.user import User


router = APIRouter(prefix='/reviews', tags=['Reviews Data'])


@contextmanager
def handle_review_exception():
    try:
        yield
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.args[0])


@router.get('/users/{username}')
async def get_users_reviews(username: str):
    with handle_review_exception():
        return await ReviewsService.get_user_reviews(username)


@router.get('/{entity_type}/{entity_id}')
async def get_entity_reviews(entity_type: ReviewType, entity_id: str):
    with handle_review_exception():
        return await ReviewsService.get_entities_reviews(entity_type, entity_id)


@router.post('/')
async def create_review(review: ReviewCreation, user: User = Depends(UserService.verify_token)):
    with handle_review_exception():
        return await ReviewsService.create_review(review, user.username)

