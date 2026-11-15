import json, textwrap
exec(open('/home/claude/g10/helpers.py').read())

def lst(n, items, prefix=''):
    for bi, t in items: fill(n, bi, t, label=prefix + str(bi + 1 if not prefix else bi % 6 + 1))

# ---------------- PAGE 1
for bi, t in enumerate(['landscape', 'location', 'area', 'site', 'countryside', 'nature']): fill(1, bi, t, label=f'List 1 – {bi+1}')
for bi, t in enumerate(['location', 'site', 'area', 'landscape', 'countryside', 'nature']): fill(1, 6 + bi, t, label=f'List 2 – {bi+1}')
# ---------------- PAGE 2
pblank(2, [(0, 'arrangement'), (1, 'collection'), (2, 'combination')], 'Verb → noun')
L2 = hlines(2, (40, 280, 600, 480), minlen=20, dark=200)
for i, t in enumerate(['improvement', 'cancellations', 'connection', 'exploration', 'advertisement', 'reservation', 'announcement', 'application']):
    Z(2, f'Capitals {i+1}', [seg(L2[i], t, 15)], t, flag=('“cancellations” (plural after “many”)' if i == 1 else None))
for i, (k, t) in enumerate([(3, 'advertisement'), (4, 'application'), (5, 'announcement'), (6, 'cancellation'), (7, 'reservation'), (8, 'combination')]):
    pblank(2, [(k, t)], ('Set 1 – ' if i < 3 else 'Set 2 – ') + 'ABC'[i % 3])
# ---------------- PAGE 3
for bi in range(4): mcq(3, bi, 'D')
# ---------------- PAGE 4
L4 = hlines(4, (30, 150, 600, 330), minlen=20, dark=200)
left = [s for s in L4 if s[0] < 200]; right = [s for s in L4 if s[0] > 200]
md = ['make', 'do', 'make', 'do', 'do', 'make', 'make', 'do', 'make', 'do', 'make', 'make', 'do', 'do', 'make', 'do', 'make', 'do']
Z(4, 'make / do 1–18', [seg(left[i], md[i], 14) for i in range(9)] + [seg(right[i], md[9 + i], 14) for i in range(9)],
  ' · '.join(f'{i+1} {w}' for i, w in enumerate(md)))
mcq(4, 0, 'B'); mcq(4, 1, 'C'); mcq(4, 2, 'D')
# ---------------- PAGE 5
c5 = [('1', [261.4, 106.7, 295.9, 116.8], 'salary'), ('2', [123.8, 127.1, 164.9, 135.7], 'income'), ('3', [130.7, 147.6, 159.5, 156.2], 'hired'),
      ('4', [170.3, 168.5, 207.0, 176.8], 'rented'), ('5', [124.4, 205.2, 170.1, 215.6], 'position'), ('6', [148.7, 241.7, 167.0, 252.0], 'job'),
      ('7', [238.5, 262.8, 300.4, 272.9], 'knowledge'), ('8', [264.2, 299.0, 326.7, 309.4], 'experience')]
for q, b, w in c5: Z(5, f'Circle {q}', [C([b[0] - 3, b[1] - 2, b[2] + 3, b[3] + 2])], w)
mcq(5, 0, 'B'); mcq(5, 1, 'A'); mcq(5, 2, 'B')
# ---------------- PAGE 6
ys = [145, 158, 183, 208, 233, 246, 271, 296, 321, 335]
mt = ['f', 'e', 'b', 'g', 'h', 'c', 'i', 'a', 'j', 'd']
Z(6, 'Match 1–10', [T(500, 519, y + 4.5, l, 15) for y, l in zip(ys, mt)], ' · '.join(f'{i+1}{l}' for i, l in enumerate(mt)))
mcq(6, 0, 'B'); mcq(6, 1, 'A')
# ---------------- PAGE 7
L7 = hlines(7, (30, 135, 600, 400), minlen=20, dark=200)
L7 = [s for s in L7 if s[1] - s[0] > 40]
ts = ['say', 'say', 'tell', 'told', 'say', 'tell', 'Say', 'tell', 'said', 'telling', 'telling']
Z(7, 'tell / say 1–10', [seg(s, t, 14) for s, t in zip(L7, ts)], ' · '.join(f'{i+1} {t}' for i, t in enumerate(ts[:9])) + ' · 10 telling / telling')
mcq(7, 0, 'C'); mcq(7, 1, 'C')
# ---------------- PAGE 8
ans8 = [['ambitious', 'difference', 'nature'], ['site', 'favours', 'spontaneous'], ['countryside', 'rational', 'area'], ['income', 'disorganised', 'experience'], ['imaginative', 'guess', 'patient']]
for g, row in enumerate(ans8):
    for j, t in enumerate(row): pblank(8, [(g * 3 + j, t)], f'{g+3}{"ABC"[j]}')
