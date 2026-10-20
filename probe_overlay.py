"""Localized figure 2 animation. All movement is a conceptual schematic."""
OVERLAY='''
<defs><marker id="probeArrow" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto"><path d="M0 0 L6 3.5 L0 7Z" fill="#2768BD"/></marker></defs>
<!-- Hide only the original feature bars, not the model or dataset panels. -->
<rect x="1173" y="351" width="151" height="79" rx="7" fill="white"/>
<g id="featureBars"></g>
<rect id="frozenFocus" x="952" y="319" width="149" height="39" rx="10" fill="#2768BD" fill-opacity=".06" stroke="#2768BD" stroke-width="1.5"/>
<rect id="layerFocus" x="921" y="374" width="28" height="190" rx="10" fill="#2768BD" fill-opacity=".08" stroke="#2768BD" stroke-width="2"/>
<g id="featurePacket"><rect x="-17" y="-15" width="34" height="30" rx="5" fill="white" stroke="#2768BD" stroke-width="1.5"/><path d="M-10 7V-3 M-3 7V-9 M4 7V0 M11 7V-6" stroke="#2768BD" stroke-width="3.5"/></g>
<g id="featureFlow"><circle r="4" fill="#2768BD"/></g>
<g id="probeTraining"><circle cx="1401" cy="370" r="8" fill="none" stroke="#087F83" stroke-width="2"/><circle cx="1401" cy="389" r="8" fill="none" stroke="#087F83" stroke-width="2"/><circle cx="1401" cy="408" r="8" fill="none" stroke="#087F83" stroke-width="2"/><circle cx="1451" cy="389" r="12" fill="none" stroke="#087F83" stroke-width="2"/><path d="M1401 370 L1451 389 M1401 389 H1451 M1401 408 L1451 389" stroke="#087F83" stroke-width="3" fill="none"/></g>
<rect x="1368" y="483" width="140" height="29" fill="#F3F7FA"/><text id="probeState" x="1443" y="503" text-anchor="middle" font-size="14" fill="#087F83">Training</text>
<rect id="trainFocus" x="850" y="651" width="332" height="68" rx="10" fill="#087F83" fill-opacity=".05" stroke="#087F83" stroke-width="1.5"/>
<rect id="testFocus" x="1223" y="651" width="280" height="68" rx="10" fill="#087F83" fill-opacity=".05" stroke="#087F83" stroke-width="1.5"/>
<g id="trainingSample"><rect x="-9" y="-13" width="18" height="26" rx="3" fill="white" stroke="#087F83"/><path d="M-5 -5 L3 -8 L5 2 L-2 6Z" stroke="#087F83" fill="none"/><circle cx="5" cy="8" r="3" fill="#087F83"/></g>
<rect id="targetFocus" x="1200" y="540" width="303" height="78" rx="12" fill="#087F83" fill-opacity=".04" stroke="none" stroke-width="1.5"/>
<rect x="850" y="610" width="350" height="22" fill="#F3F7FA"/><text id="phaseLabel" x="855" y="626" font-size="13" font-weight="bold" fill="#087F83"></text>
'''
SCRIPT='''
const vals=[.28,.8,.48,.94,.58,.36,.7,.46];
function render(t){
 const extracted=ease((t-1.1)/1.25),training=t>=2.4&&t<4.3,evaluating=t>=4.3,flight=clamp((t-.95)/1.3),x=934*(1-flight)*(1-flight)+2*1080*(1-flight)*flight+1178*flight*flight,y=402*(1-flight)*(1-flight)+2*333*(1-flight)*flight+388*flight*flight;
 $('frozenFocus').setAttribute('opacity',t<.9?.5+.5*Math.sin(t/.9*Math.PI):.25);
 $('layerFocus').setAttribute('opacity',t<2.4?(.2+.65*Math.sin(clamp((t-.5)/1.9)*Math.PI)):.22);
 $('featurePacket').setAttribute('opacity',t>.95&&t<2.25?1:0);$('featurePacket').setAttribute('transform',`translate(${x},${y})`);
 $('featureBars').innerHTML=vals.map((v,i)=>{const h=65*v*extracted;return `<rect x="${1180+i*135/8}" y="${422-h}" width="${135/11}" height="${h}" rx="2" fill="#2768BD"/>`}).join('');
 $('probeTraining').setAttribute('opacity',training?.35+.65*Math.sin((t-2.4)*Math.PI*3)**2:0);
 $('probeState').textContent=training?'Training':evaluating?'Evaluation':'Training';
 $('trainFocus').setAttribute('opacity',training?.9:.0);$('testFocus').setAttribute('opacity',evaluating?.8:0);$('targetFocus').setAttribute('opacity',ease((t-4.6)/.6)*.8);
 const p=((t-2.4)*1.4)%1;$('trainingSample').setAttribute('opacity',training?1:0);$('trainingSample').setAttribute('transform',`translate(${1048+63*p},685)`);
 const q=clamp((t-4.3)/.65);$('featureFlow').setAttribute('opacity',evaluating&&q<1?1:0);$('featureFlow').setAttribute('transform',`translate(${1338+55*q},389)`);
 $('phaseLabel').textContent=t<.9?'Frozen GENCO':t<2.4?'Extract hidden features':training?'Train the probe':'Evaluate on held-out scenarios';
}
'''
