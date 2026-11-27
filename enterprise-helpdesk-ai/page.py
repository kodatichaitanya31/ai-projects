"""Dashboard HTML (Jinja template)."""

PAGE = """<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>Enterprise Helpdesk AI</title>
<style>
body{font-family:system-ui,sans-serif;max-width:1000px;margin:1.5rem auto;padding:0 1rem;color:#1f2937}
h1{margin-bottom:.2rem}.sub{color:#6b7280;margin-top:0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:.7rem;margin:1rem 0}
.stat{border:1px solid #e5e7eb;border-radius:10px;padding:.8rem}.stat b{font-size:1.6rem;display:block}
form,.card{border:1px solid #e5e7eb;border-radius:10px;padding:1rem;margin:1rem 0}
input,textarea{width:100%;box-sizing:border-box;padding:.5rem;margin:.3rem 0}
button{background:#2563eb;color:#fff;border:0;padding:.45rem .9rem;border-radius:6px;cursor:pointer}
table{width:100%;border-collapse:collapse}td,th{padding:.5rem;border-bottom:1px solid #e5e7eb;text-align:left;vertical-align:top}
.HIGH{color:#b91c1c;font-weight:700}.MEDIUM{color:#b45309;font-weight:600}.LOW{color:#047857}
.hint{background:#f0fdf4;border-radius:6px;padding:.5rem;margin-top:.4rem;font-size:.9rem}
</style>
<h1>Enterprise Helpdesk AI</h1><p class=sub>AI-routed tickets, SLA priorities and instant knowledge-base answers.</p>
<div class=grid>
<div class=stat><b>{{ stats.total }}</b>Total tickets</div>
{% for p in ['HIGH','MEDIUM','LOW'] %}<div class=stat><b class={{p}}>{{ stats.open_by_priority.get(p,0) }}</b>Open {{p}}</div>{% endfor %}
{% for d,n in stats.open_by_dept.items() %}<div class=stat><b>{{ n }}</b>Open {{ d }}</div>{% endfor %}
</div>
<form method=post action=/tickets>
<b>New ticket</b><input name=subject placeholder="Subject" required>
<textarea name=body rows=3 placeholder="Describe the issue" required></textarea>
<button>Submit &amp; auto-triage</button></form>
<h3>Open tickets</h3>
<table><tr><th>#</th><th>Ticket</th><th>Dept</th><th>Priority</th><th>SLA</th><th></th></tr>
{% for t in tickets %}<tr><td>{{ t.id }}</td>
<td><b>{{ t.subject }}</b><br>{{ t.body }}<div class=hint><b>Suggested reply:</b> {{ t.suggestion }}</div></td>
<td>{{ t.dept }}<br><small>{{ (t.confidence*100)|int }}% sure</small></td>
<td class={{ t.priority }}>{{ t.priority }}</td><td>{{ t.sla_hours }}h</td>
<td><form method=post action=/tickets/{{ t.id }}/resolve style="border:0;padding:0;margin:0"><button>Resolve</button></form></td></tr>
{% else %}<tr><td colspan=6>No open tickets.</td></tr>{% endfor %}</table>"""
