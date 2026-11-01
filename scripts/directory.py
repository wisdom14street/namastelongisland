# Executed inside build.py (shares its globals: page, E, BASE, EMAIL, news_box, pages, CHECKED, ROOT, json, re-use helpers)
import re as _re
DATA = json.load(open(os.path.join(ROOT, 'data', 'listings.json')))
CATS_META = [
    # key, plural title, section, schema type, icon
    ('restaurants', 'Restaurants', 'eat', 'Restaurant', 'plate'),
    ('sweets', 'Sweets and mithai', 'eat', 'FoodEstablishment', 'sweet'),
    ('catering', 'Caterers', 'weddings', 'FoodEstablishment', 'plate'),
    ('grocery', 'Groceries and halal markets', 'shop', 'GroceryStore', 'basket'),
    ('clothing', 'Clothing and boutiques', 'shop', 'ClothingStore', 'hanger'),
    ('jewelry', 'Jewelers', 'shop', 'JewelryStore', 'gem'),
    ('salons', 'Salons and threading', 'shop', 'BeautySalon', 'brush'),
    ('travel', 'Travel agents', 'shop', 'TravelAgency', 'plane'),
    ('temples', 'Hindu and Jain temples', 'community', 'HinduTemple', 'diya'),
    ('gurdwaras', 'Gurdwaras', 'community', 'PlaceOfWorship', 'dome'),
    ('mosques', 'Mosques and Islamic centers', 'community', 'Mosque', 'dome'),
    ('community', 'Community and cultural organizations', 'community', 'Organization', 'people'),
    ('dance-music', 'Dance and music schools', 'community', 'EducationalOrganization', 'note'),
    ('venues', 'Venues and banquet halls', 'weddings', 'EventVenue', 'rings'),
    ('decor', 'Decor and mandap', 'weddings', 'LocalBusiness', 'flower'),
    ('mehndi', 'Mehndi artists', 'weddings', 'LocalBusiness', 'hand'),
    ('dj-dhol', 'DJs, dhol and music', 'weddings', 'LocalBusiness', 'note'),
    ('photo-video', 'Photographers and videographers', 'weddings', 'LocalBusiness', 'camera'),
    ('makeup', 'Bridal hair and makeup', 'weddings', 'BeautySalon', 'brush'),
    ('priests', 'Pandits and officiants', 'weddings', 'LocalBusiness', 'diya'),
    ('invitations', 'Invitations and printing', 'weddings', 'LocalBusiness', 'card'),
    ('planners', 'Planners', 'weddings', 'LocalBusiness', 'rings'),
]
CM = {c[0]: c for c in CATS_META}
ICON = {
 'plate': '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/>',
 'sweet': '<circle cx="8" cy="14" r="4"/><circle cx="16" cy="14" r="4"/><circle cx="12" cy="8" r="4"/>',
 'basket': '<path d="M3 10h18l-2 9H5z"/><path d="M8 10l4-6 4 6"/>',
 'hanger': '<path d="M12 6a2 2 0 1 1 2 2c-1 0-2 1-2 2v1L3 18h18l-9-7"/>',
 'gem': '<path d="M6 4h12l4 6-10 11L2 10z"/><path d="M2 10h20"/>',
 'plane': '<path d="M2 14l20-8-6 14-4-6z"/>',
 'diya': '<path d="M12 3c2 3 3 5 3 7a3 3 0 0 1-6 0c0-2 1-4 3-7z"/><path d="M3 14h18c-1 4-5 7-9 7s-8-3-9-7z"/>',
 'dome': '<path d="M5 20V12a7 7 0 0 1 14 0v8z"/><path d="M12 2v3"/><path d="M3 20h18"/>',
 'people': '<circle cx="8" cy="8" r="3"/><circle cx="16" cy="8" r="3"/><path d="M2 20c0-4 3-6 6-6s6 2 6 6"/><path d="M12 20c0-4 2-6 4-6s6 2 6 6"/>',
 'note': '<path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/>',
 'rings': '<circle cx="9" cy="14" r="6"/><circle cx="15" cy="14" r="6"/>',
 'flower': '<circle cx="12" cy="12" r="3"/><circle cx="12" cy="5" r="3"/><circle cx="12" cy="19" r="3"/><circle cx="5" cy="12" r="3"/><circle cx="19" cy="12" r="3"/>',
 'hand': '<path d="M7 21v-9l-2-3V5h2v4h1V3h2v6h1V2h2v7h1V4h2v9l-2 8z"/>',
 'camera': '<rect x="3" y="7" width="18" height="13" rx="2"/><circle cx="12" cy="13" r="4"/><path d="M8 7l2-3h4l2 3"/>',
 'brush': '<path d="M14 3l7 7-8 8-7-7z"/><path d="M6 11l-3 10 10-3"/>',
 'card': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
}
def icon(cat):
    k = CM[cat][4]
    return f'<span class="ico ico-{CM[cat][2]}" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round">{ICON[k]}</svg></span>'
