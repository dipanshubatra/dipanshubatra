from pathlib import Path
from html import escape
import xml.etree.ElementTree as ET
root=Path('/home/dipanshu/dbprofile'); out=root/'assets/ui'; out.mkdir(exist_ok=True)
BG='#0d1117'; PANEL='#111827'; LINE='#263244'; TEXT='#e5e7eb'; MUTED='#9ca3af'; BLUE='#60a5fa'; TEAL='#5eead4'; GOLD='#d6b36a'
def svg(name,w,h,body):
 (out/name).write_text(f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><style>text{{font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif}}.mono{{font-family:'SFMono-Regular',Consolas,monospace}}</style>{body}</svg>""")
# Quiet editorial hero
body=f'''<rect width="1000" height="250" rx="16" fill="{BG}"/><rect x="1" y="1" width="998" height="248" rx="15" fill="none" stroke="{LINE}"/>
<rect x="40" y="39" width="3" height="171" rx="1.5" fill="{BLUE}"/>
<text class="mono" x="66" y="62" font-size="12" letter-spacing="2" fill="{BLUE}">BACKEND ENGINEERING · JAVA / SPRING</text>
<text x="64" y="119" font-size="48" font-weight="700" letter-spacing="-1.5" fill="{TEXT}">Dipanshu Batra</text>
<text x="66" y="153" font-size="18" fill="{MUTED}">Building reliable backend systems, APIs and distributed services.</text>
<text class="mono" x="66" y="194" font-size="12" fill="#7f8b9b">JAVA 17/21   ·   SPRING BOOT   ·   REDIS   ·   POSTGRESQL</text>
<g transform="translate(824 76)" fill="none" stroke="{LINE}" stroke-width="1.5"><rect x="0" y="0" width="126" height="100" rx="12"/><rect x="16" y="16" width="94" height="18" rx="4" stroke="{BLUE}"/><path d="M16 49H110M16 64H88M16 79H98"/><circle cx="104" cy="25" r="3" fill="{BLUE}" stroke="none"/></g>
<text class="mono" x="887" y="198" text-anchor="middle" font-size="9" letter-spacing="1.2" fill="{MUTED}">DESIGN · BUILD · SHIP</text>'''
svg('hero.svg',1000,250,body)
# Static terminal panel: calm, readable, no looping typewriter
body=f'''<rect width="1000" height="190" rx="14" fill="{PANEL}" stroke="{LINE}"/><path d="M1 43H999" stroke="{LINE}"/><circle cx="25" cy="22" r="4" fill="#64748b"/><circle cx="41" cy="22" r="4" fill="#64748b"/><circle cx="57" cy="22" r="4" fill="#64748b"/><text class="mono" x="500" y="27" text-anchor="middle" font-size="11" fill="{MUTED}">dipanshu@engineering ~/profile</text>
<text class="mono" x="28" y="76" font-size="13" fill="{TEAL}">$ whoami</text><text class="mono" x="150" y="76" font-size="13" fill="{TEXT}">Backend developer focused on Java and distributed systems</text>
<text class="mono" x="28" y="108" font-size="13" fill="{TEAL}">$ building</text><text class="mono" x="150" y="108" font-size="13" fill="{TEXT}">NovaMart · microservices e-commerce / CronVault · multi-tenant scheduler</text>
<text class="mono" x="28" y="140" font-size="13" fill="{TEAL}">$ engineering</text><text class="mono" x="150" y="140" font-size="13" fill="{TEXT}">Concurrency · authentication · caching · payments · observability</text>
<text class="mono" x="28" y="172" font-size="13" fill="{TEAL}">$ status</text><text class="mono" x="150" y="172" font-size="13" fill="{TEXT}">Backend Developer Intern @ Enginow · open to SDE opportunities</text>'''
svg('terminal.svg',1000,190,body)
# Metric strip
items=[('7×','Hackathon wins'),('#4','ECSoC 2026 · global rank'),('8','NovaMart services'),('16+','Open-source projects')]
body=f'<rect width="1000" height="142" rx="14" fill="{BG}" stroke="{LINE}"/>'
for i,(n,l) in enumerate(items):
 x=18+i*250
 if i: body+=f'<path d="M{x} 27V115" stroke="{LINE}"/>'
 body+=f'<text x="{x+22}" y="76" font-size="34" font-weight="700" fill="{TEXT}">{n}</text><text x="{x+22}" y="101" font-size="12" fill="{MUTED}">{escape(l)}</text>'
svg('metrics.svg',1000,142,body)
# Microservices diagram: 8 components, clean boundaries
nodes=[('IDENTITY','Auth · JWT · OAuth2',70,130),('CATALOG','Products · Search',300,130),('INVENTORY','Stock · Reservations',530,130),('CART','Cart · Expiry',760,130),('ORDER','Checkout · Lifecycle',185,230),('PAYMENT','Cashfree · Webhooks',415,230),('NOTIFICATION','Email · Events',645,230)]
body=f'<rect width="1000" height="310" rx="14" fill="{BG}" stroke="{LINE}"/><text class="mono" x="28" y="27" font-size="10" letter-spacing="1.5" fill="{MUTED}">NOVAMART · SERVICE BOUNDARIES</text>'
body+=f'<rect x="365" y="48" width="270" height="54" rx="9" fill="#172235" stroke="{BLUE}"/><text x="500" y="71" text-anchor="middle" font-size="14" font-weight="700" fill="{TEXT}">API GATEWAY</text><text class="mono" x="500" y="88" text-anchor="middle" font-size="9" fill="{MUTED}">ROUTING · SECURITY · TRACE ID</text>'
for name,sub,x,y in nodes:
 cx=x+82
 body+=f'<path d="M500 102V115H{cx}V{y}" fill="none" stroke="{LINE}" stroke-width="1.4"/>'
for name,sub,x,y in nodes:
 body+=f'<rect x="{x}" y="{y}" width="165" height="58" rx="8" fill="{PANEL}" stroke="{LINE}"/><text class="mono" x="{x+13}" y="{y+22}" font-size="10" font-weight="700" fill="{BLUE}">{name}</text><text x="{x+13}" y="{y+42}" font-size="10" fill="{MUTED}">{escape(sub)}</text>'
body+=f'<text x="28" y="294" font-size="9" fill="{MUTED}">Conceptual overview of NovaMart service boundaries; not a runtime dependency or traffic-flow trace.</text>'
svg('architecture.svg',1000,310,body)
# Historical JMeter snapshot, no fake live telemetry
body=f'<rect width="1000" height="222" rx="14" fill="{BG}" stroke="{LINE}"/><text class="mono" x="28" y="29" font-size="10" letter-spacing="1.5" fill="{MUTED}">LOAD TEST · REDIS CACHE COMPARISON</text><text x="28" y="65" font-size="21" font-weight="650" fill="{TEXT}">Throughput under the same workload</text><text x="28" y="87" font-size="11" fill="{MUTED}">1,000 virtual users · 50 loops · 50,000 requests</text>'
for y,label,val,width,color in [(125,'CACHE ENABLED','~1,808 req/s',620,BLUE),(169,'CACHE DISABLED','~100 req/s',34,'#64748b')]:
 body+=f'<text class="mono" x="28" y="{y+5}" font-size="10" fill="{MUTED}">{label}</text><rect x="220" y="{y-11}" width="620" height="18" rx="4" fill="#1b2533"/><rect x="220" y="{y-11}" width="{width}" height="18" rx="4" fill="{color}"/><text x="860" y="{y+4}" font-size="13" font-weight="650" fill="{TEXT}">{val}</text>'
body+=f'<text x="28" y="207" font-size="10" fill="{MUTED}">Cached run: 361 ms average response · 0% errors · historical measurement, not live telemetry.</text>'
svg('performance.svg',1000,222,body)
# Achievement cards, still and consistent
wins=[('WINNER','TechFrontier 2025','IIIT Delhi'),('WINNER','Hackastra','NIT Durgapur'),('WINNER','Mukand Utsav 2K26','National-level'),('WINNER','HackOrbit 2K26','National-level'),('WINNER','Ideathon 2K26','JMIT Radaur'),('WINNER','Shark Tank','Pitch competition'),('FINALIST','ByteVerse','Hackathon'),('GLOBAL RANK 4','ECSoC 2026','Tier 1 Developer')]
body=f'<rect width="1000" height="218" rx="14" fill="{BG}" stroke="{LINE}"/>'
for i,(tag,title,sub) in enumerate(wins):
 x=18+(i%4)*246;y=16+(i//4)*96;c=GOLD if tag=='WINNER' else BLUE
 body+=f'<rect x="{x}" y="{y}" width="230" height="82" rx="9" fill="{PANEL}" stroke="{LINE}"/><rect x="{x}" y="{y}" width="3" height="82" rx="1.5" fill="{c}"/><text class="mono" x="{x+15}" y="{y+23}" font-size="9" letter-spacing="1" fill="{c}">{escape(tag)}</text><text x="{x+15}" y="{y+47}" font-size="14" font-weight="650" fill="{TEXT}">{escape(title)}</text><text x="{x+15}" y="{y+66}" font-size="10" fill="{MUTED}">{escape(sub)}</text>'
svg('wins.svg',1000,218,body)
# Static skills rows, no scrolling marquee
rows=[('BACKEND',['Java 17/21','Spring Boot 3','Spring Security','Hibernate / JPA','REST APIs','JWT · OAuth2 · RBAC']),('DATA & INFRA',['PostgreSQL','MySQL','Redis','Docker','GitHub Actions','Maven']),('ENGINEERING',['Distributed systems','Concurrency','Rate limiting','Circuit breakers','JUnit 5','JMeter'])]
body=f'<rect width="1000" height="174" rx="14" fill="{BG}" stroke="{LINE}"/>'
for i,(label,tags) in enumerate(rows):
 y=37+i*48;body+=f'<text class="mono" x="25" y="{y+4}" font-size="9" letter-spacing="1" fill="{MUTED}">{escape(label)}</text>';x=190
 for tag in tags:
  width=len(tag)*7+25
  body+=f'<rect x="{x}" y="{y-14}" width="{width}" height="26" rx="6" fill="{PANEL}" stroke="{LINE}"/><text x="{x+width/2}" y="{y+3}" text-anchor="middle" font-size="10" fill="{TEXT}">{escape(tag)}</text>';x+=width+10
svg('marquee.svg',1000,174,body)
# Neutral section title assets for remaining legacy references
for key,label in [('about','About'),('ecsoc',"ECSoC '26"),('projects','Selected Projects'),('stack','Technical Skills'),('wins','Achievements'),('journey','Experience & Journey'),('oss','Open Source'),('stats','GitHub Activity'),('architecture','System Architecture'),('performance','Performance Testing')]:
 body=f'<text x="0" y="27" font-size="22" font-weight="650" fill="{TEXT}">{escape(label)}</text><path d="M0 42H1000" stroke="{LINE}"/><path d="M0 42H72" stroke="{BLUE}" stroke-width="2"/>'
 svg(f't-{key}.svg',1000,48,body)
for p in out.glob('*.svg'):
 try: ET.parse(p)
 except Exception as e: print('INVALID',p.name,e)
print('Premium assets generated; validation report above')
