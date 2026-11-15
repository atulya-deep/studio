"""Short-format lessons (~30s, fast pace, strong hook). Importing registers them."""
import animate
from scenes import SCENES, end_card
import scenes4 as S
import scenes5 as N

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
# Hinglish roast-style shorts: on-screen text in Roman Hinglish, narration (say) in Devanagari, Hindi voice.
HI = (0.15, 0.35, 1.08, "piper:rohan", "hi")
L["18_raat_2_baje"] = ("Roz ki psychology", [
   dict(title="Abe saale, raat ke 2 baje. Neend aa rahi hai. Phir bhi *scroll* kar raha hai. Kyun?", big=True, footer="30 second ka gyaan",
        say="अबे साले, रात के दो बजे हैं। नींद आ रही है। फिर भी स्क्रॉल कर रहा है। क्यों?"),
   dict(body="Iska naam hai *revenge bedtime procrastination*. Matlab: din tera nahi tha, toh raat se *badla* le raha hai.",
        say="इसका नाम है, रिवेंज बेडटाइम प्रोक्रैस्टिनेशन। मतलब, दिन तेरा नहीं था, तो रात से बदला ले रहा है।"),
   dict(title="Asli wajah", body="Pura din office, boss, kaam. Apna time mila hi nahi. Toh dimaag bolta hai: *abhi nahi soyenge*.",
        say="असली वजह। पूरा दिन ऑफ़िस, बॉस, काम। अपना टाइम मिला ही नहीं। तो दिमाग बोलता है, अभी नहीं सोएंगे।"),
   dict(title="Fix simple hai", body="Din mein *20 minute* sirf apne liye nikaal. Warna gadhe, badla tu apni *neend* se hi le raha hai.",
        say="फ़िक्स सिंपल है। दिन में बीस मिनट सिर्फ़ अपने लिए निकाल। वरना गधे, बदला तू अपनी नींद से ही ले रहा है।"),
   dict(title="Yeh tu hai na?", body="Us kamine dost ko bhej jo *3 baje* tak online rehta hai.", footer="Follow kar le. Har hafte naya gyaan.",
        say="यह तू है ना? उस कमीने दोस्त को भेज, जो तीन बजे तक ऑनलाइन रहता है। और फ़ॉलो कर ले।"),
   ], [N.n_hook, N.n_name, N.n_why, N.n_fix], HI)
for k, (tag, cards, fns, pace) in L.items():
    animate.REELS[k] = (tag, cards); SCENES[k] = fns + [end_card]; PACE[k] = pace
