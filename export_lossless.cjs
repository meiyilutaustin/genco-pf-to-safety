// Render editable vector HTML directly to 4K lossless WebP. No MP4 intermediate.
const {chromium}=require('playwright');
const {spawn}=require('child_process');const fs=require('fs');const path=require('path');
(async()=>{const src=__dirname;const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});const p=await browser.newPage({viewport:{width:3840,height:2160},deviceScaleFactor:1});
for(const [name,seconds] of [['02-design-and-probe',7],['03-screening',8],['04-boundary',9],['05-probe-results',7]]){
 await p.goto('file://'+path.join(src,name+'.html'));await p.evaluate(()=>window.exportMode=true);
 const frameDir=fs.mkdtempSync(require('os').tmpdir()+'/gridfm-4k-');

 for(let f=0;f<seconds*12;f++){await p.evaluate(t=>render(t),f/12);const buf=await p.screenshot({clip:{x:0,y:0,width:3840,height:2160}});if(f===0||f===seconds*12-1)fs.writeFileSync(path.join(__dirname,name+(f===0?'-first':'-last')+'.png'),buf);fs.writeFileSync(path.join(frameDir,String(f).padStart(4,'0')+'.png'),buf);}
 const py=spawn('python3',[path.join(__dirname,'encode_lossless.py'),frameDir,path.join(__dirname,name+'.webp')],{stdio:'inherit'});await new Promise((res,rej)=>py.on('close',c=>c===0?res():rej(Error('encoder '+c))));
 fs.rmSync(frameDir,{recursive:true});console.log(name+' complete '+fs.statSync(path.join(__dirname,name+'.webp')).size+' bytes');
}await browser.close();})();
