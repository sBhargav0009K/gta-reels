"""edge-tts through the session proxy, with word timings.
say_words(voice, rate, text, out_mp3) -> list of (word, start_s, end_s)"""
import asyncio, os, ssl, sys, json
import edge_tts
from edge_tts import communicate as C

CA = os.path.expanduser("~/.ccr/ca-bundle.crt")
if os.path.exists(CA):
    C._SSL_CTX = ssl.create_default_context(cafile=CA)


async def say_words(voice, rate, text, out):
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    try:
        com = edge_tts.Communicate(text, voice, rate=rate, proxy=proxy, boundary="WordBoundary")
    except TypeError:
        com = edge_tts.Communicate(text, voice, rate=rate, proxy=proxy)
    words = []
    with open(out, "wb") as f:
        async for ch in com.stream():
            if ch["type"] == "audio":
                f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                s = ch["offset"] / 1e7
                words.append((ch["text"], s, s + ch["duration"] / 1e7))
    return words


if __name__ == "__main__":
    print(json.dumps(asyncio.run(say_words(*sys.argv[1:5]))))