def slugify(s): return _re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
def fmt_phone(p):
    d = _re.sub(r'\D', '', p or '')
    if len(d) == 11 and d[0] == '1': d = d[1:]
    return f'({d[:3]}) {d[3:6]}-{d[6:]}' if len(d) == 10 else ''
for L in DATA:
    L['slug'] = L.get('slug') or slugify(L['name'] + '-' + (L['town'] or 'long-island'))
    L['phone_fmt'] = fmt_phone(L.get('phone'))
by_cat = {}
for L in DATA: by_cat.setdefault(L['cat'], []).append(L)
for v in by_cat.values(): v.sort(key=lambda x: (x['town'], x['name'].lower()))
by_town = {}
for L in DATA:
    if L.get('zip'): by_town.setdefault(L['town'], []).append(L)
CAT_PAGE = {c for c, v in by_cat.items() if len(v) >= 3}
TOWN_PAGE = {t for t, v in by_town.items() if len(v) >= 3}
def cat_url(c): return f'/directory/{c}/' if c in CAT_PAGE else f'/directory/#cat-{c}'
def town_url(t): return f'/towns/{slugify(t)}/' if t in TOWN_PAGE else ''
def L_card(L, show_cat=True, anchor=True):
    tel = _re.sub(r'\D', '', L.get('phone') or '')
    links = []
    if L['phone_fmt']: links.append(f'<a href="tel:+1{tel[-10:]}">{L["phone_fmt"]}</a>')
    if L.get('website'): links.append(f'<a href="{E(L["website"])}" rel="noopener nofollow" target="_blank">Website</a>')
    if L.get('address'): links.append(f'<a href="https://www.google.com/maps/search/?api=1&query={E(L["name"] + ", " + L["address"])}" rel="noopener" target="_blank">Directions</a>')
    tl = town_url(L['town'])
    town = f'<a href="{tl}">{E(L["town"])}</a>' if tl else E(L['town'])
    cat = f'<a class="tag" href="{cat_url(L["cat"])}">{E(L["type"])}</a>' if show_cat else f'<span class="tag">{E(L["type"])}</span>'
    tmp = '<p class="warn">Listed as temporarily closed. Check before visiting.</p>' if L.get('temp_closed') else ''
    return (f'<article class="card lst" id="{L["slug"]}" data-cat="{L["cat"]}" data-town="{E(L["town"])}" data-q="{E((L["name"] + " " + L["type"] + " " + L["town"] + " " + L["address"]).lower())}">'
            f'<div class="lh">{icon(L["cat"])}<div><h3>{E(L["name"])}</h3>{cat}</div></div>'
            f'<p class="desc">{E(L["desc"])}</p><p class="addr">{(E(L["address"]) + " · " + town) if L.get("address") else "Serves Long Island"}</p><p class="links">{" · ".join(links)}</p>{tmp}'
            f'<p class="lfoot"><a href="/claim/?listing={L["slug"]}">Claim this listing</a> · <a href="/report-update/?listing={L["slug"]}">Report an update</a></p></article>')
def L_schema(L):
    d = {"@type": CM[L['cat']][3], "name": L['name']}
    if L.get('address'): d['address'] = {"@type": "PostalAddress", "streetAddress": L['address'].split(',')[0], "addressLocality": L['town'], "addressRegion": "NY", "postalCode": L['zip'], "addressCountry": "US"}
    else: d['areaServed'] = 'Long Island, NY'
    if L['phone_fmt']: d['telephone'] = '+1-' + L['phone_fmt'].replace('(', '').replace(') ', '-')
    if L.get('website'): d['url'] = L['website']
    if L['cat'] in ('restaurants',) and L.get('cuisine'): d['servesCuisine'] = L['cuisine']
    return d
