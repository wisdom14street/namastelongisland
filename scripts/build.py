#!/usr/bin/env python3
"""Builds namastelongisland.com into dist/. Static, GitHub Pages. Run: python3 scripts/build.py"""
import json, os, html, datetime, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, 'dist')
DOMAIN = 'namastelongisland.com'
BASE = f'https://{DOMAIN}'
BRAND = 'Namaste Long Island'
OPERATOR = 'Wealth Edge Ventures Inc.'
EMAIL = 'sahwisdom@gmail.com'
FORM_ENDPOINT = f'https://formsubmit.co/ajax/{EMAIL}'
GA_ID = 'G-Y7R5K9NMW0'
VER = datetime.date.today().isoformat()
CHECKED = 'November 1, 2026'
E = html.escape

GA_HEAD = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>'
           f'<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());'
           f'gtag("config","{GA_ID}",' + json.dumps({'site_brand': BRAND}) + ');</script>')

NAV = [('/directory/', 'Directory'), ('/weddings/', 'Weddings'), ('/events/', 'Events'), ('/festivals/', 'Festivals'), ('/eat/', 'Eat'),
       ('/shop/', 'Shop'), ('/temples-community/', 'Temples & community')]

DIYA = ('<svg class="diya" viewBox="0 0 64 64" aria-hidden="true"><path d="M32 6c5 8 8 13 8 18a8 8 0 0 1-16 0c0-5 3-10 8-18z" fill="#F2A007"/>'
        '<path d="M32 14c2.6 4.2 4 7 4 9.6a4 4 0 0 1-8 0c0-2.6 1.4-5.4 4-9.6z" fill="#FFE08A"/>'
        '<path d="M6 36h52c-2 12-12 20-26 20S8 48 6 36z" fill="#C2185B"/><path d="M14 40h36" stroke="#F2A007" stroke-width="3" stroke-linecap="round"/></svg>')

TORAN = ('<div class="toran" aria-hidden="true"><svg viewBox="0 0 1200 34" preserveAspectRatio="none">'
         + ''.join(f'<path d="M{x} 0 l20 0 l-10 {22 if i % 2 else 30}z" fill="{["#F2A007", "#2E7D32", "#E8630A", "#2E7D32"][i % 4]}"/>' for i, x in enumerate(range(0, 1200, 24)))
         + '</svg></div>')

ORG_LD = {
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "Organization", "@id": f"{BASE}/#org", "name": BRAND, "url": f"{BASE}/", "logo": f"{BASE}/icon.svg",
         "email": EMAIL, "areaServed": "Long Island, New York",
         "parentOrganization": {"@type": "Organization", "name": OPERATOR}},
        {"@type": "WebSite", "@id": f"{BASE}/#site", "url": f"{BASE}/", "name": BRAND, "publisher": {"@id": f"{BASE}/#org"}, "inLanguage": "en-US"},
    ]}

def page(path, title, desc, body, extra_head=''):
    canon = BASE + path
    nav = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if path.startswith(h) else ""}>{E(t)}</a>' for h, t in NAV)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{canon}">
<meta name="theme-color" content="#C2185B"><link rel="icon" href="/icon.svg" type="image/svg+xml">
<meta property="og:type" content="website"><meta property="og:site_name" content="{BRAND}"><meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{BASE}/og.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Yeseva+One&family=Mulish:wght@400;600;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v={VER}">
<script type="application/ld+json">{json.dumps(ORG_LD)}</script>
{extra_head}{GA_HEAD}</head>
<body>{TORAN}
<header class="top"><div class="wrap bar"><a class="brand" href="/">{DIYA}<span>Namaste<b>Long Island</b></span></a>
<a class="pill" href="/get-listed/">Get listed free</a></div>
<nav class="nav wrap" aria-label="Sections">{nav}</nav></header>
<main id="main">{body}</main>
<footer class="foot"><div class="wrap">
<div class="fcols"><div><p class="fbrand">{DIYA}<span>Namaste Long Island</span></p>
<p>A community guide to South Asian life on Long Island: weddings, festivals, food, worship and the people behind them.</p></div>
<div><p class="fh">Explore</p>{''.join(f'<a href="{h}">{E(t)}</a>' for h, t in NAV)}</div>
<div><p class="fh">Take part</p><a href="/get-listed/">Get listed</a><a href="/claim/">Claim your listing</a><a href="/submit-event/">Submit an event</a><a href="/newsletter/">Newsletter</a><a href="/about/">About</a><a href="/privacy/">Privacy</a></div></div>
<p class="op">Namaste Long Island is run by {OPERATOR} (also behind Namaste Bookshop in NYC). Questions or corrections: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
</div></footer>
<script>window.NLI={{endpoint:{json.dumps(FORM_ENDPOINT)},email:{json.dumps(EMAIL)}}};</script>
<script src="/assets/site.js?v={VER}" defer></script>
</body></html>'''

def cta_band(h, p, links):
    return f'<section class="band"><div class="wrap"><h2>{h}</h2><p>{p}</p><div class="btns">' + ''.join(
        f'<a class="btn{" alt" if i else ""}" href="{u}">{E(t)}</a>' for i, (u, t) in enumerate(links)) + '</div></div></section>'

def news_box(src):
    return f'''<section class="news"><div class="wrap"><h2>One email a week. Everything worth showing up for.</h2>
