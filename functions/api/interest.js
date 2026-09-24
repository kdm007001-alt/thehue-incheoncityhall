const CENTRAL_LEADS_URL = 'https://site-customer-admin.pages.dev/api/leads';
const SITE_SLUG = 'incheoncityhall-hanshin-thehue';

export async function onRequestPost({ request }) {
  const json = (data, status) => new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' }
  });
  if ((request.headers.get('content-type') || '').split(';')[0] !== 'application/json') {
    return json({ error: '잘못된 요청입니다.' }, 415);
  }
  let body;
  try { body = await request.json(); } catch { return json({ error: '잘못된 요청입니다.' }, 400); }
  if (body.website) return json({ ok: true }, 200);

  const name = String(body.name || '').trim().slice(0, 40);
  const phone = String(body.phone || '').replace(/\D/g, '');
  const visitDate = String(body.visit_date || '').trim();
  const visitTime = String(body.visit_time || '').trim();
  const dateValid = /^\d{4}-\d{2}-\d{2}$/.test(visitDate) &&
    !Number.isNaN(Date.parse(visitDate)) &&
    new Date(visitDate).toISOString().slice(0, 10) === visitDate;
  const timeValid = /^(10|11|12|13|14|15|16|17):(00|30)$/.test(visitTime) || visitTime === '18:00';
  const visitInstant = dateValid && timeValid ? Date.parse(`${visitDate}T${visitTime}:00+09:00`) : NaN;
  if (name.length < 2 || !/^010\d{8}$/.test(phone) || !dateValid || !timeValid ||
      visitDate < '2026-09-28' || Number.isNaN(visitInstant) || visitInstant < Date.now() ||
      body.consent !== 'yes' || body.site !== '인천시청역 한신더휴') {
    return json({ error: '방문예약 정보를 확인해 주세요.' }, 400);
  }

  const form = new FormData();
  form.set('site_slug', SITE_SLUG);
  form.set('name', name);
  form.set('phone', phone);
  form.set('visit_date', visitDate);
  form.set('visit_time', visitTime);
  form.set('consent', 'yes');
  form.set('source_url', new URL('/6', request.url).href);
  try {
    const response = await fetch(CENTRAL_LEADS_URL, {
      method: 'POST', body: form, signal: AbortSignal.timeout(15000)
    });
    const result = await response.text();
    if (response.ok && /<h1>접수가 완료되었습니다\.<\/h1>/.test(result)) {
      return json({ ok: true }, 201);
    }
    const message = result.match(/<h1>([^<]+)<\/h1>/)?.[1] || '접수 중 오류가 발생했습니다.';
    return json({ error: message }, response.ok ? 502 : response.status);
  } catch {
    return json({ error: '접수 중 오류가 발생했습니다.' }, 503);
  }
}