def itemlist_ld(items, name):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "ItemList", "name": name,
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": L_schema(L)} for i, L in enumerate(items)]}) + '</script>'
OSM_NOTE = ''
FOOTNOTE = (f'<p class="small srcnote">Every listing was checked on {CHECKED} against the business\'s Google Maps listing and, where it has one, its own website. '
            'We don\'t copy reviews, ratings, descriptions or photos. Details change: please confirm before you go, and owners can '
            '<a href="/claim/">claim a listing</a> or <a href="/report-update/">report an update</a>. '
            'Some leads came from <a href="https://www.openstreetmap.org/copyright" rel="noopener">OpenStreetMap</a> (© OpenStreetMap contributors, ODbL).</p>')
SEARCH = ('<div class="dsearch"><label class="sr" for="dq">Search the directory</label><input id="dq" type="search" placeholder="Search by name, food, town..." autocomplete="off">'
          '<select id="dt" aria-label="Filter by town"><option value="">All towns</option>{towns}</select><p class="small" id="dcount" role="status"></p></div>')
def town_opts(items):
    ts = sorted({L['town'] for L in items if L.get('zip')})
    return ''.join(f'<option>{E(t)}</option>' for t in ts)

# ---- directory hub ----
total = len(DATA)
chips = ''.join(f'<button type="button" class="chip" data-f="{c}">{E(CM[c][1])} <b>{len(by_cat[c])}</b></button>' for c, *_ in CATS_META if c in by_cat)
sections = ''
for c, title, *_ in CATS_META:
    if c not in by_cat: continue
    more = f' <a class="small" href="/directory/{c}/">Category page</a>' if c in CAT_PAGE else ''
    sections += f'<section class="dsec" id="cat-{c}" data-sec="{c}"><h2>{E(title)} <span class="cnt">{len(by_cat[c])}</span>{more}</h2><div class="grid">' + ''.join(L_card(L, show_cat=False) for L in by_cat[c]) + '</div></section>'
dir_body = f'''<section class="phead"><div class="wrap"><p class="kicker">Directory</p><h1>The Long Island South Asian directory</h1>
<p class="lede">{total} restaurants, shops, temples, gurdwaras, mosques, schools and wedding vendors across Nassau and Suffolk, each checked against a public source.</p>
<div class="btns"><a class="btn" href="/get-listed/">Add a business free</a><a class="btn alt" href="/towns/">Browse by town</a></div></div></section>
<section class="wrap">{SEARCH.format(towns=town_opts(DATA))}<div class="chips"><button type="button" class="chip on" data-f="">All <b>{total}</b></button>{chips}</div>
{sections}<p class="none" id="dnone" hidden>No matches. Try a different word, or <a href="/get-listed/">tell us who we're missing</a>.</p>{FOOTNOTE}</section>{news_box('directory')}'''
pages['/directory/'] = ('Long Island South Asian business directory | Namaste Long Island',
    f'Search {total} South Asian restaurants, sweet shops, grocers, boutiques, jewelers, temples, gurdwaras, mosques, dance schools and wedding vendors on Long Island.', dir_body)

