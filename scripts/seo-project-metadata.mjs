import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const decode=s=>s.replace(/&quot;/g,'"').replace(/&#39;|&#x27;/g,"'").replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&');
const escape=s=>String(s).replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const norm=s=>String(s).normalize('NFKC').toLowerCase().replace(/[^\p{L}\p{N}]/gu,'');
const attrs=t=>Object.fromEntries([...t.matchAll(/([\w:-]+)\s*=\s*(?:"([^"]*)"|'([^']*)')/g)].map(m=>[m[1].toLowerCase(),decode(m[2]??m[3])]));
const meta=(head,key)=>{for(const m of head.matchAll(/<meta\b[^>]*>/gi)){const a=attrs(m[0]);if(a.name===key||a.property===key)return a.content||'';}return '';};
const cleanText=s=>decode(s.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi,' ').replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi,' ').replace(/<[^>]*>/g,' ')).replace(/\s+/g,' ').trim();
function setMeta(head,key,value){if(!value)return head;const tag=`<meta ${key.startsWith('og:')?'property':'name'}="${key}" content="${escape(value)}">`;let found=false;head=head.replace(/<meta\b[^>]*>/gi,t=>{const a=attrs(t);if(a.name!==key&&a.property!==key)return t;if(found)return '';found=true;return tag;});return found?head:head+tag;}
function enrichDescription(old,target,body,isHome){let d=old.trim();if(!d)return d;if(!norm(d).includes(norm(target.keyword)))d=`${target.keyword}. ${d}`;
 d=d.replace(/계약금 5%, 계약금 5%,/g,'계약금 5%,');
 if(isHome){for(const [i,fact] of (target.facts||[]).entries()){
  if(!fact||norm(fact).length<4||!norm(body).includes(norm(fact)))continue;
  if(norm(d).includes(norm(fact)))break;
  const numbers=fact.match(/\d[\d,]*/g)||[];
  if(i>0&&numbers.length&&numbers.every(n=>norm(d).includes(norm(n))))break;
  const address=fact.match(/(\S+(?:동|리|읍|면))\s+(\d[\d-]*)/);
  if(i===0&&address&&norm(d).includes(norm(address[1]+address[2])))break;
  const addition=` ${i===2?'주택형 ':''}${fact}.`;
  if(d.length+addition.length<=160){d+=addition;break;}
 }}
 return d;
}
// Enrich verified image metadata without changing page content or layout.
export function weeklyHead(head,html,target,canonical){
 if(!target.imageMetadata)return head;
 const absolute=value=>{try{const u=new URL(value,canonical);return /^https?:$/.test(u.protocol)?u.href:value;}catch{return value;}};
 const infoFor=value=>target.imageMetadata[absolute(value)];
 const image=meta(head,'og:image');
 if(image){
  const url=absolute(image);head=setMeta(head,'og:image',url);
  const twitter=meta(head,'twitter:image');if(twitter)head=setMeta(head,'twitter:image',absolute(twitter));
  const info=infoFor(url);
  if(info){
   if(info.width&&info.height){head=setMeta(head,'og:image:width',info.width);head=setMeta(head,'og:image:height',info.height);}
   if(info.type)head=setMeta(head,'og:image:type',info.type);
   const alt=meta(head,'og:image:alt')||info.alt;
   if(alt){head=setMeta(head,'og:image:alt',alt);if(!twitter||absolute(twitter)===url)head=setMeta(head,'twitter:image:alt',alt);}
  }
 }
 head=setMeta(head,'og:url',canonical);
 if(!meta(head,'og:locale'))head=setMeta(head,'og:locale','ko_KR');
 function visit(node){
  if(!node||typeof node!=='object')return;
  if(Array.isArray(node)){node.forEach(visit);return;}
  for(const k of ['image','thumbnailUrl','primaryImageOfPage']){
   if(typeof node[k]==='string')node[k]=absolute(node[k]);
   else if(Array.isArray(node[k]))node[k]=node[k].map(x=>typeof x==='string'?absolute(x):x);
  }
  if(node['@type']==='ImageObject'){
   for(const k of ['url','contentUrl'])if(typeof node[k]==='string')node[k]=absolute(node[k]);
   const info=infoFor(node.url||node.contentUrl||'');
   if(info){if(info.width)node.width=info.width;if(info.height)node.height=info.height;if(info.type)node.encodingFormat=info.type;}
  }
  Object.values(node).forEach(visit);
 }
 return head.replace(/<script\b([^>]*\btype\s*=\s*["']application\/ld\+json["'][^>]*)>([\s\S]*?)<\/script>/gi,(all,a,raw)=>{const data=JSON.parse(raw);if(target.linkMainEntity&&Array.isArray(data['@graph'])){const page=data['@graph'].find(n=>n['@type']==='WebPage');const entity=data['@graph'].find(n=>n['@type']==='ApartmentComplex');if(page&&entity){entity['@id']||=canonical+'#apartment';page.mainEntity||={'@id':entity['@id']};}}visit(data);return `<script${a}>${JSON.stringify(data).replace(/</g,'\\u003c')}</script>`;});
}
function optimizeWeeklyOnly(html,target){
 const m=html.match(/<head\b[^>]*>([\s\S]*?)<\/head>/i);if(!m)throw new Error('Missing head');
 if(/noindex/i.test(meta(m[1],'robots')))return {html,skipped:true};
 const tag=[...m[1].matchAll(/<link\b[^>]*>/gi)].find(x=>attrs(x[0]).rel==='canonical');const canonical=tag?attrs(tag[0]).href:'';
 if(!/^https:\/\//.test(canonical))throw new Error('Missing canonical');
 const head=weeklyHead(m[1],html,target,canonical);const output=html.slice(0,m.index)+m[0].replace(m[1],head)+html.slice(m.index+m[0].length);
 return {html:output,changed:output!==html,canonical,description:meta(head,'description'),oldDescription:meta(m[1],'description')};
}

export function optimizeHtml(html,target,isHome=false){if(target.weeklyOnly)return optimizeWeeklyOnly(html,target);const match=html.match(/<head\b[^>]*>([\s\S]*?)<\/head>/i);if(!match)throw new Error('Missing head');const before=match[1];let head=before;
 if(/(?:^|,)\s*noindex/i.test(meta(head,'robots')))return {html,skipped:true};
 const title=decode((head.match(/<title\b[^>]*>([\s\S]*?)<\/title>/i)||[])[1]||'').trim();
 const canonicalTag=[...head.matchAll(/<link\b[^>]*>/gi)].find(m=>attrs(m[0]).rel==='canonical');const canonical=canonicalTag?attrs(canonicalTag[0]).href:'';
 if(!title||!/^https:\/\//.test(canonical))throw new Error(`Missing title/canonical: ${target.name}`);
 const body=cleanText(html.slice(match.index+match[0].length));const old=meta(head,'description');if(!old)throw new Error(`Missing description: ${canonical}`);
 const description=enrichDescription(old,target,body,isHome);
 for(const key of ['description','og:description','twitter:description'])head=setMeta(head,key,description);
 head=setMeta(head,'twitter:title',title);
 const image=meta(head,'og:image');if(image)head=setMeta(head,'twitter:image',image);
 let pages=0;let updated=0;
 function enrich(node){if(!node||typeof node!=='object')return;const types=Array.isArray(node['@type'])?node['@type']:[node['@type']];
 if(types.includes('WebPage')){pages++;node.description=description;node.name=title;node.inLanguage||='ko-KR';
  if(!node.about){node.about={'@type':'Place',name:target.name};const location=target.location;if(location&&norm(body).includes(norm(location)))node.about.address=location;}
  if(image&&!node.primaryImageOfPage)node.primaryImageOfPage={'@type':'ImageObject',url:new URL(image,canonical).href};
  if(!node.isPartOf)node.isPartOf={'@type':'WebSite',url:target.siteUrl||new URL('/',canonical).href,name:target.siteName||target.name};
  updated++;
 }
 if(Array.isArray(node))node.forEach(enrich);else if(node['@graph'])enrich(node['@graph']);
 }
 head=head.replace(/<script\b([^>]*\btype\s*=\s*["']application\/ld\+json["'][^>]*)>([\s\S]*?)<\/script>/gi,(all,a,raw)=>{let data;try{data=JSON.parse(raw);}catch{throw new Error(`Invalid existing JSON-LD: ${canonical}`);}enrich(data);return `<script${a}>${JSON.stringify(data).replace(/</g,'\\u003c')}</script>`;});
 if(!pages){const data={'@context':'https://schema.org','@type':'WebPage',url:canonical};enrich(data);head+=`<script type="application/ld+json">${JSON.stringify(data).replace(/</g,'\\u003c')}</script>`;}
 head=weeklyHead(head,html,target,canonical);
 const output=html.slice(0,match.index)+match[0].replace(before,head)+html.slice(match.index+match[0].length);
 if(output.slice(output.indexOf('</head>')+7)!==html.slice(html.indexOf('</head>')+7))throw new Error('Body changed');
 if(meta(head,'description')!==meta(head,'og:description')||meta(head,'description')!==meta(head,'twitter:description'))throw new Error('Description mismatch');
 return {html:output,canonical,description,oldDescription:old,changed:output!==html,structuredPages:updated};
}
function walk(dir){return fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(dir,e.name)):[path.join(dir,e.name)]);}
export function run(root,config){const report=[];for(const target of config.targets){const dir=path.join(root,target.path||'');if(!fs.existsSync(path.join(dir,'index.html')))throw new Error(`Missing target: ${dir}`);let changed=0;
 for(const file of walk(dir).filter(p=>p.endsWith('.html'))){const original=fs.readFileSync(file,'utf8');if(!/<head\b/i.test(original))continue;const result=optimizeHtml(original,target,file===path.join(dir,'index.html'));if(result.changed){fs.writeFileSync(file,result.html);changed++;}report.push({file:path.relative(root,file),canonical:result.canonical,changed:!!result.changed,descriptionChanged:result.description!==result.oldDescription,skipped:!!result.skipped});}
 if(!changed&&!config.allowUnchanged)throw new Error(`No optimization applied: ${target.name}`);
 }return report;}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){const [root,configPath]=process.argv.slice(2);if(!root||!configPath)throw new Error('Usage: node seo-project-metadata.mjs BUILD_DIR CONFIG_JSON');const report=run(path.resolve(root),JSON.parse(fs.readFileSync(configPath,'utf8')));console.log(JSON.stringify({targets:JSON.parse(fs.readFileSync(configPath,'utf8')).targets.length,pages:report.length,changed:report.filter(x=>x.changed).length,descriptions:report.filter(x=>x.descriptionChanged).length}));}
