"""Build the local question / paragraph / figure reading preview."""
import re,html

def build_article(root,out):
    src=(root/'post.md').read_text()
    title=src.splitlines()[0][2:]
    blocks=re.findall(r'\*\*(.*?)\*\* (.*?)(?=\n\n|\Z)',src,re.S)
    assert len(blocks)==5
    figures=['01-motivation','02-design-and-probe','03-screening','04-boundary','05-probe-results']
    captions=[
        '',
        '',
        'Texas N−2 · 8,712 scenarios with predictions; 1,549 unsafe. Each method reviews 3,098 scenarios. Bars follow recorded ranking curves; motion between points is interpolated. Final intervals are 95% bootstrap CIs.',
        'Left: illustrative 99% / 101% line loading. Right: observed Texas misses at a 35.6% review budget. Group percentages use separate denominators; 104 of 122 misses (85.2%) lie in [−0.005, 0). Budget misses and wrong-sign predictions are different quantities.',
        'Four grids × two probe heads · layer 11 · both feature sets include Q limits. Separation score (AUROC): 0.5 = chance ranking; 1 = perfect separation. Gains use unrounded scores. This is a selected feature comparison; raw-input controls do not support attributing the gain uniquely to pretraining.'
    ]
    sections=[]
    for i,((q,p),name,caption) in enumerate(zip(blocks,figures,captions),1):
        caption_html=f'<figcaption>{html.escape(caption)}</figcaption>' if caption else ''
        asset=f'media/{name}-4k.png' if i==1 else f'media/{name}.webp'
        visual=f'<a class="figure-link" href="{asset}" target="_blank" rel="noopener"><img src="{asset}" alt="{html.escape(q)}"></a>'
        sections.append(f'<section id="section-{i}"><div class="prose"><span class="number">0{i}</span><h2>{html.escape(q)}</h2><p>{html.escape(p.strip())}</p></div><figure>{visual}{caption_html}</figure></section>')
    doc='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>From Power Flow to Safety</title><style>
    *{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#fff;color:#182B3A;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;-webkit-font-smoothing:antialiased}header{max-width:1190px;margin:76px auto 65px;padding:0 24px}.eyebrow{font-size:12px;color:#087F83;text-transform:uppercase;letter-spacing:.17em;font-weight:650}h1{font-size:clamp(32px,4.2vw,52px);line-height:1.14;letter-spacing:-.035em;font-weight:650;margin:22px 0} .byline{font-size:16px;color:#617180;margin:24px 0}section{padding:48px 0 54px;border-top:1px solid #E8EDF1;max-width:1190px;margin:auto}.prose{max-width:1190px;margin:0 auto;padding:0}.number{font-size:12px;color:#087F83;letter-spacing:.12em;font-weight:650}h2{font-size:clamp(23px,2.6vw,30px);line-height:1.25;letter-spacing:-.015em;margin:12px 0 18px;font-weight:650}.prose p{font-size:17px;line-height:1.72;margin:0;color:#344957}figure{margin:30px auto 0;max-width:768px} .conclusion{max-width:1190px;margin:0 auto;padding:44px 24px 52px;border-top:1px solid #E8EDF1}.conclusion p{font-size:19px;line-height:1.65;color:#182B3A} @media(min-width:1536px){figure{max-width:896px}}iframe,img{border:0;width:100%;aspect-ratio:16/9;display:block;background:white}figcaption{max-width:1190px;padding:0 24px;margin:12px auto 0;color:#617180;font-size:13px;line-height:1.65}footer{max-width:1190px;padding:28px 30px 64px;margin:auto;font-size:14px;color:#617180}a{color:#2768BD;text-decoration:none}a:hover{text-decoration:underline}@media(max-width:680px){header{margin-top:38px;margin-bottom:36px}section{padding:30px 0}.prose p{font-size:17px}.prose,header,figcaption{padding-left:22px;padding-right:22px}figure{margin-top:18px}}
    </style><header><div class="eyebrow">Power flow · safety · representation reuse</div><h1>'''+html.escape(title)+'''</h1><div class="byline">Dr. Meiyi Li · LSU</div></header><main>'''+''.join(sections)+'<section class="conclusion"><h2>Conclusion</h2><p>'+html.escape(src.split('## Conclusion\n\n',1)[1].strip())+'</p></section>'+'''</main><footer>Dr. Meiyi Li · LSU</footer></html>'''
    (out/'index.html').write_text(doc)