# ---- category pages ----
CAT_INTRO = {
 'restaurants': 'Indian, Pakistani, Bangladeshi, Nepali, Sri Lankan, Afghan and Indo-Caribbean kitchens across Nassau and Suffolk, from dosa houses to biryani spots.',
 'sweets': 'Mithai shops and sweet counters for Diwali boxes, Eid platters, weddings and everyday chai-time snacks.',
 'grocery': 'Desi supermarkets and halal markets for dal, atta, spices, fresh produce, frozen parathas and meat.',
 'clothing': 'Boutiques for sarees, lehengas, salwar suits, kurtas and sherwanis, many with tailoring and alterations.',
 'jewelry': 'Jewelers for gold, bridal sets and South Asian styles.',
 'temples': 'Hindu and Jain mandirs on Long Island. Check each temple\'s own site for darshan hours and festival programs.',
 'gurdwaras': 'Sikh gurdwaras on Long Island, open to everyone for kirtan and langar.',
 'mosques': 'Mosques and Islamic centers on Long Island. Check each one\'s own site for prayer and Jumu\'ah times.',
 'community': 'Cultural associations and community organizations serving Long Island\'s South Asian families.',
 'dance-music': 'Schools teaching Bharatanatyam, Kathak, Bollywood, bhangra, and Indian vocal and instrumental music.',
 'venues': 'Halls and venues that host South Asian weddings and community events.',
 'catering': 'Caterers for pujas, parties and weddings.',
 'salons': 'Beauty salons offering eyebrow threading, facials and bridal styling.',
}
for c in CAT_PAGE:
    items = by_cat[c]; title = CM[c][1]
    intro = CAT_INTRO.get(c, f'{title} serving South Asian weddings and families on Long Island.')
    towns = sorted({L['town'] for L in items if L.get('zip')}) or ['Long Island']
    body = f'''<section class="phead"><div class="wrap"><p class="kicker"><a href="/directory/">Directory</a></p><h1>{E(title)} on Long Island</h1>
<p class="lede">{E(intro)} {len(items)} listed in {len(towns)} towns.</p>
<div class="btns"><a class="btn" href="/get-listed/?category={c}">Add yours free</a></div></div></section>
<section class="wrap">{SEARCH.format(towns=town_opts(items))}<div class="grid">{''.join(L_card(L, show_cat=True) for L in items)}</div><p class="none" id="dnone" hidden>No matches.</p>{FOOTNOTE}</section>{news_box(c)}'''
    pages[f'/directory/{c}/'] = (f'{title} on Long Island, NY | Namaste Long Island',
        f'{len(items)} South Asian {title.lower()} on Long Island, in {", ".join(towns[:6])}{" and more" if len(towns) > 6 else ""}. Addresses, phone numbers and websites, checked {CHECKED}.',
        body, itemlist_ld(items, f'{title} on Long Island'))

# ---- town pages ----
NEAR = {}
town_list = sorted(TOWN_PAGE, key=lambda t: -len(by_town[t]))
for t in TOWN_PAGE:
    items = sorted(by_town[t], key=lambda x: ([c[0] for c in CATS_META].index(x['cat']), x['name'].lower()))
    cats = {}
    for L in items: cats.setdefault(L['cat'], []).append(L)
    county = items[0]['county']
    secs = ''.join(f'<h2>{E(CM[c][1])} <span class="cnt">{len(v)}</span></h2><div class="grid">' + ''.join(L_card(L, show_cat=False) for L in v) + '</div>' for c, v in sorted(cats.items(), key=lambda kv: [x[0] for x in CATS_META].index(kv[0])))
    summary = ', '.join(f'{len(v)} {CM[c][1].lower()}' for c, v in sorted(cats.items(), key=lambda kv: -len(kv[1]))[:4])
    body = f'''<section class="phead"><div class="wrap"><p class="kicker"><a href="/towns/">Towns</a> · {E(county)} County</p><h1>South Asian {E(t)}</h1>
<p class="lede">{len(items)} listings in {E(t)}: {E(summary)}.</p></div></section>
<section class="wrap">{secs}{FOOTNOTE}</section>{news_box('town')}'''
    pages[f'/towns/{slugify(t)}/'] = (f'South Asian businesses and temples in {t}, NY | Namaste Long Island',
        f'{len(items)} South Asian listings in {t}, {county} County: {summary}. Checked {CHECKED}.', body)
tl = ''.join(f'<a class="townchip" href="/towns/{slugify(t)}/">{E(t)} <b>{len(by_town[t])}</b></a>' for t in sorted(TOWN_PAGE))
small = sorted(t for t in by_town if t not in TOWN_PAGE)
pages['/towns/'] = ('Browse by town | Namaste Long Island', 'South Asian restaurants, shops, temples and services by Long Island town.',
    f'''<section class="phead"><div class="wrap"><p class="kicker">Towns</p><h1>Browse by town</h1><p class="lede">Towns with at least three listings have their own page. Everywhere else is in the <a href="/directory/">full directory</a>.</p></div></section>
<section class="wrap"><div class="towns">{tl}</div><p class="small">Also listed: {E(", ".join(small))}.</p></section>''')

