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
