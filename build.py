from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).parent
DOMAIN = 'https://thehue-incheoncityhall.site'
TITLE = '인천시청역 한신더휴'
DESCRIPTION = f'{TITLE}의 사업개요, 입지환경, 프리미엄, 브랜드, 오시는 길과 방문예약 안내.'
SOCIAL_IMAGE = f'{DOMAIN}/assets/overview-official.png'
NAV = [('사업개요','/info'),('입지환경','/3'),('프리미엄','/4'),('브랜드','/7'),('오시는길','/5'),('방문예약','/6')]
footer = '''<footer class="site-footer"><p><strong>현장명 : 인천시청역 한신더휴 / TEL <a href="tel:15551622">1555-1622</a></strong></p><p>※ 본 홈페이지의 사진·그래픽·내용은 이해를 돕기 위한 것으로 실제와 차이가 있을 수 있습니다.</p><p>※ 주변 개발계획은 관계기관의 사업 진행에 따라 변경·축소·취소될 수 있습니다.</p><p>※ 공급 조건과 신청 가능 여부는 상담 및 계약 관련 문서로 확인하시기 바랍니다.</p><p>시공 : 한신공영㈜</p><p>분양 안내 운영 : 분양DM | 김동민 | 사업자등록번호 156-17-01862</p><p>인천광역시 검단구 이음6로33 3207-1704</p></footer>'''
privacy = '''1. 수집 항목: 이름, 연락처, 방문날짜, 방문시간
2. 이용 목적: 인천시청역 한신더휴 방문예약 및 상담 안내
3. 보유 기간: 접수 목적 달성 또는 철회 요청 시까지
4. 동의를 거부할 수 있으며, 동의하지 않으면 방문예약이 제한됩니다.
※ 열람·정정·삭제 또는 동의 철회는 1555-1622로 요청할 수 있습니다.'''

IMAGE_SIZES = {
    'overview-official.webp': (830, 1049),
    'terms-grid.webp': (1254, 1254),
    'location-official.webp': (828, 770),
    'siteplan-official.webp': (832, 1955),
    'brand-official.webp': (1158, 2048),
    'directions-official.webp': (833, 397),
    'premium.png': (1258, 1340),
}

def picture(filename, alt, eager=False):
    width, height = IMAGE_SIZES[filename]
    priority = 'eager" fetchpriority="high' if eager else 'lazy'
    return f'<img src="/assets/{filename}" alt="{escape(alt)}" width="{width}" height="{height}" loading="{priority}" decoding="async">'

event = '''<section class="reservation-intro" aria-labelledby="reserve-title"><svg class="reservation-icon" viewBox="0 0 64 64" aria-hidden="true"><rect x="11" y="15" width="42" height="39" rx="4" fill="none" stroke="currentColor" stroke-width="4"/><path d="M11 26h42M21 9v12M43 9v12M22 36h9M35 36h9M22 45h9" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"/></svg><h2 id="reserve-title">온라인 방문예약</h2><p>(9월 28일 이후 방문 일정 예약 접수중)</p><span class="intro-rule" aria-hidden="true"></span></section>'''
times = ''.join(f'<option value="{h:02d}:{m:02d}">{"오전" if h<12 else "오후"} {h if h<=12 else h-12}시{f" {m}분" if m else ""}</option>' for h in range(10,19) for m in (0,30) if h<18 or m==0)
form = f'''<section class="lead-section" id="reservation"><form class="lead-form" method="post" action="/api/interest"><h2>방문예약</h2><input type="hidden" name="site" value="{TITLE}"><input class="bot-field" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true"><div class="field"><label for="name">이름 <b>*</b></label><input id="name" name="name" autocomplete="name" maxlength="40" required></div><div class="field"><label for="phone1">연락처 <b>*</b></label><div class="phone-parts"><select id="phone1" data-phone aria-label="연락처 앞자리"><option value="010">010</option></select><input data-phone aria-label="연락처 가운데 자리" inputmode="numeric" maxlength="4" pattern="[0-9]{{4}}" required><input data-phone aria-label="연락처 마지막 자리" inputmode="numeric" maxlength="4" pattern="[0-9]{{4}}" required></div></div><div class="field"><label for="visit-date">방문날짜 <b>*</b></label><input id="visit-date" name="visit_date" type="date" min="2026-09-28" required></div><div class="field"><label for="visit-time">방문시간 <b>*</b></label><select id="visit-time" name="visit_time" required><option value="">방문시간을 선택해 주세요</option>{times}</select></div><div class="field"><label>개인정보 수집 및 이용 동의</label><div class="consent-text">{escape(privacy).replace(chr(10),'<br>')}</div><label class="agree"><input type="checkbox" name="consent" value="yes" required> 위 사항을 확인하였으며 개인정보 수집 및 이용에 동의합니다.</label><button class="form-submit" type="submit">방문예약 신청</button><p class="form-status" role="status" aria-live="polite"></p></div></form></section>'''

