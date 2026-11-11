"""Batch 2: ten lessons (text + narration). Importing this registers them in animate.REELS and scenes.SCENES."""
import animate
from scenes import SCENES, end_card
import scenes2a as A, scenes2b as B

END = animate.END
H = dict(big=True, footer="A 60-second lesson")
PSY, PRO, HIS = "Psychology · Mindset", "Productivity · Habits", "History · Strategy"

L = {
 "04_spotlight": (PSY, [
   dict(title="Nobody noticed your *embarrassing* moment", **H),
   dict(body="In 2000, Cornell psychologists sent students into a busy room wearing a *deeply uncool* Barry Manilow T-shirt. Then they asked: how many people noticed?",
        say="In the year two thousand, Cornell psychologists sent students into a busy room wearing a deeply uncool Barry Manilow T-shirt. Then they asked: how many people noticed?"),
   dict(title="The Spotlight Effect", body="The wearers guessed about *half* the room had seen the shirt. In reality, only about *a quarter* had."),
   dict(title="Why it happens", body="You are the centre of your world, so you assume you're the centre of theirs. But everyone else is busy *starring in their own movie*."),
   dict(title="Use it", body="Tripped on the stairs? Bad haircut? Relax. Most people never noticed, and the rest have *already forgotten*."),
   END], [A.s_hook, A.s_shirt, A.s_stats, A.s_movie, A.s_use]),
 "05_ikea": (PSY, [
   dict(title="Why you love that *wobbly shelf* you built yourself", **H),
   dict(body="It leans. There were *three screws left over*. And yet you would defend this shelf with your life."),
   dict(title="The IKEA Effect", body="In a study by Norton, Mochon and Ariely, people who assembled a plain storage box bid *63% more* for it than people shown the same box ready-made.",
        say="The IKEA effect. In a study by Norton, Mochon and Ariely, people who assembled a plain storage box bid sixty-three percent more for it than people shown the same box ready-made."),
   dict(title="Labour leads to love", body="Effort makes things feel valuable. Lovely for shelves. *Dangerous* for the bad idea you've already sunk six weeks into."),
   dict(title="Use it", body="Want people to back a plan? Let them *build part of it*. And for your own work, ask: would I pay for this if a stranger had made it?"),
   END], [A.k_hook, A.k_screws, A.k_study, A.k_love, A.k_use]),
 "06_doorway": (PSY, [
   dict(title="Why you walk into a room and *forget why*", **H),
   dict(body="You march into the kitchen with total purpose. Then you just stand there, staring at the fridge like a *confused robot*."),
   dict(title="The Doorway Effect", body="In 2011, psychologist Gabriel Radvansky found people forgot more after walking *through a doorway* than after walking the same distance inside one room.",
        say="The doorway effect. In twenty eleven, psychologist Gabriel Radvansky found people forgot more after walking through a doorway than after walking the same distance inside one room."),
   dict(title="Your brain files by scene", body="A doorway is an *event boundary*. The brain closes the old scene and files it away, along with whatever you were about to do."),
   dict(title="The fix", body="Say your mission *out loud* before you move. \"Scissors. I am getting scissors.\" You'll look odd. You'll also come back *with scissors*."),
   END], [A.d_hook, A.d_robot, A.d_study, A.d_file, A.d_fix]),
 "07_wald": (HIS, [
   dict(title="The *missing bullet holes* that saved lives", **H),
   dict(body="World War Two. Bombers limp home covered in bullet holes, mostly on the *wings and body*. The obvious plan: add armour there."),
   dict(title="Enter Abraham Wald", body="As the famous story goes, the statistician spotted the flaw. These were the planes that *made it home*. Their holes showed where a plane could be hit and survive."),
   dict(title="Survivorship bias", body="The planes hit in the *engines* never came back to be counted. The most important data was the data *nobody could see*."),
   dict(title="Use it", body="Before you copy a success story, ask: *who's missing?* For every famous dropout, count the dropouts nobody wrote a book about."),
   END], [A.w_hook, A.w_holes, A.w_wald, A.w_engines, A.w_use]),
 "08_emu": (HIS, [
   dict(title="The year Australia went to war with *birds*. And lost.", **H),
   dict(body="1932, Western Australia. Around *20,000 emus* are flattening wheat farms. The government's answer: send in the army.",
        say="Nineteen thirty-two, Western Australia. Around twenty thousand emus are flattening wheat farms. The government's answer: send in the army."),
   dict(title="The Great Emu War", body="Major Meredith arrived with two machine guns and *10,000 rounds*. The emus split into small groups and ran in every direction.",
        say="The Great Emu War. Major Meredith arrived with two machine guns and ten thousand rounds. The emus split into small groups and ran in every direction."),
   dict(title="The scoreboard", body="His report claimed 986 emus for 9,860 bullets. That's *ten bullets a bird*, with thousands of emus still eating wheat. The army went home.",
        say="The scoreboard. His report claimed nine hundred and eighty-six emus, for nine thousand eight hundred and sixty bullets. That's ten bullets a bird, with thousands of emus still eating wheat. The army went home."),
   dict(title="The lesson", body="Raw force fails against a *scattered problem*. Before you reach for a bigger hammer, check you're not *fighting emus*."),
   END], [A.e_hook, A.e_farm, A.e_guns, A.e_score, A.e_lesson]),
 "09_rats": (HIS, [
   dict(title="The rat bounty that made *more rats*", **H),
   dict(body="Hanoi, 1902. French colonial officials have a rat problem. Their bright idea: pay *one cent* for every rat tail handed in.",
        say="Hanoi, nineteen oh two. French colonial officials have a rat problem. Their bright idea: pay one cent for every rat tail handed in."),
   dict(title="It worked! Sort of.", body="Tails poured in by the thousand. Then officials noticed something odd in the streets: healthy rats with *no tails*."),
   dict(title="The loophole", body="Hunters were snipping the tails and *letting the rats go* to breed. Some people even set up *rat farms* outside the city."),
   dict(title="The Cobra Effect", body="Reward a number, and people will *deliver the number*. Before you set any target, ask: what's the sneakiest way to hit this?"),
   END], [B.r_hook, B.r_office, B.r_tails, B.r_loop, B.r_cobra]),
 "10_parkinson": (PRO, [
   dict(title="Why a 2-hour task takes *exactly* 2 weeks", say="Why a two-hour task takes exactly two weeks.", **H),
   dict(body="In 1955, historian C. Northcote Parkinson opened an essay in The Economist with one line that *still stings*.",
        say="In nineteen fifty-five, historian C. Northcote Parkinson opened an essay in The Economist with one line that still stings."),
   dict(title="Parkinson's Law", body="*Work expands* to fill the time available for its completion."),
   dict(title="His example", body="A lady with a free day can spend *all of it* sending one postcard: an hour finding the card, another hunting for her glasses, more choosing the words."),
   dict(title="Use it", body="Give tasks *less time* than feels comfortable. Set the deadline first, then start. The work will *shrink to fit*."),
   END], [B.p_hook, B.p_essay, B.p_law, B.p_lady, B.p_use]),
 "11_pomodoro": (PRO, [
   dict(title="How a *tomato* fixed a student's focus", **H),
   dict(body="Italy, late 1980s. University student Francesco Cirillo *can't concentrate*. In desperation, he grabs a kitchen timer shaped like a tomato.",
        say="Italy, late nineteen eighties. University student Francesco Chirillo can't concentrate. In desperation, he grabs a kitchen timer shaped like a tomato."),
   dict(title="The Pomodoro Technique", body="*25 minutes* on one task, nothing else. Then a 5-minute break. After four rounds, take a longer one.",
        say="The Pomodoro Technique. Twenty-five minutes on one task, nothing else. Then a five-minute break. After four rounds, take a longer one."),
   dict(title="Why it works", body="\"Write the report\" is scary. \"Work until the tomato rings\" is not. A short timer makes starting *feel small*."),
   dict(title="Try it now", body="Pick one task. Set 25 minutes. Phone *in another room*. When it rings, stop and stretch. That's one pomodoro.",
        say="Try it now. Pick one task. Set twenty-five minutes. Phone in another room. When it rings, stop and stretch. That's one pomodoro."),
   END], [B.m_hook, B.m_student, B.m_cycle, B.m_small, B.m_try]),
 "12_duck": (PRO, [
   dict(title="Stuck? Explain it to a *rubber duck*", **H),
   dict(body="Programmers have a strange secret weapon. It's yellow, it squeaks, and it has *never written a line of code*."),
   dict(title="Rubber duck debugging", body="The 1999 book The Pragmatic Programmer tells of a developer who explained his code, *line by line*, to a rubber duck.",
        say="Rubber duck debugging. The nineteen ninety-nine book, The Pragmatic Programmer, tells of a developer who explained his code, line by line, to a rubber duck."),
   dict(title="Why it works", body="To explain something simply, you have to *slow down* and spell out every step. That's usually where the mistake is hiding."),
   dict(title="Use it", body="Stuck on an email, a plan, a decision? Explain it *out loud* to a duck, a plant or the cat. The duck says nothing. *The duck is always right.*"),
   END], [B.u_hook, B.u_secret, B.u_book, B.u_why, B.u_use]),
 "13_two_minute": (PRO, [
   dict(title="The *2-minute rule* that empties your to-do list", say="The two-minute rule that empties your to-do list.", **H),
   dict(body="Your list is full of tiny jobs. Reply to Sam. Book the dentist. Each one costs more energy to *remember* than to do."),
   dict(title="The Two-Minute Rule", body="From David Allen's book Getting Things Done: if a task takes *less than two minutes*, do it the moment it shows up."),
   dict(title="The maths", body="Writing it down, re-reading it and feeling guilty about it takes *longer* than just doing it."),
   dict(title="Try it today", body="Next small task that lands: no list, no \"later\". *Two minutes, done, gone.* Save the list for the things that deserve it."),
   END], [B.t_hook, B.t_tiny, B.t_rule, B.t_math, B.t_today]),
}

for k, (tag, cards, fns) in L.items():
    animate.REELS[k] = (tag, cards)
    SCENES[k] = fns + [end_card]
