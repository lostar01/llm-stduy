#!/usr/bin/python

## pip install pdfminer.six

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

def extract_text_from_pdf(filename,page_numbers=None,min_line_length=1):
    """ 从 PDF 文件中（指定页码）提取文字"""
    paragraphs = []
    buffer = ''
    full_text = ''
  

    #提取全部文本
    for i, page_layout in enumerate(extract_pages(filename)):

        # 如果指定了页面范围，跳过范围外的页
        if page_numbers is not None and i not in page_numbers:
            continue
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                full_text += element.get_text() + '\n'

    # with open("/tmp/llam3.txt","a") as f:
    #    f.write(full_text)
    # 按空行分割，将文本重新组织成段落

    lines = full_text.split('\n')
    for text in lines:
        if len(text) >= min_line_length:
            buffer += (' ' + text) if not text.endswith('-') else text.strip('-')
        elif buffer:
            paragraphs.append(buffer)
            buffer = ''
    if buffer:
        paragraphs.append(buffer)

    return paragraphs



paragraphs = extract_text_from_pdf("/mnt/c/Users/lostar/Downloads/2406.08478v2.pdf",min_line_length=10)

for para in paragraphs:
    print(para+"\n")
