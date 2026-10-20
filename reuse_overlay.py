"""Reveal paired feature comparisons without inventing a training trajectory."""
import json

def build(root):
    data=json.loads((root/'data/paired-feature-data.json').read_text())
    over=''
    for panel in range(2):
        x=145+panel*755
        over+=f'<rect x="{x-10}" y="451" width="625" height="236" fill="white"/>'
        for tick in [.5,.6,.7,.8,.9,1.]:
            xx=x+(tick-.5)/.5*580
            over+=f'<path d="M{xx} 455 V677" stroke="#DBE3E9" stroke-width="1"/>'
    for j,d in enumerate(data):
        x=145+d['panel']*755;y=475+d['row']*59
        a=x+(d['output']-.5)/.5*580;b=x+(d['hidden']-.5)/.5*580
        delta='Equal · Δ 0.000' if abs(d['delta'])<1e-9 else f'Δ +{d["delta"]:.3f}'
        dx=a-85 if abs(d['delta'])<1e-9 else (a+b)/2
        over+=f'''<path id="gap{j}" d="M{a} {y} H{a}" stroke="#99AABB" stroke-width="2"/>
        <rect x="{a-6}" y="{y-6}" width="12" height="12" fill="#CB7C24"/>

        <g id="hidden{j}"><circle cx="{b}" cy="{y}" r="6" fill="#2768BD" stroke="white" stroke-width="1.5"/></g>
        <text id="delta{j}" x="{dx}" y="{y-4}" font-size="13" font-weight="bold" fill="#2768BD" text-anchor="middle">{delta}</text>'''
    over+='''<rect id="outputFocus" x="440" y="297" width="1074" height="72" rx="12" fill="#CB7C24" fill-opacity=".04" stroke="none" stroke-width="1.5"/>
    <rect id="hiddenFocus" x="440" y="212" width="1074" height="77" rx="12" fill="#2768BD" fill-opacity=".04" stroke="none" stroke-width="1.5"/>
    <g id="reusePacket"><rect x="-17" y="-13" width="34" height="26" rx="5" fill="white" stroke="none" stroke-width="1.5"/><path d="M-10 7V-3 M-3 7V-9 M4 7V0 M11 7V-6" stroke="#2768BD" stroke-width="3"/></g>
    <rect id="blueLegendVeil" x="75" y="756" width="245" height="38" fill="white"/><rect id="blueVeil" x="440" y="212" width="1080" height="77" rx="12" fill="#F3F7FA"/>
    <rect x="80" y="405" width="730" height="14" fill="white"/>
    <text id="reusePhase" x="800" y="413" text-anchor="middle" font-size="13" font-weight="bold" fill="#617180"></text>'''
    script='const PAIRS='+json.dumps(data)+''';
function render(t){const branch=ease((t-1.4)/.75),growth=ease((t-3)/1.4),reveal=ease((t-4.12)/.35);$('blueVeil').setAttribute('opacity',1-branch);$('blueLegendVeil').setAttribute('opacity',1-branch);$('extractBranch').setAttribute('opacity',branch);$('outputFocus').setAttribute('opacity',t<1.5?.8:.2);$('hiddenFocus').setAttribute('opacity',branch*(t<3?.8:.25));
 const fly=clamp((t-1.6)/1.1);$('reusePacket').setAttribute('transform',`translate(${176+(435-176)*fly},${277+(247-277)*fly})`);$('reusePacket').setAttribute('opacity',t>=1.6&&t<2.7?1:0);
 PAIRS.forEach((d,j)=>{const x=145+d.panel*755,y=475+d.row*59,a=x+(d.output-.5)/.5*580,b=x+(d.hidden-.5)/.5*580;$('gap'+j).setAttribute('d',`M${a} ${y} H${a+(b-a)*growth}`);$('hidden'+j).setAttribute('opacity',reveal);$('delta'+j).setAttribute('opacity',reveal);});
 $('reusePhase').textContent=t<1.5?'Local output features':t<3?'Hidden features · same target and training data':'Gain in separation score = hidden − local output';
}
'''
    return over,script,data
