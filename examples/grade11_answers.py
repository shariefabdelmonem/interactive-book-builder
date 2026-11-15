import json, re, textwrap
from blocks import blocks
from imgtools import hlines
D = json.load(open('all.json'))
B = {}
def blk(n):
    if n not in B: B[n] = blocks(n)
    return B[n]
def blanks(n): return D[str(n)]['blanks']

FS = 16          # default answer size (pt)
ZONES = {}

def T(x0, x1, y, txt, fs=FS): return {'k': 't', 'x0': x0, 'x1': x1, 'y': y, 'txt': txt, 'fs': fs}
def C(b): return {'k': 'c', 'b': b}
def on_blank(b, txt, fs=FS, left=False):
    x0, y0, x1, y1 = b[:4]
    return T(x0 + 3, None, y1 - 4, txt, fs) if left else T(x0, x1, y1 - 4, txt, fs)
def ebox(e):
    if e['k'] == 'c': return e['b']
    w = len(e['txt']) * e['fs'] * .45
    x0 = e['x0'] if e['x1'] is None else (e['x0'] + e['x1']) / 2 - w / 2
    return [x0, e['y'] - e['fs'], x0 + w, e['y'] + 3]
def Z(n, label, els, key, flag=None, extra=None, pop=None):
    bs = [ebox(e) for e in els] + ([extra] if extra else [])
    x0 = min(b[0] for b in bs); y0 = min(b[1] for b in bs); x1 = max(b[2] for b in bs); y1 = max(b[3] for b in bs)
    box = [round(min(x0, 44), 1), round(y0 - 4, 1), round(max(x1, 556), 1), round(y1 + 4, 1)]
    ZONES.setdefault(n, []).append({'id': f'{n}-{len(ZONES.get(n, []))}', 'label': label, 'box': box, 'a': els, 'key': key, 'flag': flag, 'pop': pop})

def mcq(n, bi, letter, gap=True, label=None, flag=None):
    b = blk(n)[bi]
    opt = [o for o in b['opts'] if o[4].strip().startswith(letter + '.')][0]
    els = [C([opt[0] - 2, opt[1] + 1, opt[2] + 2, opt[3] - 1])]
    txt = re.sub(r'^[A-D]\.\s*', '', opt[4]).strip()
    if gap and b['blanks']: els.append(on_blank(b['blanks'][0], txt))
    num = re.match(r'^(\d+)', b['head'][4])
    Z(n, label or (f'Q{num.group(1)}' if num else 'Q'), els, f'{letter}. {txt}', flag, extra=b['head'][:4])

def fill(n, bi, txt, label=None, flag=None, k=0, fs=FS):
    b = blk(n)[bi]
    num = re.match(r'^(\d+)', b['head'][4])
    Z(n, label or (f'{num.group(1)}' if num else 'Q'), [on_blank(b['blanks'][k], txt, fs)], txt, flag, extra=b['head'][:4])

def pblank(n, idx_txt, label, fs=FS, left=False, flag=None):
    bl = blanks(n)
    els = [on_blank(bl[i], t, fs, left) for i, t in idx_txt]
    Z(n, label, els, ' / '.join(t for _, t in idx_txt), flag)

def seg(s, txt, fs=FS, left=False):  # image-detected line [x0,x1,y]
    x0, x1, y = s
    return T(x0 + 3, None, y - 3, txt, fs) if left else T(x0, x1, y - 3, txt, fs)

# ---------------------------------------------------------------- PAGE 1
L1 = hlines(1, (30, 230, 570, 385))
rows = sorted(set(s[2] for s in L1)); cols = sorted(set((s[0], s[1]) for s in L1))
cols = [c for c in cols if True]
colx = sorted({round(s[0]) : s for s in L1}.values(), key=lambda s: s[0])
IN = ['trouble','the future','the mood for','a hurry','a mess','cash','charge of','debt','particular','public','one’s interest','tears','the long run','the meantime']
ON = ['holiday','tour','purpose','the run','good terms','fire','display','sale','second thoughts','the phone','behalf of','the verge of']
def cell(c, r):
    s = [q for q in L1 if abs(q[0] - colx[c][0]) < 4 and abs(q[2] - rows[r]) < 2][0]; return s
