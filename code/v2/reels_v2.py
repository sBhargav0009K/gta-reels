"""Reel specs for the v2 full-bleed engine (fb.py).
Each line = one voiced sentence = one scene (cut on every line).
  say: spoken text   key: word highlighted yellow in captions
  img: official screenshot name   fx/fy: crop position (0..1)   move: in|out|l|r
  big: show as huge on-screen text instead of captions (hook + CTA)   tag: fact chip on the scene
status chip rules: "CONFIRMED BY ROCKSTAR" only with a Rockstar source; "REPORTED IN PREVIEWS" for
press preview reports; "UNTESTED · TEST IT" when we have no source and the reel is an experiment.
Fact check 25 Nov 2026: see REEL_LOG.md."""

REELS = {
    "4A": dict(
        slug="steal_their_shades", status="REPORTED IN PREVIEWS", bpm=104,
        lines=[
            dict(say="If their sunglasses fall off, they're yours.", big="Their shades fall off? They're yours.", img="Vice_City_24", fx=0.42),
            dict(say="That's what GTA 6 previews showed.", key="previews", img="Vice_City_03", fx=0.5, tag="REPORTED IN PREVIEWS"),
            dict(say="A scuffle knocks the glasses off.", key="scuffle", img="Vice_City_09", fx=0.6),
            dict(say="You pick them up,", key="pick", img="Vice_City_22", fx=0.3, move="r"),
            dict(say="and they go straight on your face.", key="face", img="Vice_City_24", fx=0.5, move="in"),
            dict(say="Hats? Bags? Nobody's tested it all yet.", key="tested", img="Vice_City_08", fx=0.5),
            dict(say="Send this to the friend who loots everything.", big="Send this to\nthe friend who\nloots everything", img="Vice_City_01", fx=0.5, big_cols=[(255, 255, 255), (255, 214, 60)]),
        ]),
    "5A": dict(
        slug="scuba_diving", status="CONFIRMED BY ROCKSTAR", bpm=92, mood="chill",
        lines=[
            dict(say="GTA 6's ocean is not empty.", big="GTA 6's ocean\nis NOT empty", img="Leonida_Keys_04", fx=0.5),
            dict(say="Scuba diving is a real activity.", key="Scuba", img="Leonida_Keys_01", fx=0.45, tag="CONFIRMED BY ROCKSTAR"),
            dict(say="Head to the coast and gear up,", key="gear", img="Leonida_Keys_05", fx=0.55),
            dict(say="then drop below the surface.", key="below", img="Leonida_Keys_07", fx=0.35),
            dict(say="The trailer showed manta rays and dolphins.", key="manta", img="Leonida_Keys_04", fx=0.2, move="r"),
            dict(say="Save this for your next chill session.", big="Save this for\nyour next\nchill session", img="Leonida_Keys_06", fx=0.25),
        ]),
    "5C": dict(
        slug="date_night", status="REPORTED IN PREVIEWS", bpm=96, mood="chill",
        lines=[
            dict(say="A date in GTA 6 can change your story.", big="A date can\nchange your\nstory", img="Jason_and_Lucia_16", fx=0.45),
            dict(say="Invite Jason or Lucia to tag along.", key="tag", img="Vice_City_02", fx=0.62),
            dict(say="Go shopping, hit the gym, or just explore.", key="explore", img="Vice_City_26", fx=0.5),
            dict(say="You can even hold hands.", key="hands", img="Vice_City_11", fx=0.35),
            dict(say="Previews say time together changes how the story plays out.", key="story", img="Vice_City_27", fx=0.5, tag="REPORTED IN PREVIEWS"),
            dict(say="Tag who you'd take to Vice City.", big="Tag who you'd\ntake to\nVice City", img="Vice_City_01", fx=0.5),
        ]),
    "6B": dict(
        slug="does_it_remember_rain", status="UNTESTED · TEST IT", bpm=100,
        lines=[
            dict(say="Does GTA 6 remember the rain?", big="Does GTA 6\nremember\nthe rain?", img="Vice_City_17", fx=0.5),
            dict(say="Next storm, don't hide inside.", key="storm", img="Ambrosia_02", fx=0.5),
            dict(say="The moment it stops, go straight out.", key="stops,", img="Vice_City_22", fx=0.55),
            dict(say="Check the roads. Do the puddles stay, or vanish?", key="puddles", img="Vice_City_09", fx=0.45, tag="UNTESTED · TEST IT"),
            dict(say="At night, look for city lights in the water.", key="lights", img="Vice_City_27", fx=0.5),
            dict(say="Test it, and tell me what you find.", big="Test it.\nTell me what\nyou find.", img="Vice_City_11", fx=0.4),
        ]),
    "7A": dict(
        slug="fishing", status="CONFIRMED BY ROCKSTAR", bpm=92, mood="chill",
        lines=[
            dict(say="No cops. No chaos. Just fishing.", big="No cops.\nNo chaos.\nJust fishing.", img="Jason_Duval_03", fx=0.3),
            dict(say="Rockstar's trailer showed fishing off a boat.", key="boat.", img="Vice_City_15", fx=0.5, tag="CONFIRMED BY ROCKSTAR"),
            dict(say="Try a pier, the swamp, or open water.", key="swamp,", img="Grassrivers_04", fx=0.45),
            dict(say="Cast. Wait for the bite. Reel it in.", key="bite.", img="Mount_Kalaga_National_Park_06", fx=0.45),
            dict(say="Then see what bites in each spot.", key="each", img="Leonida_Keys_01", fx=0.5),
            dict(say="Send this to the friend who needs a break.", big="Send this to\nthe friend who\nneeds a break", img="Port_Gellhorn_06", fx=0.5),
        ]),
    "7C": dict(
        slug="base_jump", status="CONFIRMED BY ROCKSTAR", bpm=108,
        lines=[
            dict(say="Step off a Vice City skyscraper.", big="Step off a\nVice City\nskyscraper", img="Vice_City_10", fx=0.3),
            dict(say="Base jumping is back in GTA 6.", key="back", img="Vice_City_17", fx=0.5, tag="CONFIRMED BY ROCKSTAR"),
            dict(say="Climb a tower at golden hour.", key="golden", img="Vice_City_11", fx=0.25),
            dict(say="Step off. Free fall. Pull the chute.", key="chute.", img="Mount_Kalaga_National_Park_02", fx=0.45),
            dict(say="Steer for the beach and land it.", key="beach", img="Vice_City_26", fx=0.5),
            dict(say="Send this to the friend who'd jump first.", big="Send this to\nthe friend who'd\njump first", img="Vice_City_27", fx=0.5),
        ]),
}