<p>Garba nights, temple festivals, new restaurants and wedding-season finds across Long Island, in one short weekly note.</p>
<div class="form inline" data-form="newsletter" data-subject="Newsletter signup">
<input type="hidden" name="source" value="{src}"><label class="sr" for="nl-{src}">Email</label>
<input id="nl-{src}" name="email" type="email" required autocomplete="email" placeholder="you@example.com">
<input name="_honey" type="text" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
<button type="button" class="btn send">Sign me up</button><p class="msg" role="status"></p></div>
<p class="fine">We use your email only for the newsletter. Unsubscribe any time by replying "stop".</p></div></section>'''

# ---------- Verified data (checked on the organizer's or venue's own page) ----------
EVENTS = [
    dict(date='2026-11-08', when='Sun, Nov 8, 2026 · 7:00 pm onward', name='Diwali and Chopda Pujan',
         where='BAPS Shri Swaminarayan Mandir, 2 Deshon Drive, Melville',
         what='Diwali evening at the mandir, with the Chopda Pujan blessing of new account books.',
         src='https://www.baps.org/Global-Network/North-America/LongIsland/Upcoming-Events.aspx', srcname='baps.org'),
    dict(date='2026-11-09', when='Mon, Nov 9, 2026 · 6:30–8:30 pm', name='Community Diwali dinner (Meetup group)',
         where='Bikanervala, 594 S Broadway, Hicksville',
         what='A Diwali dinner gathering posted by the "Hang Out in Queens and Nassau" Meetup group. RSVP on Meetup.',
         src='https://www.meetup.com/hangoutinqueensandnassau/events/317177036/', srcname='meetup.com'),
    dict(date='2026-11-10', when='Tue, Nov 10, 2026 · 10:30 am–7:00 pm', name='Annakut Darshan',
         where='BAPS Shri Swaminarayan Mandir, 2 Deshon Drive, Melville',
         what='Darshan of the Annakut offering for the Hindu New Year (Govardhan Puja).',
         src='https://www.baps.org/Global-Network/North-America/LongIsland/Upcoming-Events.aspx', srcname='baps.org'),
    dict(date='2026-11-15', when='Sun, Nov 15, 2026 · 5:00–10:00 pm', name='RANA 27th Diwali Gala',
         where='Crest Hollow Country Club, 8325 Jericho Turnpike, Woodbury',
         what='The organizer\'s annual Diwali gala. Tickets are listed at $150 on the organizer\'s page.',
         src='https://www.ranausa.org/event/', srcname='ranausa.org'),
    dict(date='2026-11-09b', when='Mondays, Nov 9, 16, 23 and 30, 2026 · 7:00–8:00 pm', name='Bollywood Dance Class (4 weeks)',
         where='Hicksville Public Library, Hicksville',
         what='A beginner Bollywood dance series for adults (18+). Registration is required and covers all four classes.',
         src='https://hicksvillelibrary.libcal.com/event/17149045', srcname='hicksvillelibrary.libcal.com'),
    dict(date='2026-11-21', when='Sat, Nov 21, 2026 · 8:00 pm', name='Udit Narayan & Aditya Narayan in concert',
         where='Tilles Center for the Performing Arts, 720 Northern Blvd, Brookville',
         what='The playback singers perform in the Concert Hall. Tickets through Tilles Center.',
         src='https://www.tillescenter.org/event/udit-narayan-aditya-narayan', srcname='tillescenter.org'),
    dict(date='2026-11-22', when='Sun, Nov 22, 2026 · 7:45 am–3:00 pm', name='AAPIQLI Annual CME and Research Competition',
         where='DeMatteis Center, 101 Northern Blvd, Greenvale',
         what='Continuing medical education and a research competition from the American Association of Physicians of Indian Origin, Queens and Long Island chapter.',
         src='https://aapiqli.org/events/', srcname='aapiqli.org'),
    dict(date='2026-12-12', when='Sat, Dec 12, 2026 · 5:00–7:00 pm', name="Pramukh Swami Maharaj's Janma Jayanti",
         where='BAPS Shri Swaminarayan Mandir, 2 Deshon Drive, Melville',
         what='A celebration of the birth anniversary of Pramukh Swami Maharaj.',
         src='https://www.baps.org/Global-Network/North-America/LongIsland/Upcoming-Events.aspx', srcname='baps.org'),
    dict(date='2026-12-19', when='Sat, Dec 19, 2026 · 5:00–7:00 pm', name="Pramukh Swami Maharaj's Birthday: Mahila Celebration",
         where='BAPS Shri Swaminarayan Mandir, 2 Deshon Drive, Melville',
         what='A celebration organized by women, for women.',
         src='https://www.baps.org/Global-Network/North-America/LongIsland/Upcoming-Events.aspx', srcname='baps.org'),
    dict(date='2026-11-01', when='Sun, Nov 1, 2026 · 7:00 pm', name='Sufi Sham with Hans Raj Hans',
         where='Pearl Banquet Hall, 276 W Old Country Road, Hicksville',
         what='An evening of Punjabi folk and Sufi songs from the Padma Shri singer, billed by the organizer as his last New York show. Tables from $150.',
         src='https://www.desieventsonline.com/events/eventdisplay.asp?id=427969', srcname='desieventsonline.com'),
    dict(date='2026-11-04', when='Wed, Nov 4, 2026 · all day', name='CultureCrafts: Diwali drop-in',
         where='Hampton Bays Public Library, 52 Ponquogue Ave, Hampton Bays',
         what='A small Diwali craft and an information table about the festival in the library\'s Teen Room. Drop in any time.',
         src='https://hamptonbays.librarycalendar.com/event/culturecrafts-diwali-drop-50098', srcname='hamptonbays.librarycalendar.com'),
    dict(date='2026-11-06', when='Fri, Nov 6, 2026 · 4:00–5:00 pm', name='Craft-Along: Diwali',
         where='Henry Waldinger Memorial Library, 60 Verona Place, Valley Stream',
         what='Stories and a Diwali craft for kids in grades K to 6. Registration required, 17 spots.',
         src='https://valleystreamlibrary.assabetinteractive.com/calendar/craft-along-diwali-2/', srcname='valleystreamlibrary.org'),
    dict(date='2026-11-07', when='Sat, Nov 7, 2026 · 10:00 am–12:00 pm', name='Drop-in Diwali craft',
         where='Mineola Memorial Library, 195 Marcellus Road, Mineola',
         what='A free Diwali craft in the Children\'s Library for kids and teens. No sign-up; supplies while they last.',
         src='https://mineola.librarycalendar.com/events/month/2026/11', srcname='mineola.librarycalendar.com'),
    dict(date='2026-11-15b', when='Sun, Nov 15, 2026 · 7:30 pm (doors 6:30)', name='Ragaboyz: Generations Live',
         where='The Space at Westbury, 250 Post Ave, Westbury',
         what='A Hindi, Urdu and Punjabi music show from Sapphire Entertainment. Tickets from $65.',
         src='https://events.sulekha.com/ragaboyz-generations-live-in-new-york_event-in_westbury-ny_401984', srcname='events.sulekha.com'),
]
EVENTS.sort(key=lambda e: e['date'])

PLACES = [
    dict(kind='Mandir', name='BAPS Shri Swaminarayan Mandir, Long Island', addr='2 Deshon Drive, Melville, NY 11747', tel='(631) 996-9237',
         note='Check the mandir\'s page for darshan times and festival programs.',
         src='https://www.baps.org/Global-Network/North-America/LongIsland.aspx', srcname='baps.org'),
    dict(kind='Mandir', name='Hindu Temple of Long Island', addr='729 S Oyster Bay Road, Bethpage, NY 11714', tel='516-342-6333',
         note='Mon–Fri 9 am–12 pm and 4–8 pm; Sat and Sun 9 am–8 pm.',
         src='https://hindutempleoflongisland.com/', srcname='hindutempleoflongisland.com'),
    dict(kind='Mandir', name='Shri Navagraha Devasthanam of North America', addr='1616 Hillside Avenue, New Hyde Park, NY 11040', tel='718-740-9400',
         note='Check the temple\'s website for timings and pooja services.', src='https://www.navagrahausa.com/contactus', srcname='navagrahausa.com'),
    dict(kind='Gurdwara', name='Gurudwara Shaheedan', addr='18 W Nicholai Street, Hicksville, NY 11801', tel='917-353-7265',
         note='Check the gurdwara\'s website for the program schedule.', src='https://shaheedan.us', srcname='shaheedan.us'),
]

GROCERY = [
    dict(name='Patel Brothers Hicksville', addr='415 South Broadway, Hicksville, NY 11801', tel='516-681-0091', note='Listed hours: Monday to Sunday 9 am–8:30 pm (holiday hours may vary).',
         src='https://www.patelbros.com/locations', srcname='patelbros.com'),
    dict(name='Patel Brothers Bellerose (Queens border)', addr='251-08 Hillside Avenue, Bellerose, NY 11426', tel='718-470-1356', note='Just over the Nassau line from Floral Park and New Hyde Park.',
         src='https://www.patelbros.com/locations', srcname='patelbros.com'),
]

def place_card(p):
    kind = f'<span class="tag">{E(p["kind"])}</span>' if p.get('kind') else ''
    tel = ''.join(c for c in p['tel'] if c.isdigit())
    return (f'<article class="card place">{kind}<h3>{E(p["name"])}</h3><p class="addr">{E(p["addr"])}</p>'
            f'<p class="links"><a href="tel:+1{tel}">{E(p["tel"])}</a> · <a href="https://www.google.com/maps/search/?api=1&query={E(p["name"] + ", " + p["addr"])}" rel="noopener">Directions</a> · <a href="{p["src"]}" rel="noopener">Website</a></p>'
            f'<p class="small">{E(p["note"])}</p><p class="ver">Checked on {E(p["srcname"])}, {CHECKED}. Confirm hours before you go.</p></article>')

def event_card(e):
    return (f'<article class="card event"><p class="when">{E(e["when"])}</p><h3>{E(e["name"])}</h3><p class="addr">{E(e["where"])}</p>'
            f'<p>{E(e["what"])}</p><p class="ver">From the organizer\'s page: <a href="{e["src"]}" rel="noopener">{E(e["srcname"])}</a>. Confirm details with the organizer.</p></article>')

def upcoming():
    today = datetime.date.today().isoformat()
    return [e for e in EVENTS if e['date'] >= today]

# ---------- Pages ----------
pages = {}

ev = upcoming()
ev_html = ''.join(event_card(e) for e in ev[:4])
home_body = f'''<section class="hero"><div class="wrap">
<p class="kicker">Hicksville · New Hyde Park · Jericho · Melville · and all of Long Island</p>
<h1>Your guide to South Asian life on Long Island</h1>
<p class="lede">Weddings, festivals, food, worship and the neighbors who make it all happen. Free to use, free to be listed, and checked by a real person.</p>
<form class="hsearch" action="/directory/" method="get" role="search"><label class="sr" for="hq">Search the directory</label><input id="hq" name="q" type="search" placeholder="Try dosa, mithai, lehenga, gurdwara..."><button class="btn" type="submit">Search</button></form>
<div class="btns"><a class="btn alt" href="/directory/">Browse the directory</a><a class="btn alt" href="/get-listed/">Get listed free</a></div>
</div></section>
<section class="wrap launch"><div class="note"><b>Just launched.</b> Every listing is checked against the business's own Google Maps listing or website, with no copied reviews or photos. Missing someone, or own a listed business? <a href="/get-listed/">Add a listing</a> or <a href="/claim/">claim yours</a>.</div></section>
{f'<section class="wrap"><div class="sechead"><h2>Coming up</h2><a href="/events/">All events</a></div><div class="grid">{ev_html}</div></section>' if ev else ''}
<section class="wrap"><h2>Explore</h2><div class="tiles">
<a class="tile t3" href="/directory/"><b>Full directory</b><span>Search every listing</span></a>
<a class="tile t1" href="/weddings/"><b>Wedding vendors</b><span>Mandap to mehndi, by category</span></a>
<a class="tile t2" href="/festivals/"><b>Festival guide</b><span>Diwali, Navratri, Holi, Eid, Vaisakhi and more</span></a>
<a class="tile t3" href="/events/"><b>Events</b><span>Garba nights, pujas, galas, melas</span></a>
<a class="tile t4" href="/eat/"><b>Eat</b><span>Restaurants, mithai, chaat, catering</span></a>
<a class="tile t5" href="/shop/"><b>Shop</b><span>Groceries, sarees, jewelry, puja supplies</span></a>
<a class="tile t6" href="/temples-community/"><b>Temples & community</b><span>Mandirs, gurdwaras, associations</span></a>
</div></section>
<section class="wrap facts"><h2>Who this is for</h2>
<p>Long Island is home to about 112,000 South Asian residents, about seven in ten of them in Nassau County. Hicksville alone has about 8,700, roughly one in five people in town. The guide covers Indian, Pakistani, Bangladeshi, Sri Lankan, Nepali and Indo-Caribbean families, and everyone who loves a good festival.</p>
<p class="small">Source: U.S. Census Bureau, American Community Survey 2020–2024 5-year estimates, via <a href="https://censusreporter.org" rel="noopener">censusreporter.org</a>.</p></section>
{news_box('home')}'''
pages['/'] = ('Namaste Long Island: South Asian weddings, festivals, food and events on Long Island',
              'A community guide to South Asian life on Long Island: wedding vendors, festival guide, events, restaurants, shops, temples and gurdwaras, checked by a real person.', home_body)

WED = [
    ('venues', 'Venues and banquet halls', 'Halls, hotels and estates that can host a baraat, a 400-seat reception, and a fire-safe havan.'),
    ('catering', 'Caterers', 'Regional menus for every event: Gujarati, Punjabi, South Indian, Bengali, Pakistani, Indo-Caribbean, Jain and vegan.'),
    ('decor', 'Decor and mandap', 'Mandaps, stage design, floral garlands and marigold walls, lighting and entrances.'),
    ('dj', 'DJs, dhol and live music', 'Sangeet DJs, dhol players for the baraat, live singers and classical musicians.'),
    ('photo', 'Photographers and videographers', 'Teams who know the rituals and when not to block the pandit.'),
    ('mehndi', 'Mehndi artists', 'Bridal and guest mehndi, at home or at the venue.'),
    ('makeup', 'Bridal hair and makeup', 'Artists for long, multi-event days and draping help with sarees and dupattas.'),
    ('attire', 'Bridal and groom attire', 'Lehengas, sarees, sherwanis, alterations and rentals.'),
    ('jewelry', 'Jewelers', 'Bridal sets, gold, kundan and polki, and repairs.'),
    ('priests', 'Pandits, priests and officiants', 'Hindu, Sikh, Jain, Muslim and interfaith ceremonies.'),
    ('cards', 'Invitations and favors', 'Cards, boxes of mithai, return gifts and signage.'),
    ('planners', 'Planners and coordinators', 'Full planning or day-of help for multi-day celebrations.'),
]
wed_body = '''<section class="phead"><div class="wrap"><p class="kicker">Wedding vendors</p><h1>Long Island South Asian wedding vendors</h1>
<p class="lede">A directory of local vendors for mehndi, sangeet, haldi, the ceremony and the reception. Each category opens with its first verified vendors. Listing is free.</p>
<div class="btns"><a class="btn" href="/get-listed/?category=wedding">List your wedding business free</a><a class="btn alt" href="/claim/">Already listed? Claim it</a></div></div></section>
<section class="wrap"><div class="note">Launching now: these categories are open and waiting for their first vendors. We list only businesses we've confirmed directly, and we never copy reviews from other sites.</div>
<div class="cats">''' + ''.join(
    f'<article class="card cat" id="{k}"><h2>{E(t)}</h2><p>{E(d)}</p><p class="empty">Be one of the first {E(t.lower())} listed.</p>'
    f'<a class="btn sm" href="/get-listed/?category={k}">Get listed in this category</a></article>' for k, t, d in WED) + '''</div></section>
