"""Headless check of audio.js in the real player UI (fake LLM, reply delayed 3 s)."""
import asyncio, json
from playwright.async_api import async_playwright

URL = "http://127.0.0.1:7860/"
INIT = """
window.__events = [];
const S = AudioBufferSourceNode.prototype;
const start = S.start, stop = S.stop;
S.start = function (...a) { window.__events.push({ev: 'start', dur: +this.buffer.duration.toFixed(2), loop: this.loop, t: Math.round(performance.now())}); return start.apply(this, a); };
S.stop = function (...a) { window.__events.push({ev: 'stop', dur: +this.buffer.duration.toFixed(2), t: Math.round(performance.now())}); return stop.apply(this, a); };
"""


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=True,
                                    args=["--autoplay-policy=no-user-gesture-required", "--no-sandbox"])
        page = await b.new_page()
        errors = []
        page.on("console", lambda m: m.type == "error" and errors.append(m.text))
        page.on("pageerror", lambda e: errors.append(str(e)))
        await page.add_init_script(INIT)

        async def slow(route):
            await asyncio.sleep(3)
            await route.continue_()
        await page.route("**/gradio_api/call/talk/**", slow)

        events = lambda: page.evaluate("window.__events.splice(0)")
        report = {}
        await page.goto(URL)
        await page.wait_for_function("document.body.dataset.room", timeout=30000)
        await page.mouse.click(5, 5)
        await page.wait_for_timeout(2500)
        report["first_room"] = await page.evaluate("document.body.dataset.room")
        report["toggle_button"] = await page.locator("#sound-toggle").inner_text()
        report["start_sounds"] = await events()

        # Walk through exits until someone is present.
        visited = [report["first_room"]]
        for _ in range(8):
            if await page.locator("#people [data-npc]").count():
                break
            exits = page.locator('#hotspots button[data-action="move"]:not(.locked)')
            if not await exits.count():
                break
            await exits.first.click()
            await page.wait_for_function(f"document.body.dataset.room !== {json.dumps(visited[-1])}", timeout=10000)
            await page.wait_for_timeout(1500)
            visited.append(await page.evaluate("document.body.dataset.room"))
        report["rooms_visited"] = visited
        report["move_sounds"] = await events()

        person = page.locator("#people [data-npc]").first
        report["npc"] = await person.get_attribute("data-npc")
        await person.click()
        await page.wait_for_selector("#dialogue[open]")
        await page.wait_for_timeout(500)
        await events()
        await page.fill("#question", "Where were you last night?")
        await page.click("#send")
        await page.wait_for_selector("#thinking:not([hidden])", timeout=5000)
        t0 = await page.evaluate("performance.now()")
        await page.wait_for_selector("#thinking[hidden]", state="attached", timeout=30000)
        t1 = await page.evaluate("performance.now()")
        await page.wait_for_timeout(600)
        report["thinking_visible_ms"] = round(t1 - t0)
        report["dialogue_sounds"] = await events()
        report["reply"] = (await page.locator("#lines li").last.inner_text())[:120]

        await page.click("#leave")
        await page.wait_for_timeout(300)
        await events()
        await page.evaluate("document.getElementById('case-file').showModal()")
        await page.wait_for_timeout(2000)
        report["accusation_sounds"] = await events()
        await page.evaluate("document.getElementById('case-file').close()")
        await page.wait_for_timeout(2000)
        report["after_accusation"] = await events()
        await page.evaluate("document.getElementById('journal').showModal()")
        await page.wait_for_timeout(500)
        report["journal_sounds"] = await events()
        await page.evaluate("document.getElementById('journal').close(); document.getElementById('ending').hidden = false")
        await page.wait_for_timeout(2000)
        report["ending_sounds"] = await events()
        report["errors"] = errors
        print(json.dumps(report, indent=1))
        await b.close()

asyncio.run(main())