# ---- section hubs (replace placeholder-only versions) ----
def hub(section, h1, lede, extra=''):
    cs = [c for c in CATS_META if c[2] == section and c[0] in by_cat]
    cards = ''
    for c, title, *_ in cs:
        items = by_cat[c]
        preview = ''.join(f'<li><a href="{cat_url(c) if c in CAT_PAGE else "/directory/"}#{L["slug"]}">{E(L["name"])}</a> <span class="small">{E(L["town"])}</span></li>' for L in items[:6])
        cards += (f'<article class="card cat"><div class="lh">{icon(c)}<h2>{E(title)} <span class="cnt">{len(items)}</span></h2></div><ul class="plist">{preview}</ul>'
                  f'<a class="btn sm" href="{cat_url(c)}">See all {len(items)}</a></article>')
    return f'''<section class="phead"><div class="wrap"><p class="kicker">{E(section.title())}</p><h1>{h1}</h1><p class="lede">{lede}</p>
<div class="btns"><a class="btn" href="/get-listed/">Get listed free</a><a class="btn alt" href="/directory/">Search the directory</a></div></div></section>
<section class="wrap"><div class="cats">{cards}</div>{extra}</section>{news_box(section)}'''
WED_EMPTY = [(k, t) for k, t, d in WED if {'venues': 'venues', 'catering': 'catering', 'decor': 'decor', 'dj': 'dj-dhol', 'photo': 'photo-video', 'mehndi': 'mehndi', 'makeup': 'makeup', 'attire': 'clothing', 'jewelry': 'jewelry', 'priests': 'priests', 'cards': 'invitations', 'planners': 'planners'}[k] not in by_cat]
wed_extra = ('<div class="note soft"><b>Still open for first listings:</b> ' + ', '.join(E(t.lower()) for k, t in WED_EMPTY) + '. <a href="/get-listed/?category=wedding">Add your business</a>.</div>' if WED_EMPTY else '')
wed_extra += '<p class="small">Wedding shopping: see <a href="' + cat_url('clothing') + '">clothing and boutiques</a> and <a href="' + cat_url('jewelry') + '">jewelers</a>. Featured placements are coming soon; basic listings stay free.</p>'
pages['/weddings/'] = (pages['/weddings/'][0], pages['/weddings/'][1], hub('weddings', 'Long Island South Asian wedding vendors', 'Venues, caterers, decorators, mehndi artists, DJs and dhol players, photographers, makeup artists and pandits for mehndi, sangeet, the ceremony and the reception.', wed_extra))
pages['/eat/'] = (pages['/eat/'][0], pages['/eat/'][1], hub('eat', 'Where to eat South Asian on Long Island', 'Restaurants and sweet shops from Hicksville\'s South Broadway to Hillside Avenue and out east.'))
pages['/shop/'] = (pages['/shop/'][0], pages['/shop/'][1], hub('shop', 'South Asian shopping on Long Island', 'Groceries, sarees and lehengas, jewelry and travel.',
    '<p class="small">Full disclosure: our operator also runs Namaste Bookshop at 2 W 14th St in Manhattan, which sells incense, diyas and Ganesh and Lakshmi statues.</p>'))
pages['/temples-community/'] = (pages['/temples-community/'][0], pages['/temples-community/'][1], hub('community', 'Temples, gurdwaras, mosques and community groups', 'Places of worship, cultural associations and dance and music schools across Long Island.'))

# ---- report an update ----
ru_fields = (field('listing', 'Listing name or link', req=True) + field('what', 'What should change?', req=True, opts=['Phone or website', 'Address or hours', 'Permanently closed', 'Wrong category', 'Remove my listing', 'Something else']) +
             field('details', 'Details', area=True, req=True) + field('contact_name', 'Your name') + field('email', 'Your email', 'email', True) +
             field('relationship', 'Your connection', opts=['Owner or staff', 'Customer or visitor', 'Other']))
pages['/report-update/'] = ('Report an update | Namaste Long Island', 'Tell us about a change or mistake in a Namaste Long Island listing.',
    f'''<section class="phead"><div class="wrap"><p class="kicker">Report an update</p><h1>Report an update</h1><p class="lede">Moved, closed, new number, or something we got wrong? Tell us and we'll check it.</p></div></section>
<section class="wrap narrow">{form('report_update', 'Listing update', ru_fields, 'Send update')}<p class="small">Owners: <a href="/claim/">claim your listing</a> to manage it directly.</p></section>''')
