from schemas.survey import SurveyForm
from services.database import _MongoClient


class _RecommendationService(_MongoClient):
    def __init__(self, url: str | None = None) -> None:
        super().__init__(url)
        self.coll = self.db['survey']

    async def save_survey(self, survey: SurveyForm, username: str):
        await self.coll.update_one(
            {'username': username},
            {'$set': {**survey.dict(), 'username': username}},
            upsert=True,
        )

    async def get_survey(self, username: str):
        return await self.coll.find_one({'username': username}, {'_id': 0, 'username': 0})


RecommendationService = _RecommendationService()
