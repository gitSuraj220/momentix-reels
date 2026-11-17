"""English subtitles (SRT) for the AI Bubble long video, timed from shots.json (t0/t1 per shot).
Run: python3 make_srt_en.py -> final/AI_Bubble_EN.srt"""
import json, re

EN = {
1: "The CEO of the world's most hyped AI company is stressed.",
2: "Because his ChatGPT has reached almost every home...",
3: "...and yet the company keeps losing money.",
5: "Welcome to the AI era...",
6: "...where a simple chatbot turned into a $7 trillion gamble almost overnight.",
7: "30 November 2022. A Wednesday.",
8: "At one company, everything was normal.",
9: "People were drinking coffee, sharing memes, developers were fixing bugs.",
10: "And that same day, OpenAI dropped its chatbot... ChatGPT.",
12: "Within 24 hours, the internet had a new obsession.",
13: "Someone was writing emails with it, someone was fixing code, and someone was writing their breakup story.",
14: "SON: Dad, I'm talking to an AI bot... that can make us crorepatis!",
15: "DAD: How?",
16: "SON (typing): \"Build me a ₹100 crore business in 1 minute. 100% profit. And no mistakes.\"",
17: "ChatGPT went so viral that it got 1 million users in just 5 days.",
18: "And 100 million in 2 months.",
19: "Instagram took two and a half years to reach 100 million users. Facebook took four and a half.",
20: "ChatGPT became... the fastest-growing app in history.",
21: "Then... Google's headquarters went into full panic mode.",
22: "BOSS: This technology is ours! We built the Transformer model! What happened to it?",
23: "BOSS: Then why is my own son using ChatGPT instead of Google's AI?",
24: "ENGINEER: Because... we were scared to launch it.",
25: "BOSS: Then launch anything now! Call it Bard, call it Gemini, call it whatever you want. Just launch it!",
26: "Google went into full hustle mode.",
27: "It had the technology for years.",
28: "But the company was scared... that the AI might say something wrong, there might be a lawsuit, or its name might get dragged in the media.",
29: "And OpenAI? It launched without fear.",
30: "Within weeks, Microsoft put $10 billion into OpenAI. And kept another $3 billion ready on the side.",
31: "Google rushed to launch Bard...",
32: "USER: Gemini, tell me, who is the most popular person in the world?",
33: "GEMINI: Modi Ji.",
34: "- USER: Who is Modi Ji?\n- GEMINI: The Modi government.",
35: "And that's it... on day one, Gemini made a complete mess.",
36: "On the other side, Amazon started pouring billions into Anthropic.",
37: "And this was the investors' scene...",
38: "STARTUP: Our app takes dogs for walks...",
39: "...but we use machine learning to pick the best route.",
40: "INVESTOR: Shh! Here's $50 million.",
41: "STARTUP: Won't you look at our demo?",
42: "PITCHER (2023): We're building an app that lets you talk directly to Voldemort... in Python.",
43: "JUDGE: Next, please.",
44: "PITCHER: We're using AI in it.",
45: "- JUDGE: AI? Really?\n- PITCHER: Yes.",
46: "JUDGE: Here's $100 million.",
47: "One company even raised $30 million to build an AI...",
48: "...whose job was to give back another AI's answers under a new name.",
49: "But the real madness was... the GPU shortage.",
50: "These tiny computer chips suddenly became more valuable than gold and oil.",
51: "And Nvidia became the most valuable company in the world.",
52: "Nvidia's CEO Jensen Huang started showing up at conferences in a leather jacket... like a rockstar.",
53: "And in a way... he was one.",
54: "Renting one high-end GPU cost about $3 an hour.",
55: "Sounds cheap, right?",
56: "But a startup's work was never going to run on one GPU...",
57: "Even a small startup may rent 500 chips just to train one model.",
58: "That's $1,500 an hour.",
59: "$36,000 a day.",
60: "And over $1.1 million a month. Just in GPU rent.",
61: "Still, companies were hoarding GPUs... as if the world was ending and people were stocking up on rations.",
62: "As fast as Nvidia made chips, demand grew even faster.",
63: "At one point, the waiting list reached 12 months.",
64: "A black market started.",
65: "People began smuggling these chips across borders.",
66: "By 2024, everything had become \"AI-powered\".",
67: "Your toaster could now burn bread 10% more efficiently.",
68: "Your calendar app was suggesting meeting times with an algorithm.",
69: "And the supermarket self-checkout? The camera was always there...",
70: "...it just got renamed \"machine learning\".",
71: "The party was in full swing.",
72: "Champagne was popping. Cheques were clearing.",
73: "Then someone asked that awkward question...",
74: "\"Bro... how much does it cost to run all this?\"",
75: "January 2025.",
76: "Sam Altman posted a tweet that sent investors' blood pressure through the roof.",
77: "\"We're losing money on OpenAI Pro subscriptions. People use it much more than we expected.\"",
78: "Yes, you heard that right.",
79: "OpenAI charges $200 a month for its Pro plan. And still loses money on every subscriber.",
80: "But wait... the story gets worse.",
81: "Look at OpenAI's numbers for 2024. Revenue: $3.7 billion. Loss: $5 billion.",
82: "The company didn't just fail to make a profit... it burned more than it earned.",
83: "Now comes the really shocking part.",
84: "According to one research firm, running AI and its data centres will need $6.7 trillion by 2030.",
85: "Let's break that down. $5.2 trillion goes straight into AI infrastructure: GPUs, chips, power, cooling and building data centres.",
86: "The remaining $1.5 trillion goes into cloud infrastructure.",
87: "And just the four biggest tech companies were expected to spend $350 billion in 2025. In one year.",
88: "To justify this spending, AI companies would need to earn $2 trillion every year by 2030.",
89: "And the whole AI industry's revenue today? About $200 billion.",
90: "So revenue has to grow 10 times.",
91: "BOARD MEMBER: Sam, by our numbers revenue will be $20 billion in 2025. And you're saying you'll reach $100 billion by 2029?",
92: "SAM: We need to grow at exactly this speed.",
93: "BOARD MEMBER: Sam, that's not speed. That's a hockey-stick graph drawn by someone who has never played hockey.",
94: "- BOARD MEMBER: Do you know how much just trying will cost?\n- SAM: $115 billion of cash burn by 2029.",
95: "- BOARD MEMBER: And when will profit come?\n- SAM: In 2029. Maybe 2030. Or 2031?",
96: "BOARD MEMBER: And if revenue doesn't reach $100 billion? What if your hockey stick breaks?",
97: "SAM: Then we'll raise more money.",
98: "BOARD MEMBER: From whom? Who's left? Microsoft? Saudi Arabia? Some pension fund that's a bit too optimistic?",
99: "SAM: Come on, the world isn't short of investors!",
100: "Since 2021, private investors have poured hundreds of billions of dollars into AI startups.",
101: "Most of it went to just 10 companies, whose total value grew by about $1 trillion.",
102: "Everyone was making the same bet... that one of them would become the next Google.",
103: "Then the cracks started to show.",
104: "ChatGPT started to \"hallucinate\".",
105: "In tech language, that means... making things up with complete confidence.",
106: "Citing research papers that don't exist.",
107: "Court cases that never happened.",
108: "And numbers that probably came from another planet.",
109: "Google's AI told a user to add glue to pizza so the cheese would stick.",
110: "It learned that from a joke on Reddit. Yes, really.",
111: "Then the lawsuits began.",
112: "Writers, artists, journalists... all had the same question: \"Did you train your AI on my copyrighted work?\"",
113: "The answer? \"Umm... yes.\"",
114: "The New York Times sued OpenAI. Getty Images sued Stability AI.",
115: "Writers dragged companies to court. Artists went after the rest.",
116: "AI COMPANY: We didn't steal. We trained our AI on public data.",
117: "ARTIST: You took the whole internet's data without permission... and made money from it.",
118: "AI COMPANY: Well... when you put it like that, it does sound illegal.",
119: "By mid-2024, cracks had started to appear.",
120: "The hype was very loud. But the numbers were scary.",
121: "And now one question was buzzing in everyone's head... just like a mosquito near your ear at 3 AM:",
122: "\"When will this bubble burst?\"",
123: "The losses are huge. Company valuations look far bigger than reality.",
124: "But this bubble isn't bursting the way the dot-com bubble did. Why?",
125: "Because the people inflating it have the deepest pockets in the world.",
126: "In 1999, startups had zero revenue... and 17 foosball tables in the office for fun.",
127: "Today, the big tech companies funding the AI bubble actually make money. A lot of it.",
128: "So much that, if they wanted... they could buy a whole country.",
129: "Microsoft makes billions from Azure.",
130: "Google makes billions from ads.",
131: "Meta makes billions showing you the same meme... your cousin already sent you on WhatsApp.",
132: "These big companies aren't investing in AI because it's profitable right now.",
133: "They're investing... because they're scared of being left behind.",
134: "What if AI becomes the next iPhone moment? The next Google moment?",
135: "What if this is the moment the whole world changes overnight?",
136: "Then the company that slows down... becomes the next BlackBerry. And nobody wants to be BlackBerry.",
137: "Think of these big tech companies as poker players sitting at the table with unlimited money.",
138: "If Microsoft backs off, Google wins. If Google backs off, Amazon wins. If Amazon backs off, Meta wins.",
139: "Nobody is blinking. Nobody is folding. Everyone keeps raising the bet.",
140: "And this is where the really tough question comes in. If everyone keeps spending... how does the bubble burst?",
141: "Short answer: when a real-world event forces everyone... to stop pretending.",
142: "Historically, such events come in two kinds.",
143: "One: the money suddenly stops coming.",
144: "The dot-com bubble didn't burst because building websites was a bad idea.",
145: "It burst because the money tap was shut.",
146: "Interest rates rose. Loans got expensive. Funding vanished.",
147: "And thousands of companies died overnight.",
148: "If interest rates rise in the coming years and big tech tightens its budgets... the AI bubble's game is over instantly.",
149: "Two: a huge, embarrassing failure comes out.",
150: "Every bubble has that moment. A failure so big that everyone panics.",
151: "In the dot-com era, company results crushed expectations.",
152: "In 2008, it was Lehman Brothers.",
153: "In crypto, it was FTX.",
154: "For AI, it could be a big lab revealing a massive loss. A new model's disastrous launch. Or a lawsuit that stops everything.",
155: "So where do we stand right now?",
156: "Big tech is still spending.",
157: "No result has caused an earthquake yet. No FTX-level scam has come out.",
158: "Cracks are showing... but not big enough to break trust.",
159: "So yes, this bubble is inflated. Yes, the numbers are insane.",
160: "But it won't burst just because of hype and noise.",
161: "It will burst when one of these giants finally says... \"Okay. That's enough.\"",
162: "Until then, the bubble will keep floating.",
163: "We're not at the explosion yet. We're at the point where the tension keeps building.",
164: "The breath you take in before a scream.",
165: "The pull on a rope just before it snaps.",
166: "The episode right before the season finale.",
}