# ---------------- PAGE 9 (open sentences – model answers)
m9 = [(0, 'finished my homework'), (1, 'eaten my lunch'), (2, 'moved to Doha'), (3, 'been very busy'), (4, 'finished the project'), (5, 'has lived in Doha'),
      (6, 'been friends'), (7, 'read'), (8, 'met'), (9, 'been'), (10, 'been'), (11, 'has cooked this')]
for r in range(6): pblank(9, m9[2*r:2*r+2], f'Present perfect row {r+1}', fs=11, flag=('model answers – any correct present perfect completion is accepted' if r == 0 else None))
# ---------------- PAGE 10
for lab, it, fl in [('Examples 1', [(1, 'were very happy in our old house')], 'model ending – any correct past simple completion'),
                    ('Examples 2', [(2, 'weren’t')], '“any” signals the negative'), ('Examples 3', [(3, 'used')], None),
                    ('Examples 4', [(4, 'was'), (5, 'had')], None), ('Examples 5', [(6, 'played'), (7, 'went')], None), ('Examples 6', [(8, 'was'), (9, 'beat')], None),
                    ('Negation', [(11, 'didn’t go'), (12, 'didn’t sleep'), (13, 'wasn’t'), (14, 'didn’t speak')], None),
                    ('Yes/No', [(15, 'win'), (16, 'cook')], None), ('Wh', [(17, 'live'), (19, 'reach')], None),
                    ('Mixed 1', [(20, 'speak'), (21, 'act'), (22, 'watch')], None), ('Mixed 2', [(23, 'visited'), (24, 'played'), (25, 'was'), (26, 'slept')], None),
                    ('Mixed 3', [(27, 'saw'), (28, 'called'), (29, 'used'), (30, 'got'), (31, 'opened')], None)]:
    pblank(10, it, lab, fs=11.5, flag=fl)
# ---------------- PAGE 11-12
for bi, l in zip(range(1, 6), 'BCCBC'): mcq(11, bi, l)
b = blk(11)[6]; o = [x for x in b['opts'] if x[4].startswith('B.')][0]
Z(11, 'Q6', [C([o[0] - 2, o[1] + 1, o[2] + 2, o[3] - 1]), on_blank(b['blanks'][0], 'has'), on_blank(b['blanks'][1], 'finished')], 'B. has / finished', extra=b['head'][:4])
mcq(12, 0, 'A'); mcq(12, 1, 'C'); mcq(12, 2, 'A')
b = blk(12)[3]; o = [x for x in b['opts'] if x[4].startswith('B.')][0]
Z(12, 'Q10', [C([o[0] - 2, o[1] + 1, o[2] + 2, o[3] - 1]), on_blank(b['blanks'][0], 'have'), on_blank(b['blanks'][1], 'finished')], 'B. have / finished',
  flag='options B and C are identical in the original (“have / finished”) – both are correct', extra=b['head'][:4])
for i, t in enumerate(['have never been', 'has never eaten', 'hasn’t called', 'visited', 'hasn’t watched', 'moved']): fill(12, 4 + i, t, label=f'Correct {i+1}')

# ---------------- PAGE 13 examples column (model sentences)
EX13 = {'quickly': 'He finished his lunch quickly.', 'carefully': 'Please drive carefully.', 'beautifully': 'She sings beautifully.',
        'easily': 'I solved the problem easily.', 'angrily': 'He shouted angrily.', 'happily': 'The children played happily.',
        'fast': None, 'well': 'Ali speaks English well.', 'hard': 'They work hard every day.',
        'nicer': 'This hotel is nicer than that one.', 'wiser': 'My grandfather is wiser than me.', 'larger': 'Qatar is larger than Bahrain.',
        'taller': 'Hamad is taller than his brother.', 'faster': 'A car is faster than a bike.', 'smaller': 'My room is smaller than yours.',
        'bigger': 'An elephant is bigger than a horse.', 'sadder': 'The film was sadder than the book.', 'thinner': 'This book is thinner than that one.',
        'easier': 'Maths is easier than physics.', 'angrier': 'He was angrier than ever.', 'happier': 'I am happier in my new school.',
        'farther': 'Al Khor is farther than Lusail.', 'worse': 'Today’s weather is worse than yesterday’s.', 'better': 'Your answer is better than mine.',
        'more famous': 'Messi is more famous than his brother.', 'more expensive': 'Gold is more expensive than silver.', 'more important': 'Health is more important than money.'}
