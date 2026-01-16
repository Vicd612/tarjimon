import aiohttp

async def tarjimon(text, lang):
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "auto",
            "tl": lang,
            "dt": "t",
            "q": text
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    translated = "".join([s[0] for s in data[0] if s[0]])
                    return translated
        
        return text
    except:
        return text