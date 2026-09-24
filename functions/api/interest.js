const CENTRAL_LEADS_URL = 'https://site-customer-admin.pages.dev/api/leads';
const SITE_SLUG = '인천시청역한신더휴';

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

  const name = String(body.name || '').trim().slice(0, 60);
  const phone = String(body.phone || '').replace(/\D/g, '');
  const birth = String(body.birth || '').trim();
  const address = String(body.address || '').trim().slice(0, 250);
  const priority = String(body.priority || '');
  const family = String(body.family || '').trim().slice(0, 500);
  if (!name || !/^010\d{8}$/.test(phone) || !/^\d{6}$/.test(birth) || !address ||
      !['특별공급', '1순위', '2순위'].includes(priority) || body.consent !== 'yes' ||
      body.site !== '인천시청역 한신더휴') {
    return json({ error: '필수 항목을 확인해 주세요.' }, 400);
  }

  const form = new FormData();
  form.set('site_slug', SITE_SLUG);
  form.set('name', name);
  form.set('phone', phone);
  form.set('birth', birth);
  form.set('region', address);
  form.set('priority', priority);
  form.set('family', family);
  form.set('consent', 'yes');
  form.set('source_url', new URL('/6', request.url).href);

  try {
    const response = await fetch(CENTRAL_LEADS_URL, {
      method: 'POST',
      body: form,
      signal: AbortSignal.timeout(15000)
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