def ts(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def wrap(t, n=42):
    if '\n' in t: return t
    words, lines, cur = t.split(), [], ''
    for w in words:
        if len(cur) + len(w) + 1 > n and cur: lines.append(cur); cur = w
        else: cur = (cur + ' ' + w).strip()
    lines.append(cur)
    return '\n'.join(lines)

shots = json.load(open('shots.json'))['shots']
cues = []
for s in shots:
    t = EN.get(s['id'])
    if not t: continue
    t0, t1 = s['t0'], s['t1']
    # split long cues (> ~84 chars) at sentence boundaries, time by character share
    parts = [p for p in re.split(r'(?<=[.?!])\s+(?=[A-Z"$-])', t) if p] if len(t) > 84 and '\n' not in t else [t]
    # merge tiny parts
    merged = []
    for p in parts:
        if merged and (len(merged[-1]) + len(p) < 70): merged[-1] += ' ' + p
        else: merged.append(p)
    tot = sum(len(p) for p in merged); a = t0
    for p in merged:
        b = a + (t1 - t0) * len(p) / tot
        cues.append((a, b - 0.04, p)); a = b
with open('final/AI_Bubble_EN.srt', 'w') as f:
    for i, (a, b, p) in enumerate(cues, 1):
        f.write(f"{i}\n{ts(a)} --> {ts(b)}\n{wrap(p)}\n\n")
print(len(cues), 'cues; last ends', ts(cues[-1][1]))
