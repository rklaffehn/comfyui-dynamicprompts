from aiohttp import web
from functools import lru_cache

import server

from dynamicprompts.generators import RandomPromptGenerator
from dynamicprompts.generators.magicprompt import MagicPromptGenerator

from ..random import DPRandomGenerator
from ..feeling_lucky import DPFeelingLucky


@lru_cache(maxsize=1)
def get_generator(template_text):
    return DPRandomGenerator()


@server.PromptServer.instance.routes.post("/dynamicprompts/random")
async def generate_random(request: web.Request):
    '''Generate a random prompt from a template when a client asks this end-point.
    @param request {template: str}
    @returns response {prompt: str}
    '''
    query = await request.json()

    if not "template" in query:
        return web.Response(status=404, reason="missing template in request")

    try:
        template_text = query["template"].strip()
        generator = get_generator(template_text)
        prompt = generator.get_prompt(template_text)
        print(generator, template_text)

        return web.json_response({"prompt": prompt[0].strip()})
    except Exception as ex:
        return web.Response(status=404, reason=str(ex))


@lru_cache(maxsize=1)
def get_feeling_lucky_generator(template_text):
    return DPFeelingLucky()


@server.PromptServer.instance.routes.post("/dynamicprompts/feeling_lucky")
async def generate_feeling_lucky(request: web.Request):
    query = await request.json()

    if not "template" in query:
        return web.Response(status=404, reason="missing template in request")

    try:
        template_text = query["template"].strip()
        generator = get_feeling_lucky_generator(template_text)
        prompt = generator.get_prompt(template_text, autorefresh=True)

        return web.json_response({"prompt": prompt[0].strip()})
    except Exception as ex:
        return web.Response(status=404, reason=str(ex))


class MagicPromptServer:
    def __init__(self) -> None:
        self.cache = []
        self.generator = MagicPromptGenerator(
            prompt_generator=RandomPromptGenerator())

    def get_prompt(self, text: str) -> str:
        if not self.cache:
            self.cache = self.generator.generate(text)

        return self.cache.pop()


@lru_cache(maxsize=1)
def get_magic_prompt_generator(template_text):
    return MagicPromptServer()


@server.PromptServer.instance.routes.post("/dynamicprompts/magic_prompt")
async def generate_magic_prompt(request: web.Request):
    query = await request.json()

    if not "template" in query:
        return web.Response(status=404, reason="missing template in request")

    try:
        template_text = query["template"].strip()
        generator = get_magic_prompt_generator(template_text)
        prompt = generator.get_prompt(template_text)

        return web.json_response({"prompt": prompt[0].strip()})
    except Exception as ex:
        return web.Response(status=404, reason=str(ex))