<section class="wrap"><div class="note soft"><b>Featured placements are coming soon.</b> Basic listings stay free. Vendors who want a featured spot can email <a href="mailto:''' + EMAIL + '''?subject=Featured%20placement">''' + EMAIL + '''</a>. Paid placements will always be labeled.</div></section>''' + news_box('weddings')
pages['/weddings/'] = ('South Asian wedding vendors on Long Island | Namaste Long Island',
                       'Find and list Long Island vendors for South Asian weddings: venues, caterers, mandap decor, DJs and dhol, photographers, mehndi, makeup, attire, jewelers and pandits.', wed_body)

ev_all = ''.join(event_card(e) for e in ev)
events_body = f'''<section class="phead"><div class="wrap"><p class="kicker">Events</p><h1>South Asian events on Long Island</h1>
<p class="lede">Pujas, galas, garba and dandiya nights, melas, concerts and community gatherings. Organizers can add events free.</p>
<div class="btns"><a class="btn" href="/submit-event/">Submit an event</a><a class="btn alt" href="/newsletter/">Get the weekly email</a></div></div></section>
<section class="wrap">{f'<h2>Coming up</h2><div class="grid">{ev_all}</div>' if ev else ''}
<div class="note soft"><b>How events get here.</b> We list events from organizers' own announcements and from the submission form, with a link back to the organizer. We don't copy news articles or other calendars. Spotted a mistake? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</div></section>{news_box('events')}'''
pages['/events/'] = ('South Asian events on Long Island: Diwali, garba, galas | Namaste Long Island',
                     'Upcoming South Asian community events on Long Island, from temple festivals to Diwali galas, each linked to the organizer. Submit your event free.', events_body)

FEST = [
    ('Diwali', 'Festival of lights, observed by Hindus, Sikhs (as Bandi Chhor Divas) and Jains. Five days of lamps, Lakshmi puja, sweets and family visits.',
     'In 2026 Diwali falls on Sunday, November 8; in 2027 on Friday, October 29.', 'https://www.timeanddate.com/holidays/india/diwali', 'timeanddate.com',
     'On Long Island: BAPS Shri Swaminarayan Mandir in Melville lists Diwali and Chopda Pujan on Nov 8, 2026 and Annakut Darshan on Nov 10.'),
    ('Navratri and Dussehra', 'Nine nights honoring the Goddess, with garba and dandiya raas, followed by Dussehra. Bengali families mark Durga Puja in the same season.',
     'Follows the lunar calendar, usually in September or October.', '', '',
     'Long Island garba nights are often held in school gyms, halls and temple grounds. Organizers: submit yours.'),
    ('Ganesh Chaturthi', 'Ten days for Lord Ganesha, ending with the visarjan (immersion).',
     'Usually late August or September.', '', '',
     'In 2026, Indo American Community Voice held its 4th Ganesh Mahotsav in Hicksville on Sept 18–20 at the Broadway Mall parking lot, as reported by The South Asian Times.'),
    ('India Day Parade, Hicksville', 'A celebration of Indian Independence Day (August 15) with floats, music and flags on South Broadway.',
     'Held in August.', '', '',
     'The 16th annual parade marched on Sunday, Aug 23, 2026, as reported by the Long Island Press.'),
    ('Holi', 'The spring festival of colors, bonfires the night before, and gulal the next day.',
     'Follows the lunar calendar, usually in March.', '', '', 'Community Holi events are posted here as organizers announce them.'),
    ('Eid al-Fitr and Eid al-Adha', 'Eid al-Fitr ends Ramadan; Eid al-Adha follows the Hajj. Prayers, new clothes, family meals and charity.',
     'Both move about 11 days earlier each year on the Gregorian calendar; dates depend on the moon.', '', '', 'Masjids and associations: submit Eid prayer times and gatherings.'),
    ('Vaisakhi', 'Harvest festival and the founding of the Khalsa, marked at gurdwaras with kirtan, langar and Nagar Kirtan processions.',
     'Usually April 13 or 14.', '', '', 'Gurdwaras: submit your Vaisakhi program and Nagar Kirtan route.'),
    ('Pohela Boishakh, Puthandu, Vishu and other new years', 'Regional new years from Bengal, Tamil Nadu, Kerala and beyond, celebrated with food, music and new clothes.',
     'Mostly mid-April.', '', '', 'Associations: tell us about your celebration.'),
    ('Phagwah and Indo-Caribbean celebrations', 'Phagwah (Holi) and Diwali are celebrated by Guyanese and Trinidadian families, with chowtal singing and mandir programs.',
     'Phagwah usually falls in March.', '', '', 'The biggest celebrations are in Richmond Hill, Queens, next door.'),
]
SRCS = {'Ganesh Chaturthi': ('https://www.thesouthasiantimes.info/new-york/news/indo-american-community-voice-inc-celebrates-resounding-success-of-4th-ganesh-mahotsav-in-hicksville/10115', 'The South Asian Times'),
        'India Day Parade, Hicksville': ('https://www.longislandpress.com/2026/08/25/hicksville-indian-community-celebrates-80-years-of-independence/', 'Long Island Press')}
fest_cards = ''
for name, what, when, wsrc, wsn, li in FEST:
    w = f'{E(when)}' + (f' <span class="small">(<a href="{wsrc}" rel="noopener">{wsn}</a>)</span>' if wsrc else '')
    s = SRCS.get(name)
    l = E(li) + (f' <span class="small">(<a href="{s[0]}" rel="noopener">{s[1]}</a>)</span>' if s else '')
    if name == 'Diwali':
        l += ' <span class="small">(<a href="https://www.baps.org/Global-Network/North-America/LongIsland/Upcoming-Events.aspx" rel="noopener">baps.org</a>)</span>'
    fest_cards += f'<article class="card fest"><h2>{E(name)}</h2><p>{E(what)}</p><p><b>When:</b> {w}</p><p><b>Locally:</b> {l}</p></article>'
fest_body = f'''<section class="phead"><div class="wrap"><p class="kicker">Festival guide</p><h1>A Long Island guide to South Asian festivals</h1>
<p class="lede">What each festival is, when it usually falls, and where Long Island celebrates it. Exact dates and local programs appear only when the organizer has published them.</p></div></section>
<section class="wrap"><div class="cats">{fest_cards}</div>
<div class="note soft">Organizing a festival event? <a href="/submit-event/">Submit it free</a> and we'll add it to the calendar and the weekly email.</div></section>{news_box('festivals')}'''
pages['/festivals/'] = ('South Asian festival guide for Long Island: Diwali, Navratri, Holi, Eid, Vaisakhi',
                        'When Diwali, Navratri, Ganesh Chaturthi, Holi, Eid, Vaisakhi and other South Asian festivals fall, and how Long Island celebrates them.', fest_body)