els = [seg(cell(0 if i < 7 else 1, i % 7), w, 15) for i, w in enumerate(IN)] + [seg(cell(2 if i < 6 else 3, i % 6), w, 15) for i, w in enumerate(ON)]
Z(1, 'Table: in / on', els, 'in: ' + ', '.join(IN) + '<br>on: ' + ', '.join(ON))
mcq(1, 0, 'B'); mcq(1, 1, 'A')
# ---------------------------------------------------------------- PAGE 2-3
for bi, l in enumerate('BABAA'): mcq(2, bi, l)
for bi, l in enumerate('BADD'): mcq(3, bi, l)
# ---------------------------------------------------------------- PAGE 4
for bi, t in enumerate(['around', 'along', 'away', 'through', 'by', 'with', 'through', 'by', 'away', 'to']):
    fill(4, bi, t, label=('List 1 – ' if bi < 5 else 'List 2 – ') + str(bi % 5 + 1))
# ---------------------------------------------------------------- PAGE 5
for bi, t in enumerate(['ecosystem', 'predators', 'delicate', 'prey', 'chain']): fill(5, bi, t)
L5 = [s for s in hlines(5, (30, 560, 580, 800))]
for i, t in enumerate(['effect', 'need', 'increase', 'advantage', 'increase', 'reason', 'threat', 'importance', 'damage', 'solution']):
    Z(5, f'Nouns {i+1}', [seg(L5[i], t)], t, flag=('the sentence also allows “decrease”; “increase” matches “More and more people…”' if i == 2 else None))
# ---------------------------------------------------------------- PAGE 6
L6 = hlines(6, (30, 410, 570, 600))
for i, t in enumerate(['over', 'over', 'under', 'over', 'over', 'under']):
    Z(6, f'Compound {i+1}', [seg(L6[i], t, 18)], t + ['rated', 'paid', 'estimate', 'use', 'cooked', 'charge'][i])
mcq(6, 0, 'A')
# ---------------------------------------------------------------- PAGE 7
mcq(7, 0, 'B'); mcq(7, 1, 'D')
for bi, t in enumerate(['undercooked', 'underestimated', 'underfed', 'underpaid', 'undercharged']): fill(7, 2 + bi, t, label='List 1 – ' + str(bi + 1))
for bi, t in enumerate(['overrated', 'overpaid', 'overfed', 'overhunted', 'overused']): fill(7, 7 + bi, t, label='List 2 – ' + str(bi + 1))
# ---------------------------------------------------------------- PAGE 8
L8 = hlines(8, (30, 300, 570, 800))
p8 = {1: 'actually', 2: 'exactly', 3: 'literally', 4: 'case', 5: 'event', 6: 'situation', 7: 'scenario', 8: 'remind', 9: 'memorise',
      10: 'remembered', 11: 'single', 12: 'rare', 13: 'unique', 14: 'matches', 15: 'combine', 16: 'connect'}
order8 = [8, 1, 2, 9, 3, 10, 4, 5, 11, 12, 6, 7, 13, 14, 15, 16]
for s, q in sorted(zip(L8, order8), key=lambda z: z[1]):
    Z(8, f'{q}', [seg(s, p8[q])], p8[q])
# ---------------------------------------------------------------- PAGE 9
circ9 = [('1', [257.9, 274.9, 327.6, 282.2], 'appalled'), ('2', [193.5, 297.2, 261.4, 304.7], 'pleasing'), ('3', [256.7, 319.5, 341.6, 326.9], 'disgusting'),
         ('4', [68.2, 331.4, 134.6, 337.5], 'Alarmed'), ('5', [262.8, 353.7, 369.2, 360.9], 'disappointed'), ('6', [298.8, 376.2, 410.5, 383.4], 'embarrassing'),
         ('7', [274.9, 398.7, 349.0, 404.6], 'confused'), ('8', [216.5, 421.0, 296.6, 428.4], 'depressed')]
