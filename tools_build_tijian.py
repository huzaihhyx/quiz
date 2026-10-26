#!/usr/bin/env python3
# A股体检页生成器: 61-ammo合诊md → gh-pages/skill/tijian/*.html (v1·261027)
import markdown, re, os, html

AMMO = '/root/.openclaw/workspace/hhyxL/60-69-reading/61-ammo'
OUT = '/root/.openclaw/workspace/gh-pages/skill/tijian'
os.makedirs(OUT, exist_ok=True)

COMPANIES = [
    ('002315', '焦点科技', [
        ('焦点科技_七件套合诊_261026_v1.md', f'{AMMO}/基本面穿透/焦点科技_七件套合诊_261026_v1.md', '⭐ 七件套合诊(261026最新)'),
        ('焦点科技_四件套合诊_261023_v1.1.md', f'{AMMO}/基本面穿透/焦点科技_四件套合诊_261023_v1.1.md', '四件套合诊(261023·v1.1)'),
        ('焦点科技_收益判断_261023_v1.md', f'{AMMO}/基本面穿透/焦点科技_收益判断_261023_v1.md', '收益判断(261023)'),
        ('生态取证卷_002315_261023_v1.md', f'{AMMO}/生意判官/取证深化/002315/生态取证卷_002315_261023_v1.md', '生意判官·生态取证卷(261023)'),
    ]),
    ('603195', '公牛集团', [
        ('公牛集团603195_七件套合诊_261026_v1.md', f'{AMMO}/基本面穿透/公牛集团603195_七件套合诊_261026_v1.md', '⭐ 七件套合诊(261026最新)'),
        ('生态取证卷_261023_v1.md', f'{AMMO}/生意判官/取证深化/603195/生态取证卷_261023_v1.md', '生态取证卷·第一批'),
        ('生态取证卷_第二批_261023_v1.md', f'{AMMO}/生意判官/取证深化/603195/生态取证卷_第二批_261023_v1.md', '生态取证卷·第二批'),
        ('生态取证卷_第三批_261023_v1.md', f'{AMMO}/生意判官/取证深化/603195/生态取证卷_第三批_261023_v1.md', '生态取证卷·第三批'),
        ('生态取证卷_第四批_261023_v1.md', f'{AMMO}/生意判官/取证深化/603195/生态取证卷_第四批_261023_v1.md', '生态取证卷·第四批'),
    ]),
    ('001221', '悍高集团', [
        ('悍高集团001221_七件套合诊_261026_v1.md', f'{AMMO}/基本面穿透/悍高集团001221_七件套合诊_261026_v1.md', '⭐ 七件套合诊(261026)'),
    ]),
    ('603551', '奥普科技', [
        ('奥普科技603551_七件套合诊_261026_v1.md', f'{AMMO}/基本面穿透/奥普科技603551_七件套合诊_261026_v1.md', '⭐ 七件套合诊(261026)'),
    ]),
    ('000915', '华特达因', [
        ('华特达因_六件套合诊_261024_v1.md', f'{AMMO}/基本面穿透/华特达因_六件套合诊_261024_v1.md', '⭐ 六件套全诊(261024)'),
    ]),
    ('us', '美股观察', [
        ('美股前3卡_样品_苹果AAPL_261023_v1.md', f'{AMMO}/基本面穿透/美股前3卡_样品_苹果AAPL_261023_v1.md', '苹果AAPL·前3卡样品(261023)'),
        ('美股幸存池_终选合龙名单_261024_v1.md', f'{AMMO}/基本面穿透/美股幸存池_终选合龙名单_261024_v1.md', '美股幸存池·终选合龙名单(261024)'),
    ]),
]

CSS = '''body{font-family:-apple-system,BlinkMacSystemFont,'PingFang SC',sans-serif;background:#0f1626;color:#dbe4f0;margin:0;padding:14px;max-width:900px;margin:0 auto}
a{color:#7fb3e8}
.top{display:flex;align-items:center;gap:10px;margin-bottom:10px;flex-wrap:wrap}
.back{background:#1a2332;border:1px solid #2a3a55;border-radius:16px;padding:6px 14px;color:#8fa3bf;text-decoration:none;font-size:13px}
h1{font-size:20px;margin:4px 0}
.code{color:#5a6b85;font-size:13px}
.jump{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}
.jump a{background:#1a2332;border:1px solid #2a3a55;border-radius:14px;padding:5px 12px;font-size:12px;text-decoration:none}
.doc{background:#141d31;border:1px solid #22304d;border-radius:12px;padding:12px 14px;margin:14px 0}
.doc h2{font-size:16px;margin:0 0 8px;color:#fff;border-bottom:1px solid #22304d;padding-bottom:6px}
.md h1,.md h2{font-size:15px;color:#e8eef8;margin:12px 0 6px}.md h3{font-size:14px;color:#cdd8e8;margin:10px 0 5px}
.md p{font-size:13px;line-height:1.7;margin:6px 0}.md li{font-size:13px;line-height:1.7}
.md table{border-collapse:collapse;width:100%;margin:8px 0;font-size:12px;display:block;overflow-x:auto}
.md th,.md td{border:1px solid #2a3a55;padding:4px 7px;text-align:left}.md th{background:#1a2332}
.md strong{color:#ffd98a}.md hr{border:0;border-top:1px solid #22304d;margin:10px 0}
.foot{color:#5a6b85;font-size:11px;margin-top:16px}
.up{color:#e86868}.down{color:#5bd08a}'''

def md_html(path):
    txt = open(path, encoding='utf-8').read()
    return markdown.markdown(txt, extensions=['tables', 'attr_list'])

summary = {}
for code, name, docs in COMPANIES:
    nav = ' '.join(f'<a href="#d{i}">{t}</a>' for i, (_, _, t) in enumerate(docs))
    secs = ''
    first_txt = ''
    for i, (_, path, title) in enumerate(docs):
        raw = open(path, encoding='utf-8').read()
        if not first_txt:
            m = re.search(r'(总判一句话[^\n]*|总门[^\n]*|总评[^\n]*|一句话[^\n]*)', raw)
            if m:
                first_txt = re.sub(r'[*#>|]', '', m.group(1)).strip()[:90]
        secs += f'<div class="doc" id="d{i}"><h2>{html.escape(title)}</h2><div class="md">{md_html(path)}</div></div>'
    page = f'''<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} {code} · A股体检</title><style>{CSS}</style></head><body>
<div class="top"><a class="back" href="../index.html#tijian">← 工具箱</a><h1>{name} · {code}</h1></div>
<div class="code">{first_txt}</div>
<div class="jump">{nav}</div>
{secs}
<div class="foot">生成 261027 · 源档 hhyxL/61-ammo · 由build_tijian.py自动生成 · 不构成投资建议</div>
</body></html>'''
    open(f'{OUT}/{code}.html', 'w', encoding='utf-8').write(page)
    summary[code] = (name, len(docs), first_txt)

for c, (n, k, s) in summary.items():
    print(f'{c} {n} {k}件 | {s[:60]}')
print('BUILD_OK')