EAT = [('restaurants', 'Restaurants', 'North and South Indian, Pakistani, Bangladeshi, Sri Lankan, Nepali and Indo-Caribbean kitchens.'),
       ('sweets', 'Sweets and mithai', 'Mithai boxes for Diwali and weddings, and the shop that still makes jalebi fresh.'),
       ('chaat', 'Chaat and street food', 'Pani puri, vada pav, kathi rolls and samosas.'),
       ('catering', 'Party catering', 'Trays for pujas, birthdays and graduation parties.'),
       ('tiffin', 'Tiffin and home cooks', 'Licensed home-style meal services and weekly tiffin plans.')]
eat_body = '''<section class="phead"><div class="wrap"><p class="kicker">Eat</p><h1>Where to eat South Asian on Long Island</h1>
<p class="lede">Restaurants, sweet shops, chaat counters and caterers from Hicksville to Commack. Owners can list free.</p>
<div class="btns"><a class="btn" href="/get-listed/?category=restaurant">List your restaurant free</a></div></div></section>
<section class="wrap"><div class="note">Launching now. We add restaurants after confirming the details with the owner, and we never post reviews copied from other sites.</div><div class="cats">''' + ''.join(
    f'<article class="card cat" id="{k}"><h2>{E(t)}</h2><p>{E(d)}</p><p class="empty">Be one of the first listed.</p><a class="btn sm" href="/get-listed/?category={k}">Get listed</a></article>' for k, t, d in EAT) + '</div></section>' + news_box('eat')
