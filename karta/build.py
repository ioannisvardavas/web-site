import base64, urllib.parse, pathlib
U = pathlib.Path('/mnt/user-data/uploads/Desktop')
b64 = lambda p: base64.b64encode(pathlib.Path(p).read_bytes()).decode()

B_LEFKO = (U/'brand/sima-B/B-lefko.svg').read_text().strip()
B_ICON = urllib.parse.quote(B_LEFKO.replace('#ffffff', '#1d1b4f'))
B_INLINE = B_LEFKO.replace('<svg ', '<svg aria-hidden="true" ').replace('id="g"', 'id="bg"').replace('url(#g)', 'url(#bg)')

def ic(path, fill=False, extra=''):
    a = 'fill="currentColor"' if fill else 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
    return f'<svg viewBox="0 0 24 24" {a} aria-hidden="true" {extra}>{path}</svg>'

R = {
 'B_SVG': B_INLINE,
 'B_ICON': B_ICON,
 'FOTO': b64('/home/claude/karta/foto.jpg'),
 'MAN_GR': b64(U/'brand/fonts/manrope-greek.woff2'),
 'MAN_LA': b64(U/'brand/fonts/manrope-latin.woff2'),
 'INT_GR': b64(U/'brand/fonts/inter-greek.woff2'),
 'INT_LA': b64(U/'brand/fonts/inter-latin.woff2'),
 'CAL': 'https://cal.com/ioannis-vardavas-0yon6x/30min',
 'CAL_SVG': ic('<rect x="3" y="4.5" width="18" height="16" rx="3"/><path d="M3 9.5h18M8 2.5v4M16 2.5v4"/>'),
 'I_FAM': ic('<circle cx="9" cy="7" r="3"/><circle cx="17" cy="9" r="2.3"/><path d="M3.5 20c0-3.3 2.5-6 5.5-6s5.5 2.7 5.5 6M14.5 20c.2-2.6 1.4-4.6 3-4.6s2.8 2 3 4.6"/>'),
 'I_BIZ': ic('<rect x="3" y="7" width="18" height="13" rx="2.5"/><path d="M8.5 7V5a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v2M3 12.5h18"/>'),
 'I_POL': ic('<path d="M12 3l7.5 3v5.5c0 4.6-3.2 8.3-7.5 9.5-4.3-1.2-7.5-4.9-7.5-9.5V6z"/><path d="M8.8 12l2.2 2.2 4.4-4.4"/>'),
 'I_OK': ic('<circle cx="12" cy="12" r="9"/><path d="M8 12.3l2.6 2.6L16.2 9.3"/>'),
 'I_TEL': ic('<path d="M5 4h3.5l1.6 4.2-2.2 1.4a11 11 0 0 0 6.5 6.5l1.4-2.2L20 15.5V19a2 2 0 0 1-2.2 2A16.5 16.5 0 0 1 3 6.2 2 2 0 0 1 5 4z"/>'),
 'I_WA': ic('<path d="M12 2.2a9.7 9.7 0 0 0-8.4 14.6L2.3 21.7l5-1.3A9.7 9.7 0 1 0 12 2.2zm0 17.7a8 8 0 0 1-4.1-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8 8 0 1 1 12 19.9zm4.4-6c-.2-.1-1.4-.7-1.7-.8-.2-.1-.4-.1-.5.1l-.8 1c-.1.2-.3.2-.5.1a6.6 6.6 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5a.9.9 0 0 0-.7.3 2.8 2.8 0 0 0-.9 2.1 5 5 0 0 0 1 2.6 11.3 11.3 0 0 0 4.4 3.9c1.6.7 2.3.8 3.1.6.5-.1 1.4-.6 1.6-1.2.2-.6.2-1 .1-1.2l-.4-.3z"/>', fill=True),
 'I_VI': ic('<path d="M12 2.5c-4.6 0-8.3 2.6-8.3 8 0 2.9 1 5 2.8 6.3v3.7l3-2.1c.8.2 1.6.2 2.5.2 4.6 0 8.3-2.6 8.3-8s-3.7-8.1-8.3-8.1z"/><path d="M9.3 7.6c.4-.3.9-.2 1.1.2l.7 1.2c.2.4.1.8-.2 1l-.5.4c.4 1.1 1.3 2 2.4 2.5l.4-.5c.3-.3.7-.4 1-.2l1.2.7c.4.2.5.7.2 1.1-.6.8-1.6 1.1-2.5.7a8 8 0 0 1-4.6-4.6c-.4-.9-.1-1.9.8-2.5z" fill="currentColor" stroke="none"/>'),
}
import re
T = pathlib.Path('/home/claude/karta/template.html').read_text()
for idx, out in ((1, 'index.html'), (0, 'g/index.html')):   # 1 = πληθυντικός (άγνωστος), 0 = ενικός (γνωστός, «Γεια σου»)
    s = re.sub(r'\[\[(.*?)\|(.*?)\]\]', lambda m: m.group(idx + 1 if idx == 1 else 1), T, flags=re.S)
    for k, v in R.items():
        s = s.replace('{{' + k + '}}', v)
    assert '{{' not in s and '[[' not in s
    o = pathlib.Path('/home/claude/karta') / out; o.parent.mkdir(exist_ok=True); o.write_text(s)
    print(out, len(s)//1024, 'KB')