rows = [l for l in D['13']['lines'] if l[0] > 140 and l[0] < 220 and l[4].strip() in EX13]
seen = set(); els = []
for l in rows:
    w = l[4].strip(); y = l[3] - 2.5
    if w == 'fast':
        txt = 'He runs fast.' if l[1] < 300 else 'A car is faster than a bike.'
        if l[1] > 300: continue
    else: txt = EX13[w]
    x0 = 222 if l[1] < 320 else 242
    els.append(T(x0 + 4, None, y, txt, 10.5))
Z(13, 'Examples column', els, 'model example sentences for every adjective / adverb / comparison', flag='model examples – students may write their own sentences')
# ---------------- PAGE 14
p14 = ['quietly', 'more informative', 'loudly', 'the most expensive', 'quickly', 'as tiring', 'well', 'more interesting', 'easily', 'better']
for i, t in enumerate(p14): fill(14, i, t)
b = blk(14)[10]; Z(14, '11', [on_blank(b['blanks'][0], 'better'), on_blank(b['blanks'][1], 'better')], 'better and better', extra=b['head'][:4])
b = blk(14)[11]; Z(14, '12', [on_blank(b['blanks'][0], 'good'), on_blank(b['blanks'][1], 'well')], 'good / well', extra=b['head'][:4])
# ---------------- PAGE 15-18 rewrites
for k, (i, t) in enumerate([(8, 'Youssef has to wear the uniform at the Police Academy.'), (10, 'Security guards have to stand up all the time.'),
                           (12, 'Car drivers have to stop at the red traffic lights.'), (14, 'All the students must study hard for tomorrow’s exam.'),
                           (16, 'Last weekend, we had to drive fast to reach home on time.'), (18, 'Last weekend, we needed to drive fast to reach home on time.')]):
    pblank(15, [(i, t)], f'Rewrite {k+1}', fs=14, left=True)
for k, (i, t, f) in enumerate([(8, 'doesn’t have to go to school on Thursday.', None), (10, 'needn’t pay the rent this month.', None),
                              (12, 'didn’t need to go to school on Thursday.', None), (14, 'needn’t have paid the rent this month.', '“didn’t need to pay” is also accepted; “needn’t have paid” means he paid anyway')]):
    pblank(16, [(i, t)], f'Rewrite {k+1}', fs=14, left=True, flag=f)
mcq(17, 1, 'B'); mcq(17, 2, 'D')
for k, (i, t) in enumerate([(5, 'I ought to train harder to win matches.'), (7, 'I should train harder to win matches.'), (9, 'I had better train harder to win matches.')]):
    pblank(17, [(i, t)], f'Rewrite {k+1}', fs=14, left=True)
mcq(18, 1, 'B'); mcq(18, 2, 'A', flag='per the note on the page: “will + inf.” expresses certainty about the future')
pblank(18, [(2, 'Ghanem must be abroad; he is in Spain.')], 'Rewrite 1', fs=14, left=True)
pblank(18, [(4, 'Sultan can’t be at home; his car isn’t in front of the house.')], 'Rewrite 2', fs=14, left=True)
# ---------------- PAGE 19-22 relative clauses
pblank(19, [(0, 'who'), (1, 'who'), (2, 'who')], 'who examples', fs=11.5)
pblank(19, [(6, 'which'), (7, 'which'), (8, 'which')], 'which examples', fs=11.5)
for k, (i, t) in enumerate([(3, 'Khalid is a strong young man who can run for about an hour.'), (4, 'I saw the old man who lent me the money yesterday.'),
                           (5, 'Nasser, who is an astronaut, lives in Doha.'), (9, 'That is the wooden chair which I bought last week.'),
                           (10, 'I ate a cheese sandwich which tasted delicious.'), (11, 'Nasser lives in Doha, which is the capital city of Qatar.')]):
    pblank(19, [(i, t)], ('Join who ' if k < 3 else 'Join which ') + str(k % 3 + 1), fs=14, left=True)
