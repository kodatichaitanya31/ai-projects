"""HTML page served at /."""

PAGE = """<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>AI Interview Prep</title>
<style>
body{font-family:system-ui,sans-serif;max-width:760px;margin:2rem auto;padding:0 1rem;color:#222}
.card{border:1px solid #ddd;border-radius:10px;padding:1rem;margin:1rem 0}
button{background:#2563eb;color:#fff;border:0;padding:.5rem 1rem;border-radius:6px;cursor:pointer}
textarea,input[type=text]{width:100%;box-sizing:border-box;padding:.5rem;margin:.4rem 0}
.tag{display:inline-block;background:#e0e7ff;border-radius:12px;padding:2px 10px;margin:2px}
.fb{background:#f0fdf4;padding:.5rem;border-radius:6px;white-space:pre-wrap;margin-top:.4rem}
</style>
<h1>AI Interview Prep</h1>
<p>Upload your resume (PDF, DOCX or TXT) to get tailored interview questions and answer feedback.</p>
<div class=card>
<input type=text id=role placeholder="Target role (e.g. Backend Developer)">
<input type=file id=resume accept=".pdf,.docx,.txt"><br><br>
<button onclick=analyze()>Generate questions</button> <span id=status></span>
</div>
<div id=out></div>
<script>
const esc=s=>s.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
async function analyze(){
  const f=document.getElementById('resume').files[0];
  if(!f){alert('Choose a resume file');return}
  const fd=new FormData();fd.append('resume',f);fd.append('role',document.getElementById('role').value);
  status.textContent='Analyzing...';
  const r=await fetch('/api/analyze',{method:'POST',body:fd});const d=await r.json();
  status.textContent='';
  if(d.error){out.innerHTML='<p style=color:red>'+esc(d.error)+'</p>';return}
  let h='<div class=card><b>Skills found:</b><br>'+(d.skills.map(s=>'<span class=tag>'+esc(s)+'</span>').join('')||'none detected')+
        '<br><small>Questions by: '+d.mode+'</small></div>';
  d.questions.forEach((q,i)=>{h+='<div class=card><b>Q'+(i+1)+'. '+esc(q)+'</b>'+
    '<textarea rows=4 id=a'+i+' placeholder="Type your answer..."></textarea>'+
    '<button onclick="fb('+i+')">Get feedback</button><div class=fb id=f'+i+' hidden></div></div>'});
  out.innerHTML=h;window.Q=d.questions;
}
async function fb(i){
  const r=await fetch('/api/feedback',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({question:window.Q[i],answer:document.getElementById('a'+i).value})});
  const d=await r.json();const el=document.getElementById('f'+i);el.hidden=false;el.textContent=d.feedback;
}
</script>"""
