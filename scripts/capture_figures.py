"""Render versioned paper figure crops described by each metadata.json."""
import argparse, hashlib, io, json, pathlib, urllib.request
import pypdfium2 as pdfium
from PIL import Image

ROOT=pathlib.Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source-dir',type=pathlib.Path,help='Optional local cache: <id>/paper.pdf')
    parser.add_argument('--paper',help='Only capture this arXiv ID')
    args=parser.parse_args()
    for meta_path in sorted((ROOT/'papers').glob('*/metadata.json')):
        meta=json.loads(meta_path.read_text())
        if args.paper and meta['id']!=args.paper: continue
        html_figures=[f for f in meta['figures'] if f.get('kind')=='arxiv_html_figure']
        for figure in html_figures:
            dest=meta_path.parent/figure['file']
            if dest.exists():continue
            with urllib.request.urlopen(figure['source'],timeout=30) as response:data=response.read()
            if hashlib.sha256(data).hexdigest()!=figure['source_image_sha256']:raise ValueError('HTML source figure digest changed')
            dest.parent.mkdir(parents=True,exist_ok=True)
            Image.open(io.BytesIO(data)).convert('RGB').save(dest,optimize=True)
        pdf_figures=[f for f in meta['figures'] if f.get('kind')!='arxiv_html_figure']
        if not pdf_figures:continue
        cache=(args.source_dir or ROOT/'.cache')/meta['id']/'paper.pdf'
        if not cache.exists():
            cache.parent.mkdir(parents=True,exist_ok=True)
            url=f"https://arxiv.org/pdf/{meta['id']}{meta['version']}"
            req=urllib.request.Request(url,headers={'User-Agent':'dailyReading/1.0 personal research archive'})
            with urllib.request.urlopen(req,timeout=90) as response: data=response.read()
            if not data.startswith(b'%PDF'):raise ValueError(f'{url}: not a PDF')
            cache.write_bytes(data)
        sha=hashlib.sha256(cache.read_bytes()).hexdigest()
        if sha!=meta['pdf_sha256']:
            raise ValueError(f"PDF digest changed for {meta['id']}; review the version before recapturing")
        doc=pdfium.PdfDocument(str(cache))
        for figure in pdf_figures:
            page=doc[figure['page']-1]
            width,height=page.get_size()
            x0,y0,x1,y1=figure['box_pt']
            if not (0<=x0<x1<=width and 0<=y0<y1<=height):raise ValueError('Invalid crop coordinates')
            scale=3
            bitmap=page.render(scale=scale)
            full=bitmap.to_pil().convert('RGB')
            image=full.crop(tuple(round(v*scale) for v in (x0,y0,x1,y1)))
            dest=meta_path.parent/figure['file'];dest.parent.mkdir(exist_ok=True)
            image.save(dest,optimize=True)
            print(meta['id'],figure['file'],image.size)
        doc.close()

if __name__=='__main__':main()