for q, b, w in circ9: Z(9, f'Circle {q}', [C([b[0] - 2, b[1] - 3, b[2] + 2, b[3] + 3])], w)
L9 = hlines(9, (30, 440, 580, 800))
suf = ['fascination', 'measurement', 'realisation', 'reflection', 'expectation', 'announcement']
Z(9, 'Suffixes', [seg(L9[i], t, 14) for i, t in enumerate(suf)], ', '.join(suf))
for i, t in enumerate(['disappointment', 'cancellation', 'imagination', 'inspiration', 'motivation', 'achievement', 'connection', 'prevention']):
    Z(9, f'Form {i+1}', [seg(L9[6 + i], t)], t)
# ---------------------------------------------------------------- PAGE 10
L10 = hlines(10, (20, 100, 600, 180))
top = {('L', 113.4): None}
form10 = [(L10[1], 'noun (sense) + ible'), (L10[2], 'verb (wear) + able'), (L10[3], 'verb (act) + ive'), (L10[4], 'noun (wealth) + y'),
          (L10[5], 'noun (mystery) + ious'), (L10[6], 'noun (fame) + ous')]
Z(10, 'How adjectives are formed', [seg(s, t, 13, left=True) for s, t in form10], '; '.join(t for _, t in form10))
cx = [(49, 130.5), (131.8, 212.4), (215.6, 295.2), (319, 441), (441, 565.6)]
ry = [326, 352.5, 379, 405.5]
tbl = [['beneficial', 'financial', 'educational', 'global'], ['intensive', 'decisive', 'cooperative', 'protective'], ['healthy', 'risky', 'dirty', 'dusty'],
       ['spacious', 'adventurous', 'humorous', 'furious'], ['accessible', 'predictable', 'reusable', 'advisable']]
Z(10, 'Adjective table', [T(cx[c][0], cx[c][1], ry[r], w, 13) for c, col in enumerate(tbl) for r, w in enumerate(col)],
  ' | '.join(['-al: ', '-ive: ', '-y: ', '-ous/-ious: ', '-able/-ible: '][c] + ', '.join(col) for c, col in enumerate(tbl)))
for bi, t in enumerate(['dusty', 'predictable', 'humorous', 'dirty', 'global', 'educational', 'accessible', 'risky', 'financial', 'advisable']): fill(10, bi, t)
# ---------------------------------------------------------------- PAGE 11
b = blk(11)[0]; Z(11, 'A', [on_blank(b['blanks'][0], 'combines'), on_blank(b['blanks'][1], 'impact')], 'A. combines  B. impact', extra=b['head'][:4])
for bi, t, lab in [(2, 'underpaid', 'B1'), (3, 'situation', 'B2'), (5, 'educational', 'C1'), (6, 'achievement', 'C2'), (8, 'unique', 'D1'), (9, 'exactly', 'D2')]: fill(11, bi, t, label=lab)
# ---------------------------------------------------------------- PAGE 12
for lab, it in [('this time yesterday', [(0, 'was watching')]), ('at three p.m.', [(1, 'was doing')]), ('Negation', [(2, 'wasn’t sleeping'), (3, 'was playing')]),
                ('Negation 2', [(4, 'was working')]), ('Yes/No 1', [(5, 'driving')]), ('Yes/No 2', [(6, 'Were')]), ('Wh 1', [(7, 'were you doing')]), ('Wh 2', [(8, 'were you driving')])]:
    pblank(12, it, lab, flag=("listed under Negation, but the meaning (she didn’t even hear the call) needs the positive form “was working”" if lab == 'Negation 2' else None))
