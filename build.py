"""Build vector loop previews from the approved masters; evaluation artifacts only."""
from pathlib import Path
import csv,json,re,hashlib
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
OUT=Path(__file__).resolve().parent
MASTER=OUT/'masters'
TABLE=ROOT/'data'
ref={r['scorer']:r for r in csv.DictReader(open(TABLE/'texas_screen_refpoint_k2.csv'))}
curves=list(csv.DictReader(open(TABLE/'texas_screen_k2.csv')))
series={}
for key in ['genco_pred','dc','random']:
    pts=[[0,0]]+[[float(r['review_frac']),float(r['recall'])] for r in curves if r['scorer']==key and float(r['review_frac'])<float(ref[key]['review_frac'])]
    pts.append([float(ref[key]['review_frac']),float(ref[key]['recall'])])
    series[key]={'points':pts,'final':ref[key]}
# Keep original text, paths, palette and aspect ratio. No PNG resampling.
SUBTITLES={
'From predicting a physical state to deciding whether operating limits are violated.',
'Safety ranking uses outputs. A separate probe tests whether hidden features predict reactive-limit switching.',
'Texas N−2 · GENCO vs. DC and random ranking · selected scenarios receive exact AC review.',
'Why a small prediction error can flip a decision — and where the Texas screening misses actually lie.',
'Reactive-limit switching · frozen features · linear and MLP probes · matched training data.'}
def base(name):
    s=(MASTER/f'{name}.svg').read_text();s=s[s.index('<svg '):]
    s=re.sub(r'width="1152pt" height="648pt"','width="1600" height="900"',s,count=1)
    s=s.replace('APPROVED DESIGN DRAFT  /  19 OCT 2026','Dr. Meiyi Li · LSU')
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
    root=ET.fromstring(s)
    if name=='05-probe-results':
        for node in root.iter():
            if node.get('id')=='patch_6': node.set('id','extractBranch')
    for parent in root.iter():
        for node in list(parent):
            if node.tag.endswith('}text'):
                value=''.join(node.itertext())
                if value in SUBTITLES: parent.remove(node)
    s=ET.tostring(root,encoding='unicode')
    s=s.replace('Only this trains','Training')
    if name=='05-probe-results':
        s=s.replace('Test AUROC  →  higher is better','Separating Q-limit cases  →  higher is better')
    s=s.replace('misses have true normalized margins between −0.024 and 0.','misses lie within 0.024 of the operating limit.')
    s=s.replace('35.6% review budget. Margin &lt; 0 means violation. Budget misses are not the same as wrong-sign predictions.','35.6% review budget · margin &lt; 0 means violation · loading values are illustrative.')
    return s
css='''body{margin:0;background:#fff;font-family:"DejaVu Sans",Arial,sans-serif} main{width:100%;margin:0 auto} svg{display:block;width:100%;height:auto} .stage{position:relative} #overlay{position:absolute;inset:0} text{font-family:"DejaVu Sans",Arial,sans-serif;font-variant-numeric:tabular-nums} .embed .tools{display:none}.tools{padding:12px 4%;display:flex;gap:16px;align-items:center;color:#617180;font-size:14px} button,a{font:inherit;color:#2768BD;background:white;border:1px solid #DBE3E9;border-radius:6px;padding:7px 12px;text-decoration:none} @media(prefers-reduced-motion:reduce){.tools:after{content:"Reduced motion: final frame"}}'''
common='''if(new URLSearchParams(location.search).has('embed'))document.documentElement.classList.add('embed');const $=id=>document.getElementById(id);const clamp=x=>Math.max(0,Math.min(1,x));const ease=x=>{x=clamp(x);return x*x*(3-2*x)};const fmt=n=>Math.round(n).toLocaleString('en-US');let paused=new URLSearchParams(location.search).has('embed'),offset=0,last=performance.now();const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;function tick(now){if(!paused)offset+=(now-last)/1000;last=now;if(!window.exportMode)render(reduced?DURATION-.8:offset%DURATION);requestAnimationFrame(tick)}$('pause').onclick=()=>{paused=!paused;$('pause').textContent=paused?'Play':'Pause'};$('replay').onclick=()=>{offset=0;paused=false;$('pause').textContent='Pause'};window.addEventListener('message',e=>{if(e.source!==parent||e.data?.type!=='visibility')return;if(e.data.visible&&paused)offset=0;paused=!e.data.visible;last=performance.now()});requestAnimationFrame(tick);'''
def page(name,title,overlay,script,duration):
    html='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>'+title+'</title><style>'+css+'</style><main><div class="stage" role="img" aria-label="'+title+'">'+base(name)+'<svg id="overlay" viewBox="0 0 1600 900" xmlns="http://www.w3.org/2000/svg">'+overlay+'</svg></div><div class="tools"><button id="pause">Pause</button><button id="replay">Replay</button><a href="index.html">All figures</a><span>Vector master · automatic '+str(duration)+' s loop · no audio</span></div></main><script>const DURATION='+str(duration)+';'+script+common+'</script></html>'
    (OUT/f'{name}.html').write_text(html)
