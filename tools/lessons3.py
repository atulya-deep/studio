"""Batch 3: pratfall effect, Ivy Lee method, Operation Mincemeat. Importing registers them in animate.REELS and scenes.SCENES."""
import animate
from scenes import SCENES, end_card
import scenes3 as S

END = animate.END
H = dict(big=True, footer="A 60-second lesson")
PSY, PRO, HIS = "Psychology · Mindset", "Productivity · Habits", "History · Strategy"

L = {
 "14_pratfall": (PSY, [
   dict(title="Why *spilling your coffee* can make people like you more", **H),
   dict(body="In 1966, psychologist Elliot Aronson played students a tape of a quiz contestant who got *92% of the questions right*. On some tapes, there was then a crash.",
        say="In nineteen sixty-six, psychologist Elliot Aronson played students a tape of a quiz contestant who got ninety-two percent of the questions right. On some tapes, there was then a crash."),
   dict(title="The Pratfall Effect", body="He'd *spilled coffee* all over his new suit. Listeners liked the star *more* after the blunder. The same spill made an average contestant *less* likeable."),
   dict(title="Why it works", body="Someone who seems flawless feels *distant*, almost superhuman. A small slip makes a capable person *human*, and easier to like."),
   dict(title="Use it", body="Show you're good at the job first. Then stop hiding every small slip. *Laugh at the spill.* Competence plus a flaw beats flawless."),
   END], [S.pf_hook, S.pf_tape, S.pf_result, S.pf_why, S.pf_use]),
 "15_ivy_lee": (PRO, [
   dict(title="The to-do list that was worth *$25,000*", say="The to-do list that was worth twenty-five thousand dollars.", **H),
   dict(body="As the story goes: in 1918, steel boss Charles Schwab asked consultant Ivy Lee to make his team more productive. Lee asked for *15 minutes* with each executive.",
        say="As the story goes: in nineteen eighteen, steel boss Charles Schwab asked consultant Ivy Lee to make his team more productive. Lee asked for fifteen minutes with each executive."),
   dict(title="The Ivy Lee Method", body="Each evening, write the *six most important* tasks for tomorrow. Rank them. Work through them *one at a time*, in order. Anything unfinished moves to tomorrow's list."),
   dict(title="The bill", body="Lee charged nothing up front: pay what it's worth. Three months later, Schwab sent him a cheque for *$25,000*. That's hundreds of thousands in today's money.",
        say="The bill. Lee charged nothing up front: pay what it's worth. Three months later, Schwab sent him a cheque for twenty-five thousand dollars. That's hundreds of thousands in today's money."),
   dict(title="Try it tonight", body="Before you log off, write *six tasks*. Not ten. Six. Tomorrow, start with number one and don't touch number two *until it's done*."),
   END], [S.iv_hook, S.iv_office, S.iv_list, S.iv_cheque, S.iv_tonight]),
 "16_mincemeat": (HIS, [
   dict(title="The fake officer who *fooled Hitler*", **H),
   dict(body="1943. The Allies want to invade *Sicily*, and anyone with a map can see it coming. So British intelligence decides to sell the Germans a lie.",
        say="Nineteen forty-three. The Allies want to invade Sicily, and anyone with a map can see it coming. So British intelligence decides to sell the Germans a lie."),
   dict(title="Operation Mincemeat", body="On 30 April, a British submarine released a body off Spain, dressed as Royal Marines officer *Major William Martin*. His papers said the Allies would land in *Greece and Sardinia*.",
        say="Operation Mincemeat. On the thirtieth of April, a British submarine released a body off Spain, dressed as Royal Marines officer Major William Martin. His papers said the Allies would land in Greece and Sardinia."),
   dict(title="The details sold it", body="His pockets held a photo of his fiancée, *theatre ticket stubs* and a receipt for an engagement ring. Hitler sent troops to Greece. In July, the Allies landed in *Sicily*."),
   dict(title="The lesson", body="Big claims make people suspicious. *Small, specific details* make them believe. Next time you need to persuade, skip \"trust me\" and *show the receipts*."),
   END], [S.mm_hook, S.mm_map, S.mm_sub, S.mm_pockets, S.mm_lesson]),
}

for k, (tag, cards, fns) in L.items():
    animate.REELS[k] = (tag, cards)
    SCENES[k] = fns + [end_card]