# ---------------------------------------------------------------- PAGE 13
for lab, it in [('When 1', [(0, 'heard'), (1, 'was doing')]), ('When 2', [(2, 'was reading'), (3, 'rang')]), ('While 1', [(4, 'were washing'), (5, 'started')]),
                ('While 2', [(6, 'started'), (7, 'were washing')]), ('While 3', [(8, 'called'), (9, 'was jogging')]), ('While 4', [(10, 'was jogging'), (11, 'was watching')])]:
    pblank(13, it, lab)
# ---------------------------------------------------------------- PAGE 14
mcq(14, 1, 'D', label='A. Q1'); mcq(14, 2, 'D', label='A. Q2')
for i, t in enumerate(['were watching', 'heard', 'was shopping', 'received', 'was', 'doesn’t meet', 'was watching']):
    fill(14, 4 + i, t, label=f'B. {i+1}', flag=('the sentence is incomplete in the original (it starts with “but now he…”)' if i == 5 else None))
# ---------------------------------------------------------------- PAGE 15
rw15 = [(1, 'My grandfather used to take me to the gym every day when I was in Primary six.'), (3, 'I used to stay in a hotel in London when I was there ten years ago.'),
        (5, 'When she was young, my sister would watch TV for hours.'), (8, 'I was going to take my brother to the gym, but he got sick.'),
        (9, 'We were going to stay in a hotel, but we couldn’t because we had no money.'), (10, 'They were going to travel to London, but their mother got sick.')]
for k, (i, t) in enumerate(rw15): pblank(15, [(i, t)], f'Rewrite {k+1}', fs=14, left=True)
# ---------------------------------------------------------------- PAGE 16-17
for bi, l in enumerate('BDCADD'): mcq(16, bi, l)
mcq(17, 0, 'D'); mcq(17, 1, 'B')
for k, (i, t) in enumerate([(2, 'used to walk to school when he was a child.'), (4, 'used to win football matches when he was in school.'),
                           (7, 'were going to participate in the race, but our car broke down.'), (9, 'was going to visit the Tower of London, but he ran out of time.'),
                           (11, 'was going to buy a new car, but he chose to redecorate his old house.')]):
    pblank(17, [(i, t)], f'Rewrite {k+1}', fs=14, left=True, flag=('“would walk” is also correct' if k == 0 else None))
# ---------------------------------------------------------------- PAGE 18-19
mcq(18, 1, 'B'); mcq(18, 2, 'B'); mcq(18, 3, 'C')
mcq(19, 0, 'A')
for i, t in enumerate(['gave', 'had done', 'had finished', 'arrived', 'went', 'had left', 'had afforded', 'had left', 'had escaped', 'were sleeping', 'were talking', 'went']):
    fill(19, 2 + i, t, label=f'B. {i+1}')
# ---------------------------------------------------------------- PAGE 20-21
for bi, l in enumerate('ACDB'): mcq(20, bi, l)
L21 = hlines(21, (30, 50, 600, 800))
Z(21, 'Rules', [seg(L21[0], 'adjective', 13), seg(L21[1], 'noun', 13), seg(L21[2], 'in order', 13)], 'adjective / noun / in order')
rw21 = ['It was such an isolated village that it took us two days on foot to reach it.', 'You must study for many years in order to become a vet.',
        'He was very careful so as not to fall when he was climbing the tree.', 'The view was so impressive that everybody stopped to admire it.',
        'I brought extra clothes so that I wouldn’t get cold at night.']
for i, t in enumerate(rw21): Z(21, f'Rewrite {i+1}', [seg(L21[4 + i], t, 14, left=True)], t)
# ---------------------------------------------------------------- PAGE 22-23
rw22 = [(0, '1A', 'Abdullah can climb mountains easily.'), (2, '1B', 'Ahmed couldn’t travel to London last summer because he had no money.'),
        (4, '2A', 'You mustn’t use the car horn in this area.'), (6, '2B', 'You can’t smoke inside the mall.'),
        (8, '3A', 'Mohamed may / might attend the French classes.'), (10, '3B', 'She could have won the gold medal.'),
        (12, '4A', 'You must go through the brochure before checking in.'), (14, '4B', 'In the past, you had to have a license to go camping.')]