def page(route, body):
    heading = TITLE if route=='/' else f'{dict((url,label) for label,url in NAV)[route]} | {TITLE}'
    section_name = TITLE if route == '/' else dict((url,label) for label,url in NAV)[route]
    nav = ''.join(f'<a href="{url}"'+(' aria-current="page"' if route==url else '')+f'>{label}</a>' for label,url in NAV)
    canonical = DOMAIN + (route if route == '/' else route + '/')
    breadcrumb_items = [{
        '@type': 'ListItem', 'position': 1, 'name': TITLE, 'item': DOMAIN + '/'
    }]
    if route != '/':
        breadcrumb_items.append({
            '@type': 'ListItem', 'position': 2, 'name': section_name, 'item': canonical
        })
    structured_data = json.dumps({
        '@context': 'https://schema.org',
        '@graph': [
            {'@type': 'WebSite', '@id': DOMAIN + '/#website', 'url': DOMAIN + '/', 'name': TITLE, 'inLanguage': 'ko-KR'},
            {'@type': 'WebPage', '@id': canonical + '#webpage', 'url': canonical, 'name': heading,
             'description': DESCRIPTION, 'isPartOf': {'@id': DOMAIN + '/#website'}, 'inLanguage': 'ko-KR'},
            {'@type': 'BreadcrumbList', 'itemListElement': breadcrumb_items},
        ]
    }, ensure_ascii=False, separators=(',', ':'))
    html = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{heading}</title><meta name="description" content="{DESCRIPTION}"><meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"><meta name="googlebot" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canonical}"><link rel="alternate" type="application/rss+xml" title="{TITLE} RSS" href="{DOMAIN}/rss.xml"><meta property="og:locale" content="ko_KR"><meta property="og:type" content="website"><meta property="og:site_name" content="{TITLE}"><meta property="og:title" content="{heading}"><meta property="og:description" content="{DESCRIPTION}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{SOCIAL_IMAGE}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{heading}"><meta name="twitter:description" content="{DESCRIPTION}"><meta name="twitter:image" content="{SOCIAL_IMAGE}"><script type="application/ld+json">{structured_data}</script><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/styles.css"></head><body><header class="site-header"><a class="brand-name" href="/">{TITLE}</a><nav class="nav" aria-label="주요 메뉴">{nav}</nav><button class="menu-toggle" aria-label="메뉴 열기" aria-expanded="false">☰</button></header><main>{body}</main>{footer}<div class="zoom-modal" role="dialog" aria-modal="true" aria-label="지역도 크게 보기"><button type="button" aria-label="닫기">×</button><img alt="지역도 확대 이미지"></div><script src="/site.js?v=20260924-reserve-open" defer></script></body></html>'''
    path = ROOT/route.lstrip('/')/'index.html' if route!='/' else ROOT/'index.html'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(html,encoding='utf-8')

