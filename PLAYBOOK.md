# @mind_shap Instagram playbook

Deepstash-style micro-lessons: Psychology & mindset, Productivity & habits, History & strategy (from books and research).
3 posts/week: Mon, Wed, Fri ~18:40 IST. Owner approves each weekly batch before it posts.
Content must be ORIGINAL writing (Deepstash is a format reference only). Facts must be checked against sources.

## Files
- `queue.json` — posting queue. status: pending (awaiting approval) → approved → posted. `post_on` = YYYY-MM-DD (IST).
- `reels/` — final MP4s (public raw URLs = raw_base + file).
- `tools/` — generator: `animate.py` (REELS text/narration specs), `scenes.py` (animated scenes per slide), `chars.py` (characters + owl mascot), `reel3.py` (renderer).

## Render setup in a fresh session
```
mkdir -p /home/claude/reels /home/claude/tts && cp tools/*.py /home/claude/reels/
pip install --break-system-packages -q kokoro-onnx soundfile pycairo
cd /home/claude/tts && curl -sSLO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx && curl -sSLO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
cd /home/claude/reels && python3 reel3.py <key>        # output: /home/claude/reels/v3/<key>.mp4
```
Narration wavs are generated automatically if missing (voice af_heart). Each reel = 5 lesson slides + END card (6 entries in animate.REELS and scenes.SCENES; last scene is `end_card`).
To add a lesson: add text cards to `animate.REELS[key]` (title/body, *accent*, optional `say` for pronunciation) and 5 scene functions + `end_card` to `scenes.SCENES[key]` (960x720 panel, draw with chars.py helpers). Render stills first: `python3 reel3.py <key> --still IDX T`.

## Posting (Windsor.ai for Social Media connector)
execute_action connector=instagram action=create_video_post account=<account_id>
params: video_url=raw_base+file, caption, share_to_feed=true, thumb_offset=2500
Then set status=posted, add media_id + permalink (get_data fields media_id, media_permalink, last_3dT), commit and push to branch `reels`.
Only post items with status=approved. Never post pending items.

## Batch 2 onwards
New lessons live in `tools/lessons2.py` (text + narration + scene list) with scenes in `tools/scenes2a.py` / `scenes2b.py` and shared props in `tools/kit2.py` (duck, tomato, emu, rat, plane, monitor, bubbles). Add a lesson by adding an entry to `lessons2.L`. Preview all scenes of a lesson with `python3 sheet.py <key>` (writes v3/sheet_<key>.png), then `python3 reel3.py <key>`. Tone: some lessons should have a funny twist.

## Batch 3 onwards
Lessons 14+ live in `tools/lessons3.py` with scenes in `tools/scenes3.py` (props: mug/coffee splash, podium, tape recorder, scoreboard, notepad, cheque, clock, steel-mill window, briefcase, submarine, Mediterranean map, photo/ticket/receipt). `reel3.py` and `sheet.py` import it. Keep key visuals out of the panel's bottom-right corner (owl mascot sits there).

## Short format (preferred from 2026-11-15)
Owner asked for ~30-second everyday-psychology videos with an attention-grabbing hook. See `tools/lessons4.py` + `scenes4.py` (17_phantom): 4 lesson cards + a short share-prompt end card, ~70 spoken words, loud first second (shake, flashing text), fast pace via `lessons4.PACE[key] = (lead, tail, speech speed)`. Add new short lessons to `lessons4.L`.

## Hinglish test (2026-11-15)
Owner wants to test Hindi for reach. Agreed style: Hinglish roast tone, mild slang only (abe, bhai, pagal), NO hard gaali. On-screen text in Roman Hinglish; narration `say` in Devanagari with a Hindi voice via `lessons4.HI` pace tuple (lead, tail, speed, voice, lang). Example: 18_raat_2_baje in `lessons4.py` + `scenes5.py`. Owner must listen before posting: audio can't be checked here.

Hindi voice update: Kokoro Hindi sounded unnatural to the owner. Use native Piper Hindi voices instead: `pip install piper-tts`, download `vits-piper-hi_IN-{rohan,pratham,priyamvada}-medium.tar.bz2` from github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/ into /home/claude/tts/hi/, and set the voice to `piper:rohan` (see `animate._piper`). Owner also asked for a small amount of mild abuse (abe saale, gadhe, kamine); still no hard gaali.

Narration flow fix: Piper inserts ~0.45s silences after every phrase, which the owner heard as 'breaking'. `animate._tighten` now caps internal pauses at 0.15s; keep speed near 1.08.

## CURRENT STYLE (from 2026-11-17, supersedes the card style above)
Owner asked to drop the card/slide layout. New videos use the full-screen motion renderer `tools/motion.py` (class Film): full-bleed animated scenes at 1080x1920, big word-by-word captions, push transitions, no header/progress bar/owl, ~18-22s, 6 beats of one sentence each. Example film: `tools/film_voice.py` (19_voice) -> `python3 film_voice.py --stills` to preview, `python3 film_voice.py` to render to /home/claude/reels/v4/. Rules: hook words and full visuals on screen at frame 0; change scene every 2-4s; keep action in y 200-1180 and captions near y 1340; end with a share prompt. Topics: everyday psychology/body/brain 'why do you...' questions. English narration (af_heart, speed 1.08). Weekly batches should be made in this style, as new film_*.py files.

Hinglish roast films in motion style: see `tools/film_dimaag.py` (voice `piper:rohan`, lang hi; captions in Roman Hinglish, `say` in Devanagari). Owner asked for strong abuse on this one (chutiye, saala, gadhe, bakchod). Never use maa-behen, caste, religion or gender slurs.

## Batch 2026-12-14 (films 22-24)
Three motion-style films, one per pillar: `tools/film_peak.py` (22_peak_end), `tools/film_bundle.py` (23_temptation_bundling), `tools/film_cannae.py` (24_cannae). `film_peak.sheet(f)` writes a 12-frame contact sheet (`--stills`). New props: ice bucket + `submerge` (hand in water), thermometer, stopwatch, headphones, locker, treadmill, couch, top-down battle map (`film_cannae.battle`, phases 0-3) with a colour legend.

## Batch 2026-12-14 (films 33-35)
Motion-style films, one per pillar: `tools/film_franklin.py` (33_franklin, Ben Franklin effect), `tools/film_fresh.py` (34_fresh_start, Dai/Milkman/Riis 2014), `tools/film_pyrrhic.py` (35_pyrrhic, Plutarch's Pyrrhus). Each runs `--stills` for a 12-frame sheet. New props: Franklin (grey hair, specs) + tricorn rival, rare book/note, coin, favour meter, calendar page (`film_fresh.calendar`), search bar, spike chart, gym/treadmill reuse, crowned king Pyrrhus + Epirote hoplite, cracking trophy, Roman gate, casualty scoreboard.
