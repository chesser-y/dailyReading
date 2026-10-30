"""Typeset project-authored summaries; these are not alphaXiv screenshots."""
import argparse, json, pathlib
from PIL import Image,ImageDraw,ImageFont

ROOT=pathlib.Path(__file__).resolve().parents[1]
def choose_font(requested):
    candidates=[requested,'/System/Library/Fonts/STHeiti Medium.ttc','/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc']
    for path in candidates:
        if path and pathlib.Path(path).is_file():return path
    raise SystemExit('Set --font to an installed CJK font file')

def wrap(text,font,width,draw):
    lines=[];current=''
    for c in text:
        if c=='\n':lines.append(current);current='';continue
        if current and draw.textlength(current+c,font=font)>width:lines.append(current);current=c
        else:current+=c
    if current:lines.append(current)
    return lines

def render(meta,sections,path,font_path):
    width=1440;left=76;available=width-left*2
    canvas=Image.new('RGB',(width,6000),'#f5f6f7');d=ImageDraw.Draw(canvas)
    font=ImageFont.truetype(font_path,31);small=ImageFont.truetype(font_path,23)
    heading=ImageFont.truetype(font_path,33);title=ImageFont.truetype(font_path,53)
    d.rectangle((0,0,width,14),fill='#116f72');y=65
    d.text((left,y),'DAILY READING  /  '+meta['first_archived'],font=small,fill='#116f72');y+=53
    for line in wrap(meta['short'],title,available,d):d.text((left,y),line,font=title,fill='#152d39');y+=67
    d.text((left,y),f"arXiv:{meta['id']}  |  {meta['version']}  |  AI中文阅读笔记",font=small,fill='#52636c');y+=60
    for label,text in sections:
        d.line((left,y,width-left,y),fill='#c9d6d8',width=2);y+=25
        d.text((left,y),label,font=heading,fill='#116f72');y+=53
        for line in wrap(text,font,available,d):d.text((left,y),line,font=font,fill='#26353c');y+=48
        y+=32
    footer=f"来源：arxiv.org/abs/{meta['id']} · alphaxiv.org/abs/{meta['id']}"
    d.text((left,y),footer,font=small,fill='#52636c');y+=43
    d.text((left,y),'本项目自写摘要与解读的排版图；非第三方网页截图；核查程度见逐篇笔记。',font=small,fill='#52636c');y+=62
    if y>6000:raise ValueError('Card too tall')
    path.parent.mkdir(parents=True,exist_ok=True);canvas.crop((0,0,width,y)).save(path,optimize=True)
    print(path.relative_to(ROOT),width,y)

def main():
    p=argparse.ArgumentParser();p.add_argument('--font');args=p.parse_args();font=choose_font(args.font)
    for path in sorted((ROOT/'papers').glob('*/metadata.json')):
        m=json.loads(path.read_text());assets=path.parent/'assets'
        render(m,[('中文摘要 · AI改写',m['abstract']),('边界与复现条件',m['limits'])],assets/'abstract-summary.png',font)
        render(m,[('研究问题与价值',m['intro']),('输入 → 模型 → 输出',m['method']),('alphaXiv解读 · 中文提炼',m['alpha']),('思考与借鉴 · 本项目推断',m['inference'])],assets/'reading-card.png',font)

if __name__=='__main__':main()