(OUT/'01-motivation.svg').write_text(base('01-motivation'))
page('01-motivation','From predicting grid states to assessing safety','','function render(t){}',0)
# Screening: true stored curve points, including original random baseline.
over='';colors=['#2768BD','#CB7C24','#617180']
for i,c in enumerate(colors):
    y=385+i*119
    over+=f'''<rect x="450" y="{y-3}" width="175" height="78" fill="white"/><rect x="700" y="{y-3}" width="90" height="78" fill="white"/><rect x="849" y="{y-4}" width="675" height="100" fill="white"/>
    <path d="M 451 {y+31} H 617" stroke="#DBE3E9" stroke-width="2"/>
    <g id="cards{i}"></g><text id="count{i}" x="730" y="{y+27}" font-size="20" font-weight="bold" fill="#182B3A">0</text><text x="730" y="{y+52}" font-size="14" fill="#617180">checked</text>
    <rect x="855" y="{y+5}" width="485" height="37" rx="12" fill="#ECF1F5"/><rect id="bar{i}" x="855" y="{y+5}" width="0" height="37" rx="12" fill="{c}"/>
    <text id="pct{i}" x="1372" y="{y+29}" font-size="30" font-weight="bold" fill="{c}">0.0%</text><text id="found{i}" x="855" y="{y+77}" font-size="16" font-weight="bold" fill="{c}"></text><text id="ci{i}" x="1372" y="{y+63}" font-size="14" fill="#617180"></text>'''
