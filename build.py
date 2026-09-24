from pathlib import Path
from html import escape

ROOT = Path(__file__).parent
DOMAIN = 'https://thehue-incheoncityhall.site'
TITLE = '인천시청역 한신더휴'
NAV = [('사업개요','/info'),('입지환경','/3'),('프리미엄','/4'),('브랜드','/7'),('오시는길','/5'),('방문예약','/6')]
footer = '''<footer class="site-footer"><p><strong>현장명 : 인천시청역 한신더휴 / TEL <a href="tel:15551622">1555-1622</a></strong></p><p>※ 본 홈페이지의 사진·그래픽·내용은 이해를 돕기 위한 것으로 실제와 차이가 있을 수 있습니다.</p><p>※ 주변 개발계획은 관계기관의 사업 진행에 따라 변경·축소·취소될 수 있습니다.</p><p>※ 공급 조건과 신청 가능 여부는 상담 및 계약 관련 문서로 확인하시기 바랍니다.</p><p>시공 : 한신공영㈜</p><p>분양 안내 운영 : 분양DM | 김동민 | 사업자등록번호 156-17-01862</p><p>인천광역시 검단구 이음6로33 3207-1704</p></footer>'''
privacy = '''1. 수집 항목: 이름, 연락처, 방문날짜, 방문시간
2. 이용 목적: 인천시청역 한신더휴 방문예약 및 상담 안내
3. 보유 기간: 접수 목적 달성 또는 철회 요청 시까지
4. 동의를 거부할 수 있으며, 동의하지 않으면 방문예약이 제한됩니다.
※ 열람·정정·삭제 또는 동의 철회는 1555-1622로 요청할 수 있습니다.'''

def picture(filename, alt):
    return f'<img src="/assets/{filename}" alt="{escape(alt)}" loading="lazy">'

event = '''<section class="reservation-intro" aria-labelledby="reserve-title"><svg class="reservation-icon" viewBox="0 0 64 64" aria-hidden="true"><rect x="11" y="15" width="42" height="39" rx="4" fill="none" stroke="currentColor" stroke-width="4"/><path d="M11 26h42M21 9v12M43 9v12M22 36h9M35 36h9M22 45h9" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"/></svg><h2 id="reserve-title">온라인 방문예약</h2><p>(9월 28일 이후 방문 일정 예약 접수중)</p><span class="intro-rule" aria-hidden="true"></span></section>'''
times = ''.join(f'<option value="{h:02d}:{m:02d}">{"오전" if h<12 else "오후"} {h if h<=12 else h-12}시{f" {m}분" if m else ""}</option>' for h in range(10,19) for m in (0,30) if h<18 or m==0)
form = f'''<section class="lead-section" id="reservation"><form class="lead-form" method="post" action="/api/interest"><h2>방문예약</h2><input type="hidden" name="site" value="{TITLE}"><input class="bot-field" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true"><div class="field"><label for="name">이름 <b>*</b></label><input id="name" name="name" autocomplete="name" maxlength="40" required></div><div class="field"><label for="phone1">연락처 <b>*</b></label><div class="phone-parts"><select id="phone1" data-phone aria-label="연락처 앞자리"><option value="010">010</option></select><input data-phone aria-label="연락처 가운데 자리" inputmode="numeric" maxlength="4" pattern="[0-9]{{4}}" required><input data-phone aria-label="연락처 마지막 자리" inputmode="numeric" maxlength="4" pattern="[0-9]{{4}}" required></div></div><div class="field"><label for="visit-date">방문날짜 <b>*</b></label><input id="visit-date" name="visit_date" type="date" min="2026-09-28" required></div><div class="field"><label for="visit-time">방문시간 <b>*</b></label><select id="visit-time" name="visit_time" required><option value="">방문시간을 선택해 주세요</option>{times}</select></div><div class="field"><label>개인정보 수집 및 이용 동의</label><div class="consent-text">{escape(privacy).replace(chr(10),'<br>')}</div><label class="agree"><input type="checkbox" name="consent" value="yes" required> 위 사항을 확인하였으며 개인정보 수집 및 이용에 동의합니다.</label><button class="form-submit" type="submit">방문예약 신청</button><p class="form-status" role="status" aria-live="polite"></p></div></form></section>'''