pages['/eat/'] = ('South Asian restaurants, sweets and catering on Long Island | Namaste Long Island',
                  'Indian, Pakistani, Bangladeshi, Sri Lankan, Nepali and Indo-Caribbean restaurants, mithai shops and caterers on Long Island. Owners list free.', eat_body)

shop_body = f'''<section class="phead"><div class="wrap"><p class="kicker">Shop</p><h1>South Asian shopping on Long Island</h1>
<p class="lede">Groceries, sarees and lehengas, jewelry and puja supplies close to home.</p>
<div class="btns"><a class="btn" href="/get-listed/?category=shop">List your shop free</a></div></div></section>
<section class="wrap"><h2>Groceries</h2><div class="grid">{''.join(place_card(g) for g in GROCERY)}</div>
<div class="cats">
<article class="card cat"><h2>Sarees, lehengas and menswear</h2><p>Boutiques for festival and wedding outfits, tailoring and alterations.</p><p class="empty">Be one of the first listed.</p><a class="btn sm" href="/get-listed/?category=attire">Get listed</a></article>
<article class="card cat"><h2>Jewelry</h2><p>Gold, bridal sets, bangles and everyday pieces.</p><p class="empty">Be one of the first listed.</p><a class="btn sm" href="/get-listed/?category=jewelry">Get listed</a></article>
<article class="card cat"><h2>Puja supplies and gifts</h2><p>Diyas, murtis, incense, kumkum, thalis and return gifts.</p><p class="empty">Be one of the first listed.</p><a class="btn sm" href="/get-listed/?category=puja">Get listed</a>
<p class="small">Full disclosure: our operator also runs Namaste Bookshop at 2 W 14th St in Manhattan, which sells incense, diyas and Ganesh and Lakshmi statues.</p></article>
</div></section>{news_box('shop')}'''
pages['/shop/'] = ('South Asian groceries, sarees, jewelry and puja supplies on Long Island',
                   'Where to shop for South Asian groceries, festival and wedding clothes, jewelry and puja supplies on Long Island.', shop_body)

