from fastapi import APIRouter, Depends, HTTPException

from schemas.survey import SurveyForm
from services import UserService
from services.city import CityService
from services.recommendation import RecommendationService
from services.user import User


router = APIRouter(prefix='/rec', tags=['Personal Recommendations Data'])


@router.post('/survey')
async def save_survey_result(form: SurveyForm, user: User = Depends(UserService.verify_token)):
    try:
        city = await CityService.find_city_by_id(form.current_city)
        await UserService.update_city(user.username, city)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=e.args)
    await RecommendationService.save_survey(form, user.username)


@router.get('/survey', response_model=SurveyForm | None)
async def get_survey_result(user: User = Depends(UserService.verify_token)):
    return await RecommendationService.get_survey(user.username)


@router.get('/cities')
async def get_rec_city():
    return await CityService.get_random_tour()