def page(route, body):
    heading = TITLE if route=='/' else f'{dict((url,label) for label,url in NAV)[route]} | {TITLE}'
    nav = ''.join(f'<a href="{url}"'+(' aria-current="page"' if route==url else '')+f'>{label}</a>' for label,url in NAV)
    html = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{heading}</title><meta name="description" content="{TITLE}의 사업개요, 입지환경, 프리미엄, 브랜드, 오시는 길과 방문예약 안내."><link rel="canonical" href="{DOMAIN}{route}"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/styles.css"></head><body><header class="site-header"><a class="brand-name" href="/">{TITLE}</a><nav class="nav" aria-label="주요 메뉴">{nav}</nav><button class="menu-toggle" aria-label="메뉴 열기" aria-expanded="false">☰</button></header><main>{body}</main>{footer}<div class="zoom-modal" role="dialog" aria-modal="true" aria-label="지역도 크게 보기"><button type="button" aria-label="닫기">×</button><img alt="지역도 확대 이미지"></div><script src="/site.js" defer></script></body></html>'''
    path = ROOT/route.lstrip('/')/'index.html' if route!='/' else ROOT/'index.html'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(html,encoding='utf-8')

shortcuts = '''<section class="home-shortcuts" aria-label="주요 안내"><div class="status-tiles"><div class="households">총 469세대</div><div class="open-date">9월 28일 오픈예정</div></div><a class="shortcut shortcut-location" href="/3"><svg viewBox="0 0 64 64" aria-hidden="true"><path d="M6 14l17-6 18 6 17-6v42l-17 6-18-6-17 6zM23 8v42m18-36v42"/></svg><span>입지환경</span></a><a class="shortcut shortcut-premium" href="/4"><svg viewBox="0 0 64 64" aria-hidden="true"><path d="M8 32L32 10l24 22M15 28v27h34V28M27 55V38h10v17"/></svg><span>프리미엄</span></a><a class="shortcut shortcut-overview" href="/info"><svg viewBox="0 0 64 64" aria-hidden="true"><path d="M10 11h27l11 11v32H10zM37 11v11h11M16 29h25M16 37h25M16 45h18"/></svg><span>사업개요</span></a></section>'''
posters = [('overview-official.png','조감도와 사업개요'),('terms-grid.png','민간임대 핵심 계약조건'),('location-official.png','인천시청역 한신더휴 지역도'),('siteplan-official.png','단지 배치도와 동호수 배치도'),('brand-official.jpg','한신공영 브랜드 소개'),('directions-official.png','오시는 길 약도')]
hero = '''<section class="hero"><div><p class="overline">도심의 새로운 일상</p><p class="latin">THE HUE</p><p class="project">인천시청역 한신더휴</p></div></section>'''
page('/',hero+shortcuts+event+form+'<div class="stack home-posters">'+''.join(picture(*item) for item in posters)+'</div>')
page('/info','<section class="stack poster-page">'+picture(*posters[0])+'</section>')
page('/3','<section class="stack poster-page">'+picture(*posters[2])+'<button class="map-zoom" type="button" data-zoom="/assets/location-official.png">⌕ 크게보기</button></section>')
page('/4','<section class="stack poster-page">'+picture(*posters[1])+picture('premium.png','기존 한신더휴 프리미엄 안내 이미지')+'</section>')
page('/7','<section class="stack poster-page">'+picture(*posters[4])+'</section>')
page('/5','<section class="stack poster-page">'+picture(*posters[5])+'</section>')
page('/6',event+form)
(ROOT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n',encoding='utf-8')
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{DOMAIN}{r}</loc></url>' for r in ['/','/info','/3','/4','/7','/5','/6'])+'</urlset>',encoding='utf-8')
