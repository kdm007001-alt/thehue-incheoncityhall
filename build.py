from pathlib import Path
from html import escape

ROOT=Path(__file__).parent
DOMAIN='https://thehue-incheoncityhall.site'
TITLE='인천시청역 한신더휴'
NAV=[('사업개요','/info'),('입지환경','/3'),('프리미엄','/4'),('브랜드','/7'),('오시는길','/5'),('관심등록','/6')]
footer='''<footer class="site-footer"><p><strong>현장명 : 인천시청역 한신더휴 / TEL <a href="tel:15551622">1555-1622</a></strong></p><p>※ 본 홈페이지의 사진·그래픽·내용은 이해를 돕기 위한 것으로 실제와 차이가 있을 수 있습니다.</p><p>※ 주변 개발계획은 관계기관의 사업 진행에 따라 변경·축소·취소될 수 있습니다.</p><p>※ 공급 조건과 신청 가능 여부는 상담 및 계약 관련 문서로 확인하시기 바랍니다.</p><p>시공 : 한신공영㈜</p><p>분양 안내 운영 : 분양DM | 김동민 | 사업자등록번호 156-17-01862</p><p>인천광역시 검단구 이음6로33 3207-1704</p></footer>'''
privacy='''1. 수집 항목: 이름, 연락처, 생년월일, 주소, 청약통장순위, 선택 입력한 가족 정보
2. 이용 목적: 인천시청역 한신더휴 관심등록과 상담 안내
3. 보유 기간: 접수 목적 달성 또는 철회 요청 시까지
4. 동의를 거부할 수 있으며, 동의하지 않으면 관심등록 접수가 제한됩니다.
※ 수집 정보의 열람·정정·삭제 또는 동의 철회는 1555-1622로 요청할 수 있습니다.
※ 본 관심등록은 분양 상담 안내 운영자가 접수합니다.'''
form=f'''<section class="lead-section"><form class="lead-form" method="post" action="/api/interest"><h1>관심고객등록</h1><input type="hidden" name="site" value="{TITLE}"><input class="bot-field" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true"><div class="field"><label for="name">이름 <b>*</b></label><input id="name" name="name" autocomplete="name" required></div><div class="field"><label for="phone1">연락처 <b>*</b></label><div class="phone-parts"><select id="phone1" data-phone aria-label="연락처 앞자리"><option value="010">010</option></select><input data-phone aria-label="연락처 가운데 자리" inputmode="numeric" maxlength="4" pattern="[0-9]{{4}}" required><input data-phone aria-label="연락처 마지막 자리" inputmode="numeric" maxlength="4" pattern="[0-9]{{4}}" required></div></div><div class="field"><label for="birth">생년월일 <b>*</b></label><p class="hint">ex) 750202</p><input id="birth" name="birth" inputmode="numeric" minlength="6" maxlength="6" pattern="[0-9]{{6}}" required></div><div class="field"><label for="address">주소 <b>*</b></label><p class="hint">ex) 인천광역시 남동구 간석동</p><input id="address" name="address" autocomplete="address-level2" required></div><div class="field"><fieldset><legend>청약통장순위 <b>*</b></legend><label class="radio-row"><input type="radio" name="priority" value="특별공급" required> 특별공급</label><label class="radio-row"><input type="radio" name="priority" value="1순위"> 1순위</label><label class="radio-row"><input type="radio" name="priority" value="2순위"> 2순위</label></fieldset></div><div class="field"><label for="family">※ 가족 추가 청약 시</label><p class="hint">가족 이름, 연락처, 생년월일을 입력해 주세요.</p><input id="family" name="family"></div><div class="field"><label>개인정보 수집 및 이용 동의</label><div class="consent-text">{escape(privacy).replace(chr(10),'<br>')}</div><label class="agree"><input type="checkbox" name="consent" value="yes" required> 위 사항을 확인하였으며 개인정보 수집 및 이용에 동의합니다.</label><button class="form-submit" type="submit">관심고객등록</button><p class="form-status" role="status" aria-live="polite"></p></div></form></section>'''

def img(name, label, linked=False):
    element=f'<img src="/assets/{name}.png" alt="{label}" loading="lazy" width="1258">'
    return f'<a href="{dict(overview="/info",location="/3",premium="/4",brand="/7",directions="/5")[name]}" class="poster-link">{element}</a>' if linked else element

def page(route,body):
    heading=TITLE if route=='/' else f'{NAV[[u for _,u in NAV].index(route)][0]} | {TITLE}'
    desc=f'{TITLE}의 사업개요, 입지환경, 프리미엄, 브랜드, 오시는 길과 관심고객등록 안내.'
    nav=''.join(f'<a href="{u}"'+(' aria-current="page"' if route==u else '')+f'>{label}</a>' for label,u in NAV)
    html=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{heading}</title><meta name="description" content="{desc}"><link rel="canonical" href="{DOMAIN}{route}"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/styles.css"></head><body><header class="site-header"><a class="brand-name" href="/">{TITLE}</a><nav class="nav" aria-label="주요 메뉴">{nav}</nav><span class="opening">입주 안내</span><button class="menu-toggle" aria-label="메뉴 열기" aria-expanded="false">☰</button></header><main>{body}</main>{footer}<div class="zoom-modal" role="dialog" aria-modal="true" aria-label="입지지도 크게 보기"><button type="button" aria-label="닫기">×</button><img alt="입지환경 확대 이미지"></div><script src="/site.js" defer></script></body></html>'''
    path=ROOT/route.lstrip('/')/'index.html' if route!='/' else ROOT/'index.html'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(html,encoding='utf-8')

page('/',f'''<section class="hero"><div><p class="overline">도심의 새로운 일상</p><p class="latin">THE HUE</p><p class="project">인천시청역 한신더휴</p></div></section><div class="stack">{''.join(img(n,l,True) for n,l in [('overview','사업개요 및 469세대 규모'),('location','인천시청역 교통 교육 생활 입지환경'),('premium','한신더휴 프리미엄 6'),('brand','한신더휴 브랜드 소개'),('directions','인천시청역 한신더휴 현장 오시는 길')])}</div>{form}''')
for route,name,label in [('/info','overview','사업개요 및 단지규모'),('/3','location','인천시청역 입지환경'),('/4','premium','한신더휴 프리미엄 여섯 가지'),('/7','brand','한신더휴 브랜드'),('/5','directions','현장 오시는 길')]:
    extra='<button class="map-zoom" type="button" data-zoom="/assets/location.png">⌕ 크게보기</button>' if name=='location' else ''
    page(route,f'<section class="stack poster-page">{img(name,label)}{extra}</section>')
page('/6',form)
(ROOT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n',encoding='utf-8')
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{DOMAIN}{r}</loc></url>' for r in ['/','/info','/3','/4','/7','/5','/6'])+'</urlset>',encoding='utf-8')
(ROOT/'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#102d49"/><text x="32" y="45" text-anchor="middle" fill="white" font-family="sans-serif" font-size="39" font-weight="bold">H</text></svg>',encoding='utf-8')