shortcuts = '''<section class="home-shortcuts" aria-label="주요 안내"><div class="status-tiles"><div class="households">총 469세대</div><div class="open-date">9월 28일 오픈예정</div></div><a class="shortcut shortcut-location" href="/3"><svg viewBox="0 0 64 64" aria-hidden="true"><path d="M6 14l17-6 18 6 17-6v42l-17 6-18-6-17 6zM23 8v42m18-36v42"/></svg><span>입지환경</span></a><a class="shortcut shortcut-premium" href="/4"><svg viewBox="0 0 64 64" aria-hidden="true"><path d="M8 32L32 10l24 22M15 28v27h34V28M27 55V38h10v17"/></svg><span>프리미엄</span></a><a class="shortcut shortcut-overview" href="/info"><svg viewBox="0 0 64 64" aria-hidden="true"><path d="M10 11h27l11 11v32H10zM37 11v11h11M16 29h25M16 37h25M16 45h18"/></svg><span>사업개요</span></a></section>'''
posters = [('overview-official.webp','조감도와 사업개요'),('terms-grid.webp','민간임대 핵심 계약조건'),('location-official.webp','인천시청역 한신더휴 지역도'),('siteplan-official.webp','단지 배치도와 동호수 배치도'),('brand-official.webp','한신공영 브랜드 소개'),('directions-official.webp','오시는 길 약도')]
hero = '''<section class="hero"><div><p class="overline">도심의 새로운 일상</p><p class="latin">THE HUE</p><h1 class="project">인천시청역 한신더휴</h1></div></section>'''
page('/',hero+shortcuts+event+form+'<div class="stack home-posters">'+''.join(picture(*item) for item in posters)+'</div>')
page('/info','<section class="stack poster-page">'+picture(*posters[0], eager=True)+'</section>')
page('/3','<section class="stack poster-page">'+picture(*posters[2], eager=True)+'<button class="map-zoom" type="button" data-zoom="/assets/location-official.webp">⌕ 크게보기</button></section>')
page('/4','<section class="stack poster-page">'+picture(*posters[1], eager=True)+picture('premium.png','기존 한신더휴 프리미엄 안내 이미지')+'</section>')
page('/7','<section class="stack poster-page">'+picture(*posters[4], eager=True)+'</section>')
page('/5','<section class="stack poster-page">'+picture(*posters[5], eager=True)+'</section>')
page('/6',event+form)
(ROOT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n',encoding='utf-8')
routes = ['/','/info/','/3/','/4/','/7/','/5/','/6/']
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{DOMAIN}{r}</loc></url>' for r in routes)+'</urlset>',encoding='utf-8')

# The RSS descriptions mirror the public sections and link to the same image assets.
feed_pages = [
    ('/', TITLE, '총 469세대, 9월 28일 오픈예정. 온라인 방문예약, 사업개요, 입지환경, 프리미엄, 브랜드, 오시는 길 안내.', posters),
    ('/info/', '사업개요 | '+TITLE, '조감도와 사업개요 안내.', [posters[0]]),
    ('/3/', '입지환경 | '+TITLE, '인천시청역 한신더휴 지역도.', [posters[2]]),
    ('/4/', '프리미엄 | '+TITLE, '민간임대 핵심 계약조건과 한신더휴 프리미엄 안내.', [posters[1], ('premium.png','기존 한신더휴 프리미엄 안내 이미지')]),
    ('/7/', '브랜드 | '+TITLE, '한신공영 브랜드 소개.', [posters[4]]),
    ('/5/', '오시는길 | '+TITLE, '오시는 길 약도.', [posters[5]]),
    ('/6/', '방문예약 | '+TITLE, '방문예약 신청. 이름, 연락처, 방문날짜, 방문시간을 입력합니다. 방문날짜는 9월 28일부터, 시간은 오전 10시부터 오후 6시까지 30분 단위입니다.', []),
]
feed_items = []
for route, title, summary, images in feed_pages:
    url = DOMAIN + route
    body = '<p>'+escape(summary)+'</p>'+''.join(f'<img src="{DOMAIN}/assets/{filename}" alt="{escape(alt)}">' for filename, alt in images)
    feed_items.append(f'<item><title>{escape(title)}</title><link>{url}</link><description>{escape(body)}</description><pubDate>Thu, 24 Sep 2026 12:00:00 +0900</pubDate><guid isPermaLink="true">{url}</guid></item>')
(ROOT/'rss.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>'+TITLE+'</title><link>'+DOMAIN+'/</link><description>인천시청역 한신더휴 현장 안내와 방문예약</description><language>ko-KR</language>'+''.join(feed_items)+'</channel></rss>',encoding='utf-8')
