from db.mongo.collections import Conversation, ScrapedUrls


class ConversationRepo:
    @classmethod
    async def create(cls, query: str, response: str) -> Conversation:
        conversation = Conversation(query=query, response=response)
        await conversation.insert()
        return conversation

    @classmethod
    async def get_by_id(cls, id: str) -> Conversation:
        return await Conversation.get(id)

    @classmethod
    async def get_all(cls) -> list[Conversation]:
        return await Conversation.find_all().to_list()


class ScrapedUrlsRepo:
    @classmethod
    async def create(cls, url: str) -> ScrapedUrls:
        scraped_url = ScrapedUrls(url=url)
        await scraped_url.insert()
        return scraped_url

    @classmethod
    async def get_by_url(cls, url: str) -> ScrapedUrls:
        return await ScrapedUrls.find_one(ScrapedUrls.url == url)