for lab, i, t in [('whose a', 1, 'Einstein is a famous scientist whose inventions helped improve the world.'), ('whose b', 3, 'Ahmed, whose parents died last year, lives in Al Khour.'),
                  ('whose c', 5, 'Salma, whose father is my uncle, got full mark at English.'), ('where a', 10, 'I visited Australia, where I saw a lot of kangaroos.'),
                  ('where b', 12, 'Ahmed lives in Al Khour, where he can do a lot of activities.'), ('where c', 14, 'Salma goes to a British school, where she speaks English all the time.'),
                  ('when a', 17, 'My brother was born in 1973, when Egypt restored Sinai.'), ('when b', 19, 'June, when I was born, is the sixth month of the year.'),
                  ('when c', 21, 'Friday, when Muslims pray altogether, is the end of the week.')]:
    pblank(20, [(i, t)], lab, fs=12, left=True)
for bi, l in zip(range(1, 6), 'DACBD'): mcq(21, bi, l)
for k, t in enumerate(['Yesterday I met a gentleman who works in a nearby health centre.', 'Salman, who solved the puzzle, won the prize.',
                       'Ahmed, whose best friend is a director, doesn’t watch films.', 'Everyone looked for the boy whose parents were looking for him.',
                       'We stayed at Grand Hayat, which is a five-star hotel.', 'Omar took us to the club where he plays football.',
                       'The summer holiday begins in June, when I will meet my British friends.', 'Did you find the CD which you were looking for?']):
    pblank(22, [(k * 2, t)], f'Join {k+1}', fs=14, left=True, flag=('“Omar took us to the club, where he plays football” is also correct' if k == 5 else None))
# ---------------- PAGE 23 passive
for i, t in enumerate(['is predicted', 'was broken', 'was delivered', 'are constructed']): fill(23, 1 + i, t, label=f'A{i+1}')
for k, t in enumerate(['French is spoken fluently by my classmates.', 'Old things are never sold by my grandfather.', 'Classic cars are usually owned by classy people.',
                       'An email was sent to Nasser by Ahmed yesterday.', 'Abdullah’s old car was sold last Friday.', 'In the past, drinking water was bought.']):
    pblank(23, [(5 + k, t)], f'Change {k+1}', fs=14, left=True, flag=('“…was sold by Abdullah last Friday” is also accepted' if k == 4 else None))
for k, (i, t) in enumerate([(11, 'was sent last night.'), (13, 'was written by Dr. Wafaey last year.'), (15, 'were painted green by the artist!')]):
    pblank(23, [(i, t)], f'Rewrite {k+1}', fs=14, left=True)
# ---------------- PAGE 24-27 reading
mcq(24, 0, 'D', gap=False)
mcq(25, 0, 'C', gap=False); mcq(25, 1, 'D', gap=False)
b = blk(25)[2]; Z(25, 'Q4 T/F/NG', [on_blank(b['blanks'][0], 'T', 20), on_blank(b['blanks'][1], 'NG', 20)], 'A. T   B. NG', extra=b['head'][:4])
def tw(L, i, t): return T(172, None, L[i][2] - 3, t, 14)
L25 = hlines(25, (160, 480, 570, 800), minlen=150)
Z(25, 'Q5 benefits', [tw(L25, 1, 'Commuting and travel are more convenient (ride-sharing'), tw(L25, 2, 'services have simplified daily commutes).'),
                      tw(L25, 3, 'Air travel is more accessible: affordable fares and'), tw(L25, 4, 'efficient check-in processes.')],
  '1) commuting and travel more convenient (ride-sharing) 2) air travel more accessible', flag='model answer: accept any two correct benefits from paragraph 3', extra=blk(25)[3]['head'][:4])
Z(25, 'Q6 examples', [tw(L25, 6, 'Smart appliances such as advanced vacuum cleaners'), tw(L25, 7, 'and voice-controlled devices.'),
                      tw(L25, 8, 'Home automation systems control lighting,'), tw(L25, 9, 'temperature and security.')],
  '1) smart appliances / voice-controlled devices 2) home automation (lighting, temperature, security)', flag='model answer: accept any two correct examples from paragraph 4', extra=blk(25)[4]['head'][:4])
