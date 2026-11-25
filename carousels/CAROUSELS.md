# Daily carousels (Instagram, 4 slides, 1080x1350)

Look: game HUD (`gamehud.py`): minimap, health/armour bars, wanted stars, handle, in-game clock, pink/yellow slanted Anton titles, pink loading bar across slides (1/4 to 4/4). Backgrounds: official GTA VI screenshots from rockstargames.com/VI/downloads/screenshots (credit "Image: Rockstar Games" on every slide). No Rockstar logos, no character close-ups.

Every carousel tells a mini story, not a list:
1. HOOK / title card: "A Vice City story", a cliffhanger title, "✕ Swipe to play".
2. CH.1 conflict: the problem or the moment, with cutscene-style subtitles and a matching HUD state (e.g. 5 stars).
3. CH.2 turn: what changed or what you discover.
4. CH.3 payoff: the viewer goes and does it + CTA ("send them this", "follow for tomorrow's story").
The in-game clock moves forward slide by slide. Facts stay true; a small footnote cites the source when the story leans on a real fact.

Files: `gamehud.py` (shared helpers), `c1_story.py` (carousel 1, The Night You Almost Quit, update 01.002.002). Earlier drafts: `c1_patch.py`, `c1_cosy.py`, `c1_game.py`.
Plan: #2 The Secret Road to Vice City, #3 4 Things to Try This Weekend, #4 Week 1 Easter Eggs, one a day.
