# Builds api/_kb.js from the recruiter view + case-study pages + facts.md.  Run: python3 tools/build_kb.py
import re,html,glob,os,json
def txt(h):
    h=re.sub(r'(?s)<(script|style|svg|head)[^>]*>.*?</\1>','',h)
    h=re.sub(r'<(br|/div|/p|/li|/h\d|/section|/tr)[^>]*>','\n',h);h=re.sub(r'<[^>]+>',' ',h);h=html.unescape(h)
    h=re.sub(r'[ \t]+',' ',h);return re.sub(r'\n\s*\n+','\n',h).strip()
s=open('index.html').read()
i=s.find('<div class="pp" id="pp">');resume=txt(s[i:s.find('<div id="grain">')])
parts=[open('tools/facts.md').read().strip(),'## RESUME (recruiter view)\n'+resume]
for f in sorted(glob.glob('work/*/index.html')):
    n=f.split('/')[1];t=txt(open(f).read())
    parts.append('## CASE STUDY: %s (page: work/%s/)\n%s'%(n,n,t[:9000]))
kb='\n\n'.join(parts)
open('api/_kb.js','w').write('module.exports='+json.dumps(kb)+';\n')
print(len(kb),'chars')
