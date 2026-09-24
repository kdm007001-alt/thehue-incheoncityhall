export async function onRequestPost({ request, env }) {
  const json = (data, status) => new Response(JSON.stringify(data), {
    status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' }
  });
  if (!env.INTEREST_DB) return json({ error: '접수 서비스가 준비되지 않았습니다.' }, 503);
  if ((request.headers.get('content-type') || '').split(';')[0] !== 'application/json') return json({ error: '잘못된 요청입니다.' }, 415);
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
      !['특별공급', '1순위', '2순위'].includes(priority) || body.consent !== 'yes' || body.site !== '인천시청역 한신더휴') {
    return json({ error: '필수 항목을 확인해 주세요.' }, 400);
  }
  try {
    await env.INTEREST_DB.prepare(
      'INSERT INTO interest_leads (name, phone, birth, address, priority, family, consent_version) VALUES (?, ?, ?, ?, ?, ?, ?)'
    ).bind(name, phone, birth, address, priority, family, '2026-09-24').run();
    return json({ ok: true }, 201);
  } catch {
    return json({ error: '접수 중 오류가 발생했습니다.' }, 503);
  }
}