tc_body = f'''<section class="phead"><div class="wrap"><p class="kicker">Temples & community</p><h1>Mandirs, gurdwaras and community groups on Long Island</h1>
<p class="lede">Places of worship and associations, with details checked on each one's own website. Masjids, churches, Jain and Buddhist centers and cultural associations are welcome to add themselves.</p>
<div class="btns"><a class="btn" href="/get-listed/?category=community">Add your temple or association</a></div></div></section>
<section class="wrap"><div class="grid">{''.join(place_card(p) for p in PLACES)}</div>
<div class="note soft">This list is growing. We add a place only after checking its details at the source, so if yours is missing, it's because we haven't confirmed it yet. <a href="/get-listed/?category=community">Send us your details</a>.</div></section>{news_box('community')}'''
pages['/temples-community/'] = ('Hindu temples, gurdwaras and South Asian community groups on Long Island',
                                'Mandirs, gurdwaras and South Asian community organizations on Long Island, with addresses and hours checked on their own websites.', tc_body)

def field(name, label, typ='text', req=False, ph='', full=False, opts=None, area=False):
    r = ' required' if req else ''
    star = ' <span class="req">*</span>' if req else ''
    cls = ' class="full"' if full or area else ''
    if opts:
        o = ''.join(f'<option>{E(x)}</option>' for x in opts)
        inp = f'<select id="f-{name}" name="{name}"{r}><option value="">Choose one</option>{o}</select>'
    elif area:
        inp = f'<textarea id="f-{name}" name="{name}" rows="4"{r} placeholder="{E(ph)}"></textarea>'
    else:
        inp = f'<input id="f-{name}" name="{name}" type="{typ}"{r} placeholder="{E(ph)}">'
    return f'<div{cls}><label for="f-{name}">{E(label)}{star}</label>{inp}</div>'

CATS = ['Wedding: venue or banquet hall', 'Wedding: caterer', 'Wedding: decor and mandap', 'Wedding: DJ, dhol or music', 'Wedding: photo or video',
        'Wedding: mehndi', 'Wedding: hair and makeup', 'Wedding: attire', 'Wedding: jeweler', 'Wedding: pandit or officiant', 'Wedding: invitations and favors',
        'Wedding: planner', 'Restaurant', 'Sweets and mithai', 'Chaat and street food', 'Party catering', 'Tiffin or home cook', 'Grocery',
        'Clothing and boutique', 'Jewelry', 'Puja supplies and gifts', 'Temple, gurdwara or place of worship', 'Community association', 'Other service']
CONSENT = ('<div class="full check"><label><input type="checkbox" name="consent" value="yes" required> I run or represent this business or organization, the details are accurate, and you may publish them. Any photos I send are mine to share. <span class="req">*</span></label></div>')

