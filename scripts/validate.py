"""Check archival completeness, relative links and image provenance. Stdlib only."""
import json,pathlib,re,struct,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
errors=[]
catalog=json.loads((ROOT/'data/catalog.json').read_text());ids=set()
if [item['id'] for item in catalog]!=sorted(item['id'] for item in catalog):errors.append('Catalog must be sorted by arXiv ID')
for item in catalog:
    ident=item['id']
    if ident in ids:errors.append(f'Duplicate paper: {ident}')
    ids.add(ident);directory=(ROOT/item['directory']).resolve()
    if directory.parent!=ROOT/'papers' or directory.name!=f"{ident}-{item['short']}":
        errors.append(f'Paper directory must be arXiv ID then short title: {ident}')
        continue
    for name in ['README.md','metadata.json','assets/abstract-summary.png','assets/reading-card.png']:
        if not (directory/name).is_file():errors.append(f'Missing {ident}/{name}')
    meta=json.loads((directory/'metadata.json').read_text())
    if meta.get('id')!=ident or meta.get('directory')!=item['directory']:errors.append(f'Catalog/metadata mismatch: {ident}')
    if not (directory/'README.md').read_text().startswith(f"# {ident} · {item['short']}\n"):errors.append(f'Paper heading must be ID then short title: {ident}')
    for key in ['arxiv','alphaxiv','read','retrieved_at','version','figures']:
        if not meta.get(key):errors.append(f'{ident} missing {key}')
    for figure in meta['figures']:
        if not (directory/figure['file']).is_file():errors.append(f'Missing figure {ident}/{figure["file"]}')
        if figure.get('kind')=='arxiv_html_figure':
            if not figure.get('source') or not figure.get('source_image_sha256') or not figure.get('figure_number'):errors.append(f'Missing HTML figure provenance {ident}')
        elif not meta.get('pdf_sha256') or not figure.get('page') or not figure.get('box_pt') or not figure.get('source'):
            errors.append(f'Missing PDF figure provenance {ident}')
for path in ROOT.rglob('*.md'):
    if '.git' in path.parts or '.cache' in path.parts:continue
    text=path.read_text()
    # Ignore code examples and example links in templates.
    if 'templates' in path.parts:continue
    text=re.sub(r'```.*?```','',text,flags=re.S)
    for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',text):
        if re.match(r'^(https?://|mailto:|#)',target):continue
        target=target.split('#')[0]
        dest=(path.parent/target).resolve()
        if not dest.is_relative_to(ROOT) or not dest.exists():errors.append(f'{path.relative_to(ROOT)} broken local link: {target}')
for path in (ROOT/'papers').rglob('*.png'):
    data=path.read_bytes()
    if data[:8]!=b'\x89PNG\r\n\x1a\n':errors.append(f'Invalid PNG: {path}')
    else:
        w,h=struct.unpack('>II',data[16:24])
        if w<600 or h<150:errors.append(f'Image too small: {path.name} {w}x{h}')
if errors:
    print('\n'.join(errors));sys.exit(1)
print(f'OK: {len(ids)} papers, all local Markdown links, PNG dimensions and figure provenance verified')
