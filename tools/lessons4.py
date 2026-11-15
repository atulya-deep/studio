"""Short-format lessons (~30s, fast pace, strong hook). Importing registers them."""
import animate
from scenes import SCENES, end_card
import scenes4 as S

PACE = {}   # key -> (lead, tail, speech speed)
L = {
 "17_phantom": ("Everyday psychology", [
   dict(title="Your phone *didn't buzz*. You felt it anyway.", big=True, footer="A 30-second lesson"),
   dict(body="It's called a *phantom vibration*. In one study, *9 in 10* students said they'd felt one.",
        say="It's called a phantom vibration. In one study, nine in ten students said they'd felt one."),
   dict(title="Why it happens", body="Your brain is on *high alert* for notifications. So a muscle twitch or a shifting sleeve gets read as a buzz."),
   dict(title="The fix", body="Move your phone to a *different pocket*. In a hospital survey, most people who tried it said it helped."),
   dict(title="Felt it?", body="Send this to someone *glued to their phone*.", footer="Follow for a new lesson every week",
        say="Send this to someone glued to their phone. And follow for more."),
   ], [S.ph_hook, S.ph_stat, S.ph_why, S.ph_fix], (0.18, 0.38, 1.1)),
}
for k, (tag, cards, fns, pace) in L.items():
    animate.REELS[k] = (tag, cards); SCENES[k] = fns + [end_card]; PACE[k] = pace