def form(kind, subject, fields, button):
    return (f'<div class="form" data-form="{kind}" data-subject="{E(subject)}"><div class="fgrid">{fields}</div>'
            f'<input name="_honey" type="text" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">'
            f'<button type="button" class="btn send">{E(button)}</button><p class="msg" role="status"></p></div>')

gl_fields = (field('business', 'Business or organization name', req=True) + field('category', 'Category', req=True, opts=CATS) +
             field('town', 'Town', req=True, ph='e.g. Hicksville') + field('address', 'Street address (or "service area only")') +
             field('phone', 'Business phone', 'tel') + field('website', 'Website or Instagram', ph='https://') +
             field('contact_name', 'Your name', req=True) + field('email', 'Your email', 'email', True) +
             field('about', 'Describe your business in your own words', area=True, ph='What you offer, languages you speak, areas you serve') + CONSENT)
gl_body = f'''<section class="phead"><div class="wrap"><p class="kicker">Get listed</p><h1>Get your business listed free</h1>
<p class="lede">Wedding vendors, restaurants, shops, temples, associations and services across Long Island. Basic listings are free. We'll confirm your details with you before anything goes live.</p></div></section>
<section class="wrap narrow">{form('get_listed', 'New listing request', gl_fields, 'Send my listing')}
<div class="steps"><h2>What happens next</h2><ol><li>We read every request and reply by email, usually within a few days.</li><li>We confirm your details with you and check them against your website or Google Maps.</li><li>Your free listing goes live, and you can update it any time.</li></ol>
<p class="small">Featured placements are coming soon. Interested? Email <a href="mailto:{EMAIL}?subject=Featured%20placement">{EMAIL}</a>. Paid placements will always be labeled as such.</p>
<p class="small">Already listed? <a href="/claim/">Claim your listing</a>. Hosting an event? <a href="/submit-event/">Submit it here</a>.</p></div></section>'''
pages['/get-listed/'] = ('Get listed free | Namaste Long Island', 'Add your South Asian wedding business, restaurant, shop, temple or association to Namaste Long Island. Basic listings are free.', gl_body)

cl_fields = (field('business', 'Business name as listed', req=True) + field('listing_url', 'Link to the listing on this site', ph='https://namastelongisland.com/...') +
             field('contact_name', 'Your name', req=True) + field('role', 'Your role', req=True, ph='Owner, manager, organizer...') +
             field('email', 'Your email', 'email', True) + field('phone', 'Phone we can call to verify', 'tel', True) +
             field('changes', 'Anything to correct or add?', area=True) + CONSENT)
cl_body = f'''<section class="phead"><div class="wrap"><p class="kicker">Claim your listing</p><h1>Claim your listing</h1>
<p class="lede">Own or manage a business or organization on this site? Claim it to correct details, add photos and hours, and hear first when featured placements open.</p></div></section>
<section class="wrap narrow">{form('claim', 'Listing claim', cl_fields, 'Claim my listing')}
<div class="steps"><h2>How we verify</h2><ol><li>We call or email using a number or address that's publicly connected to the business.</li><li>Once confirmed, your edits go live and you become the listing's contact.</li></ol>
<p class="small">Not listed yet? <a href="/get-listed/">Get listed free</a>.</p></div></section>'''
pages['/claim/'] = ('Claim your listing | Namaste Long Island', 'Business owners and organizers: claim your Namaste Long Island listing to update details and add photos.', cl_body)

se_fields = (field('event_name', 'Event name', req=True) + field('organizer', 'Organizer', req=True) +
             field('date', 'Date', 'date', True) + field('time', 'Start and end time', req=True, ph='7:00–11:00 pm') +
             field('venue', 'Venue name', req=True) + field('address', 'Venue address and town', req=True) +
             field('price', 'Price', ph='Free, $25, $40 at the door...') + field('link', 'Tickets or info link', 'url', ph='https://') +
             field('description', 'Describe the event in your own words', area=True, req=True) +
             field('contact_name', 'Your name', req=True) + field('email', 'Your email', 'email', True) +
             '<div class="full check"><label><input type="checkbox" name="consent" value="yes" required> I\'m the organizer or authorized to share this event, the details are public, and any photo I send is mine to share. <span class="req">*</span></label></div>')
se_body = f'''<section class="phead"><div class="wrap"><p class="kicker">Submit an event</p><h1>Submit your event free</h1>
<p class="lede">Pujas, garba nights, melas, concerts, fundraisers, classes and community gatherings on Long Island. Free events and paid events are both welcome.</p></div></section>
<section class="wrap narrow">{form('submit_event', 'Event submission', se_fields, 'Submit event')}
<div class="steps"><h2>What happens next</h2><ol><li>We check the details with you or on your public page.</li><li>Your event goes on the calendar with a link back to you, and may be picked for the weekly email.</li></ol>
<p class="small">Promoted placements for events are coming soon. Listing stays free.</p></div></section>'''
pages['/submit-event/'] = ('Submit an event free | Namaste Long Island', 'Add your South Asian community event on Long Island to the Namaste Long Island calendar and weekly email. Free.', se_body)

nl_body = f'''<section class="phead"><div class="wrap"><p class="kicker">Newsletter</p><h1>The weekly Namaste Long Island email</h1>
<p class="lede">Every week: what's happening this weekend, a festival heads-up, new local businesses, and one good thing from the community. Short, local, and free.</p></div></section>
<section class="wrap narrow"><div class="form" data-form="newsletter" data-subject="Newsletter signup"><div class="fgrid">
{field('first_name', 'First name')}{field('email', 'Email', 'email', True)}{field('town', 'Your town', ph='e.g. Syosset')}
{field('interests', 'Most interested in', opts=['Events and festivals', 'Weddings', 'Food', 'Everything'])}
<input type="hidden" name="source" value="newsletter-page"></div>
<input name="_honey" type="text" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
<button type="button" class="btn send">Subscribe</button><p class="msg" role="status"></p></div>
<p class="small">We use your email only to send the newsletter. Reply "stop" any time and we'll remove you.</p>
<p class="small">Also coming: a WhatsApp Channel and Instagram for event reminders.</p></section>'''
pages['/newsletter/'] = ('Weekly newsletter | Namaste Long Island', 'A free weekly email of South Asian events, festivals, food and wedding finds on Long Island.', nl_body)

