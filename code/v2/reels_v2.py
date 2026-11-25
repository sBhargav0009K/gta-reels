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

# ---- Batch 2 (Days 3-5), fact-checked 25 Nov 2026; see REEL_LOG.md "Fact check batch 2" ----
REELS.update({
    "2A": dict(
        slug="paint_the_bedroom", status="FOUND BY PLAYERS", bpm=96, mood="chill",
        lines=[
            dict(say="Do this before you pick up Lucia in GTA 6.", big="Do this before\nyou pick up\nLucia", img="Leonida_Keys_01", fx=0.35),
            dict(say="Jason's house in Key Lento has repair projects.", key="projects.", img="Leonida_Keys_02", fx=0.45, tag="FOUND BY PLAYERS"),
            dict(say="One of them is the bedroom wall.", key="bedroom", img="Grassrivers_02", fx=0.5),
            dict(say="Hang the drywall, pick a colour, and roll the paint on yourself.", key="colour,", img="Leonida_Keys_03", fx=0.15, move="r"),
            dict(say="Guides say it gives your relationship a small boost.", key="boost.", img="Port_Gellhorn_06", fx=0.5),
            dict(say="Save this before it's too late.", big="Save this\nbefore it's\ntoo late", img="Vice_City_15", fx=0.5),
        ]),
    "1B": dict(
        slug="lucky_dog_rescue", status="FOUND BY PLAYERS", bpm=104,
        lines=[
            dict(say="Stranded at sea in GTA 6? Wait for this dog.", big="Stranded at sea?\nWait for\nthis dog", img="Leonida_Keys_01", fx=0.6),
            dict(say="Take a boat out into Gambit Bay, near Key Lento.", key="Gambit", img="Leonida_Keys_05", fx=0.5),
            dict(say="Jump in, swim away, and wait a few minutes.", key="wait", img="Leonida_Keys_01", fx=0.2, move="r"),
            dict(say="Players say a dog on a jet ski comes to rescue you.", key="dog", img="Leonida_Keys_05", fx=0.15, tag="FOUND BY PLAYERS"),
            dict(say="He takes you to an island and digs up cash.", key="cash", img="Leonida_Keys_06", fx=0.2),
            dict(say="Send this to the friend who'd wait all day.", big="Send this to\nthe friend who'd\nwait all day", img="Vice_City_15", fx=0.5),
        ]),
    "4C": dict(
        slug="joystation_console", status="CONFIRMED BY ROCKSTAR", bpm=108,
        lines=[
            dict(say="GTA 6 has video games inside the video game.", big="Video games\ninside\nGTA 6", img="Vice_City_13", fx=0.5),
            dict(say="Turn on the JoyStation at Jason's place.", key="JoyStation.", img="Grassrivers_02", fx=0.6),
            dict(say="Rockstar says an in-house team made these games.", key="team", img="Vice_City_13", fx=0.2, move="r", tag="CONFIRMED BY ROCKSTAR"),
            dict(say="Time Jackers is a twin-stick shooter.", key="Jackers", img="Vice_City_08", fx=0.5),
            dict(say="And Street Trash 3 is all about zombies.", key="zombies.", img="Port_Gellhorn_01", fx=0.5),
            dict(say="Send this to your gaming buddy.", big="Send this to\nyour gaming\nbuddy", img="Vice_City_27", fx=0.5),
        ]),
    "1A": dict(
        slug="cops_want_your_shirt", status="REPORTED IN PREVIEWS", bpm=108,
        lines=[
            dict(say="In GTA 6, the cops are looking for your shirt.", big="The cops are\nlooking for\nyour shirt", img="Vice_City_17", fx=0.5),
            dict(say="Wanted levels now come with Heat clues.", key="Heat", img="Vice_City_17", fx=0.15, move="r", tag="REPORTED IN PREVIEWS"),
            dict(say="Cameras, your face, your car, and your clothes.", key="clothes.", img="Vice_City_09", fx=0.5),
            dict(say="Change your outfit, and that clue drops off.", key="outfit,", img="Lucia_Caminos_08", fx=0.5),
            dict(say="Ditch the car too, and walk away calm.", key="calm.", img="Vice_City_22", fx=0.5),
            dict(say="Send this to your getaway driver.", big="Send this to\nyour getaway\ndriver", img="Vice_City_10", fx=0.4),
        ]),
    "6A": dict(
        slug="not_bigfoot_skunkape", status="FOUND BY PLAYERS", bpm=92, mood="chill",
        lines=[
            dict(say="That's not Bigfoot in GTA 6.", big="That's NOT\nBigfoot", img="Grassrivers_08", fx=0.5),
            dict(say="Locals call it the Skunkape.", key="Skunkape.", img="Grassrivers_04", fx=0.5, tag="FOUND BY PLAYERS"),
            dict(say="It's a questline you can only start as Jason, at night.", key="night.", img="Grassrivers_03", fx=0.5),
            dict(say="Look for the posters around Key Lento.", key="posters", img="Leonida_Keys_02", fx=0.3),
            dict(say="Days later, an expert called Kirk gets in touch.", key="Kirk", img="Grassrivers_07", fx=0.6),
            dict(say="Send this to the friend who believes.", big="Send this to\nthe friend\nwho believes", img="Grassrivers_08", fx=0.2),
        ]),
    "2C": dict(
        slug="literal_easter_egg", status="FOUND BY PLAYERS", bpm=100,
        lines=[
            dict(say="Rockstar hid a literal Easter egg in GTA 6.", big="A LITERAL\nEaster egg", img="Ambrosia_04", fx=0.5),
            dict(say="A player climbed a tower for about seven minutes.", key="seven", img="Ambrosia_04", fx=0.2, move="r", tag="FOUND BY PLAYERS"),
            dict(say="At the top, a nest of brightly coloured eggs.", key="eggs.", img="Port_Gellhorn_06", fx=0.5),
            dict(say="Throw one, and a cutscene shows it hitting a car windscreen.", key="windscreen.", img="Vice_City_09", fx=0.5),
            dict(say="The exact tower isn't confirmed yet.", key="tower", img="Mount_Kalaga_National_Park_04", fx=0.5),
            dict(say="Find it first? Tell me where.", big="Find it first?\nTell me where", img="Ambrosia_04", fx=0.8),
        ]),
    "1C": dict(
        slug="pet_the_bodega_cats", status="FOUND BY PLAYERS", bpm=96, mood="chill",
        lines=[
            dict(say="Yes, you can pet the cats in GTA 6.", big="Yes, you can\npet the cats", img="Vice_City_22", fx=0.6),
            dict(say="Rockstar's trailer showed a bodega cat on an ATM.", key="ATM.", img="Vice_City_22", fx=0.2, move="r", tag="CONFIRMED BY ROCKSTAR"),
            dict(say="Players found you can walk up and give them a pet.", key="pet.", img="Vice_City_03", fx=0.5),
            dict(say="Not all of them are friendly, though.", key="friendly,", img="Port_Gellhorn_01", fx=0.5),
            dict(say="Make it your mission to pet every cat in Leonida.", key="every", img="Vice_City_09", fx=0.4),
            dict(say="Send this to the friend with five cats.", big="Send this to\nthe friend with\nfive cats", img="Vice_City_27", fx=0.5),
        ]),
    "6C": dict(
        slug="casinos_you_cant_enter", status="CONFIRMED BY ROCKSTAR", bpm=104,
        lines=[
            dict(say="GTA 6 has casinos you can't walk into.", big="Casinos you\ncan't walk into", img="Vice_City_27", fx=0.5),
            dict(say="A reporter counted at least two big ones.", key="two", img="Vice_City_11", fx=0.3),
            dict(say="Go see them at night. They're lit up like crazy.", key="night.", img="Vice_City_08", fx=0.5),
            dict(say="So why are the doors shut?", key="shut?", img="Vice_City_10", fx=0.6),
            dict(say="Rockstar says gambling didn't fit Jason and Lucia's story.", key="story.", img="Jason_and_Lucia_16", fx=0.45, tag="CONFIRMED BY ROCKSTAR"),
            dict(say="What should be inside? Tell me.", big="What should be\ninside?\nTell me", img="Vice_City_11", fx=0.6),
        ]),
    "2B": dict(
        slug="cat_in_the_back_seat", status="FOUND BY PLAYERS", bpm=108,
        lines=[
            dict(say="In GTA 6, check the back seat before you steal a car.", big="Check the\nback seat\nfirst", img="Port_Gellhorn_01", fx=0.5),
            dict(say="Players found parked cars with a cat inside.", key="cat", img="Vice_City_09", fx=0.6, tag="FOUND BY PLAYERS"),
            dict(say="Take the car anyway,", key="anyway,", img="Vice_City_22", fx=0.5),
            dict(say="and the cat jumps you mid drive.", key="jumps", img="Ambrosia_05", fx=0.5),
            dict(say="Clips show it throwing paws at Jason.", key="paws", img="Vice_City_09", fx=0.15, move="r"),
            dict(say="Send this to the friend who'd lose to the cat.", big="Send this to\nthe friend who'd\nlose to the cat", img="Vice_City_27", fx=0.3),
        ]),
})