for i, lab, t in rw22: pblank(22, [(i, t)], lab, fs=14, left=True)
rw23 = [(0, '5A', 'Ali needn’t go through the brochure before checking in.'), (2, '5B', 'You don’t have to have a license to go camping.'),
        (4, '6A', 'You had better go on a picnic after exams.'), (6, '6B', 'You ought to have given your studies your best shot.'),
        (8, '7A', 'May I get out of the class, please?'), (10, '7B', 'Could I borrow your English book, please?'),
        (12, '8A', 'Would you turn on the AC for me, please?'), (14, '8B', 'Could you lend me your English book, please?')]
for i, lab, t in rw23: pblank(23, [(i, t)], lab, fs=14, left=True)
# ---------------------------------------------------------------- PAGE 24-25
for lab, it in [('Present simple', [(0, 'leaves'), (1, 'starts'), (2, 'begins')]), ('Arranged events', [(3, 'am travelling'), (4, 'am visiting')]),
                ('Temporary', [(5, 'am working'), (6, 'am studying')]), ('will 1', [(7, '’ll get'), (8, '’ll help')]), ('will 2', [(9, 'will cut'), (10, 'will study')]), ('will 3', [(11, '’ll call')])]:
    pblank(24, it, lab)
for lab, it in [('going to', [(0, 'am going to visit'), (1, 'am going to study'), (2, 'is going to be')]), ('Future continuous', [(7, 'will be playing'), (8, 'will be driving')]),
                ('Future perfect', [(9, 'will have started'), (10, 'will have finished')]), ('Future perfect continuous', [(11, 'will have been living'), (12, 'will have been working')])]:
    pblank(25, it, lab)
# ---------------------------------------------------------------- PAGE 26-27
for bi, l in zip([i for i, b in enumerate(blk(26)) if len(b['opts']) == 4], 'ACBCDC'): mcq(26, bi, l)
for bi, l in enumerate('BACCDD'): mcq(27, bi, l)
# ---------------------------------------------------------------- PAGE 28-31 (reading)
mcq(28, 0, 'D', gap=False)
mcq(29, 0, 'C', gap=False); mcq(29, 1, 'D', gap=False)
b = blk(29)[2]; Z(29, 'Q4 T/F/NG', [on_blank(b['blanks'][0], 'T', 20), on_blank(b['blanks'][1], 'NG', 20)], 'A. T   B. NG', extra=b['head'][:4])
L29 = hlines(29, (160, 480, 570, 800), minlen=150)
def tw(L, i, t): return T(172, None, L[i][2] - 3, t, 14)
Z(29, 'Q5 benefits', [tw(L29, 1, 'Commuting and travel are more convenient (ride-sharing'), tw(L29, 2, 'services have simplified daily commutes).'),
                      tw(L29, 3, 'Air travel is more accessible: affordable fares and'), tw(L29, 4, 'efficient check-in processes.')],
  '1) commuting and travel more convenient (ride-sharing) 2) air travel more accessible (affordable fares, efficient check-in)', flag='model answer: accept any two correct benefits from paragraph 3', extra=blk(29)[3]['head'][:4])
Z(29, 'Q6 examples', [tw(L29, 6, 'Smart appliances such as advanced vacuum cleaners'), tw(L29, 7, 'and voice-controlled devices.'),
                      tw(L29, 8, 'Home automation systems control lighting,'), tw(L29, 9, 'temperature and security.')],
  '1) smart appliances / vacuum cleaners / voice-controlled devices 2) home automation (lighting, temperature, security)', flag='model answer: accept any two correct examples from paragraph 4', extra=blk(29)[4]['head'][:4])