about_body = f'''<section class="phead"><div class="wrap"><p class="kicker">About</p><h1>About Namaste Long Island</h1>
<p class="lede">A friendly connector for Long Island's South Asian community: one place to find the vendors, events, food and places of worship that friends usually pass along by WhatsApp.</p></div></section>
<section class="wrap narrow prose">
<h2>Who runs it</h2><p>Namaste Long Island is run by {OPERATOR} (also behind Namaste Bookshop in NYC). Our goal is to help local families find what they need and help local businesses and organizations get found.</p>
<h2>How we check things</h2><ul><li>We list a business or place only after confirming it with the owner or on its own website or Google Maps listing.</li><li>Events link back to the organizer. We don't copy news stories or other calendars.</li><li>We never post fake reviews or reviews copied from other sites.</li></ul>
<h2>Free listings, and what will be paid</h2><p>Basic listings and event submissions are free. Later we'll offer featured placements and newsletter sponsorships. Anything paid will be clearly labeled as sponsored or featured.</p>
<h2>Corrections</h2><p>See something wrong? Email <a href="mailto:{EMAIL}">{EMAIL}</a> and we'll fix it.</p></section>'''
pages['/about/'] = ('About | Namaste Long Island', 'Who runs Namaste Long Island, how listings are verified, and how free and paid placements work.', about_body)

priv_body = f'''<section class="phead"><div class="wrap"><h1>Privacy</h1><p class="lede">Last updated {CHECKED}.</p></div></section>
<section class="wrap narrow prose">
<h2>Analytics</h2><p>We use Google Analytics to count visits, see which pages are useful, and count when someone sends a form or taps a phone, email or directions link. Google may set cookies to do this. You can block these with your browser settings or Google's opt-out add-on.</p>
<h2>Forms</h2><p>When you send a listing, claim, event or newsletter form, your entries are delivered to our inbox ({EMAIL}) through FormSubmit, a form-delivery service. We use them only to review your request, contact you, publish what you asked us to publish, and send the newsletter if you signed up.</p>
<h2>What we publish</h2><p>Only business, organization and event details you've agreed to share publicly. We never publish your personal email or phone unless you ask us to.</p>
<h2>Your choices</h2><p>Ask us to update or delete anything you've sent by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>. We don't sell personal information.</p>
<h2>Who we are</h2><p>Namaste Long Island is run by {OPERATOR}.</p></section>'''
pages['/privacy/'] = ('Privacy | Namaste Long Island', 'How Namaste Long Island uses analytics and the information you send through its forms.', priv_body)

NF = '''<section class="phead"><div class="wrap"><h1>This page wandered off</h1><p class="lede">It may have moved. Try the guide below.</p>
<div class="btns"><a class="btn" href="/">Home</a><a class="btn alt" href="/events/">Events</a><a class="btn alt" href="/weddings/">Wedding vendors</a></div></div></section>'''

exec(open(os.path.join(ROOT, 'scripts', 'directory.py')).read())

# ---------- write ----------
if os.path.isdir(DIST):
    for n in os.listdir(DIST):
        p = os.path.join(DIST, n)
        if n in ('og.jpg',): continue
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
os.makedirs(DIST, exist_ok=True)
for path, v in pages.items():
    t, d, b = v[:3]; xh = v[3] if len(v) > 3 else ''
    out = os.path.join(DIST, path.strip('/'), 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(page(path, t, d, b, xh))
open(os.path.join(DIST, '404.html'), 'w').write(page('/404', 'Page not found | Namaste Long Island', 'Page not found.', NF, '<meta name="robots" content="noindex">').replace(f'<link rel="canonical" href="{BASE}/404">', ''))
os.makedirs(os.path.join(DIST, 'assets'), exist_ok=True)
for f in ('site.css', 'site.js'):
    shutil.copy(os.path.join(ROOT, 'src', f), os.path.join(DIST, 'assets', f))
open(os.path.join(DIST, 'icon.svg'), 'w').write(DIYA.replace(' class="diya"', ' xmlns="http://www.w3.org/2000/svg"').replace(' aria-hidden="true"', ''))
open(os.path.join(DIST, 'CNAME'), 'w').write(DOMAIN + '\n')
open(os.path.join(DIST, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    ''.join(f'<url><loc>{BASE}{p}</loc><lastmod>{VER}</lastmod></url>\n' for p in pages) + '</urlset>\n')
bots = ['Googlebot', 'Bingbot', 'OAI-SearchBot', 'ChatGPT-User', 'GPTBot', 'PerplexityBot', 'Google-Extended', 'ClaudeBot']
open(os.path.join(DIST, 'robots.txt'), 'w').write(''.join(f'User-agent: {b}\nAllow: /\n\n' for b in bots) + f'User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n')
open(os.path.join(DIST, 'llms.txt'), 'w').write(f'''# {BRAND}
> A community guide to South Asian life on Long Island, New York: wedding vendors, events, a festival guide, restaurants, shops, temples, gurdwaras and community groups. Run by {OPERATOR}. Listings are free and verified with the business or on its own website.

## Pages
''' + ''.join(f'- [{v[0].split(" | ")[0]}]({BASE}{p}): {v[1]}\n' for p, v in pages.items()) + f'\nContact: {EMAIL}\n')
print('built', len(pages), 'pages')
