from aiohttp import web
from functools import lru_cache

import server

from ..random import DPRandomGenerator

@lru_cache(maxsize=1)
def get_generator(template_text) :
    return DPRandomGenerator()

@server.PromptServer.instance.routes.post("/dynamicprompts/random")
async def generate_random(request : web.Request):
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

        return web.json_response({"prompt": prompt[0].strip()})
    except Exception as ex:
        return web.Response(status=404, reason=str(ex))

