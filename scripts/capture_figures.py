"""Render versioned paper figure crops described by each metadata.json."""
import argparse, hashlib, json, pathlib, urllib.request
import pypdfium2 as pdfium

ROOT=pathlib.Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source-dir',type=pathlib.Path,help='Optional local cache: <id>/paper.pdf')
    parser.add_argument('--paper',help='Only capture this arXiv ID')
    args=parser.parse_args()
    for meta_path in sorted((ROOT/'papers').glob('*/metadata.json')):
        meta=json.loads(meta_path.read_text())
        if args.paper and meta['id']!=args.paper: continue
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
        for figure in meta['figures']:
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