mcq(26, 0, 'B', gap=False)
mcq(27, 0, 'B', gap=False); mcq(27, 1, 'C', gap=False)
b = blk(27)[2]; Z(27, 'Q4 T/F/NG', [on_blank(b['blanks'][0], 'F', 20), on_blank(b['blanks'][1], 'NG', 20)], 'A. F   B. NG', extra=b['head'][:4])
L27 = hlines(27, (60, 480, 570, 800), minlen=150)
x27 = 174
def tw2(i, t): return T(x27, None, L27[i][2] - 3, t, 14)
Z(27, 'Q5 signs', [tw2(1, 'Life expectancy was lower.'), tw2(3, 'Diseases that are now preventable or treatable were'), tw2(4, 'major causes of death.')],
  '1) life expectancy was lower 2) preventable diseases were major causes of death', flag='“limited access to healthcare facilities and trained medical professionals” is also correct', extra=blk(27)[3]['head'][:4])
Z(27, 'Q6 aspects', [tw2(6, 'The lack of job opportunities.'), tw2(8, 'Income disparity and limited social welfare systems.')],
  '1) lack of job opportunities 2) income disparity / limited social welfare', flag='model answer: accept any two aspects from paragraph 4', extra=blk(27)[4]['head'][:4])
# ---------------- PAGE 28-30 writing
EMAIL = ["Dear Mr. Abdelaziz Ali,", "",
         "I am writing to ask about the School IELTS Programme which will take place next summer. I am a Grade 10 student and I am very interested in joining it.",
         "First of all, could you please tell me who will be in charge of the programme? I would also like to know whether the teachers will be from our school or from an official IELTS centre.",
         "In addition, I would be grateful if you could tell me what activities are included. Will there be practice tests, speaking sessions and writing workshops?",
         "Finally, I would like to know how long the programme will last and how many hours a week we will study.",
         "I look forward to hearing from you.", "", "Yours sincerely,", "Mohammed Ali – Grade 10"]
ARTICLE = ["Souq Waqif – The Heart of Old Doha", "",
           "Last month, I visited Souq Waqif with my family, and it was one of the best days of my winter holiday. The souq is in the centre of Doha, close to the Corniche, so it is very easy to reach.",
           "What makes Souq Waqif so interesting is its traditional design. The narrow lanes, the old mud walls and the wooden roofs show us how Doha looked in the past. You can smell spices and perfume everywhere you go.",
           "There are many things to do there. Visitors can shop for traditional clothes and souvenirs, watch the falcons in the Falcon Souq, and enjoy delicious Qatari food in the restaurants.",
           "I strongly recommend Souq Waqif to everyone, especially visitors to Qatar. It is the perfect place to discover Qatari culture and have a great time with family and friends."]
L29 = hlines(29, (10, 20, 600, 800)); L30 = hlines(30, (10, 20, 600, 800))
def paras(L, ps, start):
    out = []; i = start
    for p in ps:
        if p == '': i += 0; continue
        for ln in textwrap.wrap(p, 70):
            if i >= len(L): break
            out.append(T(L[i][0] + 6, None, L[i][2] - 5, ln, 13.5)); i += 1
    return out
Z(29, 'Model email – Topic A', paras(L29, EMAIL, 1), 'Model formal email (Topic A) written on page 29', flag='model answer for students to compare with — not the only correct answer')
Z(30, 'Model article – Topic B', paras(L30, ARTICLE, 1), 'Model article (Topic B) written on page 30', flag='model answer for students to compare with — not the only correct answer')
Z(28, 'Topic A → model on page 29', [T(390, None, 160, 'Model email: page 29 →', 15)], 'see page 29', extra=[50, 140, 560, 410])
Z(28, 'Topic B → model on page 30', [T(390, None, 450, 'Model article: page 30 →', 15)], 'see page 30', extra=[50, 440, 560, 690])

out = {str(k): v for k, v in sorted(ZONES.items())}
json.dump(out, open('/home/claude/g10book/data.json', 'w'), ensure_ascii=False)
print({k: len(v) for k, v in out.items()}, sum(len(v) for v in out.values()), 'zones', '| L29', len(L29), 'L30', len(L30), 'L7', len(L7), 'L4', len(left), len(right), 'L25', len(L25), 'L27', len(L27))