over+='<rect x="635" y="216" width="540" height="54" fill="#EAF2FC"/><text id="reviewCount" x="650" y="250" font-size="26" font-weight="bold" fill="#182B3A">Reviewed: 0 / 3,098</text><rect x="84" y="753" width="1430" height="32" fill="white"/><text x="85" y="774" font-size="14" fill="#617180">Illustrative cards · recorded ranking curves · final intervals: 95% bootstrap CIs.</text><rect x="1190" y="226" width="330" height="35" fill="#EAF2FC"/><text id="budget" x="1195" y="252" font-size="19" fill="#2768BD" font-weight="bold"></text>'
scr='const DATA='+json.dumps(series)+';const keys=["genco_pred","dc","random"];const colors='+json.dumps(colors)+''';
function interp(pts,f){let j=1;while(j<pts.length-1&&pts[j][0]<f)j++;const a=pts[j-1],b=pts[j];return a[1]+(b[1]-a[1])*clamp((f-a[0])/(b[0]-a[0]));}
function render(t){const p=clamp((t-1)/3.8),fade=t>7.65?1-ease((t-7.65)/.35):1;const n=Math.round(3098*p);$('overlay').style.opacity=1;$('budget').textContent='35.6% review budget';$('reviewCount').textContent='Reviewed: '+fmt(n)+' / 3,098';
keys.forEach((key,i)=>{const d=DATA[key],v=interp(d.points,n/8712),y=385+i*119;const caught=n===3098?Math.round(+d.final.recall*1549):Math.round(v*1549);$('bar'+i).setAttribute('width',485*v);$('pct'+i).textContent=(v*100).toFixed(1)+'%';$('count'+i).textContent=fmt(n);$('found'+i).textContent=fmt(caught)+' of 1,549 unsafe scenarios found';$('ci'+i).textContent=p===1?(100*d.final.ci_lo).toFixed(1)+'–'+(100*d.final.ci_hi).toFixed(1)+'%':'';
let cards='';for(let j=0;j<3;j++){const phase=(t*.95+j/3)%1;const x=p===1?567+j*15:455+phase*126;const revealed=p===1||phase>.87;const danger=revealed&&j<(i===0?3:i===1?2:1);cards+=`<g transform="translate(${x},${y+10})"><rect width="28" height="39" rx="4" fill="white" stroke="#CBD9E5"/><path d="M5 12 L15 7 L23 18 L11 27 Z M5 12 L11 27" fill="none" stroke="#9EB8CE"/><circle cx="15" cy="7" r="2" fill="${colors[i]}"/>${revealed?`<circle cx="21" cy="32" r="5" fill="${danger?'#C8434D':'#087F83'}"/><text x="21" y="35" text-anchor="middle" font-size="8" fill="white">${danger?'!':'✓'}</text>`:''}</g>`;} $('cards'+i).innerHTML=p===1?'':cards;});}
'''
# Cards must reveal after exact AC: animated card strip continues over solver and status appears downstream.
scr=scr.replace("455+phase*126","455+phase*230").replace("phase>.87","phase>.87").replace("567+j*15","692+j*19")
over=re.sub(r'<text[^>]*id="count[0-2]"[^>]*>.*?</text>', '', over)
over=re.sub(r'<text[^>]*>checked</text>', '', over)
over=re.sub(r'<text[^>]*id="found[0-2]"[^>]*>.*?</text>', '', over)
scr=re.sub(r"\$\('count'\+i\)\.textContent=fmt\(n\);",'',scr)
scr=re.sub(r"\$\('found'\+i\)\.textContent=fmt\(caught\)\+' of 1,549 unsafe scenarios found';",'',scr)
page('03-screening','Equal review budget · different safety yield',over,scr,8)
# Boundary overlay: preserve measured distribution, use masks and a vector zoom.
over='''<rect x="103" y="464" width="641" height="221" fill="#F3F7FA"/><g id="closeup"><rect x="108" y="501" width="630" height="178" rx="12" fill="white" stroke="#D5E1EA"/><text x="128" y="529" font-size="13" font-weight="bold" fill="#CB7C24">BOUNDARY CLOSE-UP</text><rect x="145" y="562" width="280" height="32" fill="#E5F2ED"/><rect x="425" y="562" width="280" height="32" fill="#FBE9EC"/><path d="M425 542 V612" stroke="#C8434D" stroke-width="2" stroke-dasharray="7 5"/><text x="425" y="610" text-anchor="middle" font-size="12" fill="#C8434D">100%</text><g id="pred"><path d="M355 568 L365 578 L355 588 L345 578Z" fill="#2768BD"/><text x="350" y="552" text-anchor="middle" font-size="15" font-weight="bold" fill="#2768BD">Predicted: 99%</text><text x="350" y="618" text-anchor="middle" font-size="14" fill="#087F83">Within limit</text></g><g id="truth"><circle cx="495" cy="578" r="8" fill="#182B3A" stroke="white" stroke-width="2"/><text x="500" y="617" text-anchor="middle" font-size="15" font-weight="bold" fill="#182B3A">True: 101%</text><text x="500" y="640" text-anchor="middle" font-size="14" fill="#C8434D">Overload</text></g><text id="opposite" x="425" y="667" text-anchor="middle" font-size="18" fill="#C8434D" font-weight="bold">Small error → opposite decisions</text></g><path id="connect" d="M602 467 L160 501 M642 467 L700 501" fill="none" stroke="#C8D6E1" stroke-width="2"/><rect id="limitGlow" x="602" y="379" width="40" height="56" rx="6" fill="#CB7C24" fill-opacity=".16" stroke="#CB7C24" stroke-width="2"/><rect id="evidenceGlow" x="1352" y="370" width="71" height="236" rx="6" fill="#C8434D" fill-opacity=".07"/><rect id="evidenceVeil" x="814" y="300" width="712" height="410" fill="#FAFCFD" opacity=".25"/>'''
a=over.index('<path id="connect"');b=over.index('<rect id="limitGlow"');connector=over[a:b];over=over[:a]+over[b:];over=over.replace('<g id="closeup">',connector+'<g id="closeup">')
scr='''function render(t){const zoom=ease((t-1)/1.4),dots=ease((t-2.5)/.7),truth=ease((t-3.25)/.65),note=ease((t-3.9)/.5),evidence=ease((t-4.8)/.8);const fade=t>8.65?1-ease((t-8.65)/.35):1;$('overlay').style.opacity=1;$('closeup').setAttribute('opacity',zoom);$('closeup').setAttribute('transform',`translate(425,501) scale(1,${Math.max(.001,zoom)}) translate(-425,-501)`);$('connect').setAttribute('opacity',zoom);$('pred').setAttribute('opacity',dots);$('truth').setAttribute('opacity',truth);$('opposite').setAttribute('opacity',note);$('limitGlow').setAttribute('opacity',.25+.75*(1-zoom));$('evidenceVeil').setAttribute('opacity',.25*(1-evidence));$('evidenceGlow').setAttribute('opacity',evidence*(.6+.4*Math.sin(Math.min(1,(t-5.6)/.8)*Math.PI)));}'''
page('04-boundary','A small error across an operating limit',over,scr,9)
from probe_overlay import OVERLAY, SCRIPT
page('02-design-and-probe','Frozen model · train a small probe',OVERLAY,SCRIPT,7)
from reuse_overlay import build as build_reuse
reuse_over,reuse_script,reuse_data=build_reuse(ROOT)
page('05-probe-results','Hidden versus local output features · paired AUROC differences',reuse_over,reuse_script,7)
(OUT/'paired-feature-data.json').write_text(json.dumps(reuse_data,indent=2)+'\n')
from article import build_article
build_article(ROOT,OUT)
(OUT/'curve-data.json').write_text(json.dumps(series,indent=2)+'\n')
print('Built vector previews; endpoints:', {k:round(float(v['final']['recall'])*1549) for k,v in series.items()})