mcq(30, 0, 'B', gap=False)
mcq(31, 0, 'B', gap=False); mcq(31, 1, 'C', gap=False)
b = blk(31)[2]; Z(31, 'Q4 T/F/NG', [on_blank(b['blanks'][0], 'F', 20), on_blank(b['blanks'][1], 'NG', 20)], 'A. F   B. NG', extra=b['head'][:4])
L31 = hlines(31, (160, 480, 570, 800), minlen=150)
Z(31, 'Q5 signs', [tw(L31, 1, 'Life expectancy was lower.'), tw(L31, 3, 'Diseases that are now preventable or treatable were'), tw(L31, 4, 'major causes of death.')],
  '1) life expectancy was lower 2) preventable diseases were major causes of death (or: limited access to healthcare facilities and trained professionals)', flag='model answer: “limited access to healthcare facilities and trained medical professionals” is also correct', extra=blk(31)[3]['head'][:4])
Z(31, 'Q6 aspects', [tw(L31, 6, 'The lack of job opportunities.'), tw(L31, 8, 'Income disparity and limited social welfare systems.')],
  '1) lack of job opportunities 2) income disparity / limited social welfare systems', flag='model answer: accept any two aspects from paragraph 4', extra=blk(31)[4]['head'][:4])
# ---------------------------------------------------------------- PAGE 32-34 (writing)
ESSAY = ("Some people dream of growing up in a big family, while others prefer a small one. In my opinion, a big family has clear advantages, but it also has some disadvantages that we should not ignore. "
         "On the one hand, a big family gives you constant support. When you face a problem, there is always a brother, a sister or a cousin who is ready to help you. Moreover, there is never a boring moment at home. "
         "Family gatherings, meals and trips are full of fun, and children learn to share and cooperate from an early age. "
         "On the other hand, living in a big family means having very little privacy. You often share your room and your things, and it can be difficult to find a quiet place to study. "
         "In addition, younger children may copy bad habits from older brothers or cousins, such as staying up late or spending too much time on video games. "
         "To sum up, although a big family can be noisy and crowded, I believe its advantages are greater than its disadvantages. With clear rules and caring parents, a big family can be the best place to grow up.")
STORY = ("Last summer, I learned a lesson that made me a better person. It happened at a football pitch near our house in Doha on a hot Friday afternoon. "
         "My friends and I were playing a match when a new boy called Omar asked to join us. He was shy and he did not play very well. At first, I laughed at him and told him to go home. Omar looked sad and walked away slowly. "
         "While I was walking home, I saw Omar sitting alone on a bench. He told me that his family had just moved to Qatar and that he did not have any friends. "
         "Suddenly, I felt ashamed of what I had done. I apologised and invited him to play with us the next day. "
         "From that day on, Omar became one of my closest friends. We used to practise together every evening, and he became a great defender. "
         "This experience taught me to be kind to others and never to judge people too quickly. Now I always try to welcome new students at school.")
L33 = hlines(33, (30, 40, 600, 800)); L34 = hlines(34, (10, 20, 600, 800))
def para(L, text, start):
    lines = textwrap.wrap(text, 78); return [T(L[start + i][0] + 6, None, L[start + i][2] - 5, ln, 13.5) for i, ln in enumerate(lines)]
e33 = para(L33, ESSAY, 1); e34 = para(L34, STORY, 1)
Z(33, 'Model essay – Topic B', e33, 'Model argumentative essay (Topic B) written on page 33', flag='model answer for students to compare with — not the only correct answer')
Z(34, 'Model story – Topic A', e34, 'Model story (Topic A) written on page 34', flag='model answer for students to compare with — not the only correct answer')
Z(32, 'Topic A → model on page 34', [T(390, None, 98, 'Model story: page 34 →', 15)], 'see page 34', extra=[50, 60, 560, 345])
Z(32, 'Topic B → model on page 33', [T(330, None, 668, 'Model essay: page 33 →', 15)], 'see page 33', extra=[50, 440, 560, 650])

out = {str(k): v for k, v in sorted(ZONES.items())}
json.dump(out, open('/home/claude/g11book/data.json', 'w'), ensure_ascii=False)
print({k: len(v) for k, v in out.items()}, sum(len(v) for v in out.values()), 'zones')
print('lines33', len(L33), 'essay lines', len(e33), '| lines34', len(L34), 'story lines', len(e34))
