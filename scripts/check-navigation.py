import argparse
from pathlib import Path

import pymupdf


def check_navigation(path):
    labels = ('研究问题', '研究方法', '结果与讨论')
    with pymupdf.open(path) as document:
        if len(document) != 6:
            raise AssertionError('起步示例应有六页')
        for active, page_number in enumerate((2, 3, 4)):
            page = document[page_number]
            header = pymupdf.Rect(0, 0, page.rect.width, 20)
            spans = [span
                     for block in page.get_text('dict', clip=header, flags=0)['blocks']
                     for line in block['lines'] for span in line['spans']]
            for index, label in enumerate(labels):
                matches = [span for span in spans if span['text'] == label]
                if len(matches) != 1:
                    raise AssertionError(f'第 {page_number + 1} 页顶部缺少唯一章节名：{label}')
                span = matches[0]
                if (span['color'] == 0xFFFFFF) != (index == active):
                    raise AssertionError(f'第 {page_number + 1} 页当前章节高亮错误：{label}')
                bounds = pymupdf.Rect(span['bbox'])
                if not header.contains(bounds):
                    raise AssertionError(f'导航文字超出页眉：{label}')
                links = [link for link in page.get_links()
                         if link['from'].contains(bounds.tl + (bounds.br - bounds.tl) / 2)]
                if len(links) != 1 or links[0].get('page') != index + 2:
                    raise AssertionError(f'导航未指向对应章节首页：{label}')
                if index == active:
                    blue_boxes = [drawing for drawing in page.get_drawings()
                                  if drawing['fill'] is not None
                                  and drawing['fill'][2] > drawing['fill'][0] + 0.3
                                  and drawing['rect'].contains(bounds)]
                    if not blue_boxes:
                        raise AssertionError('当前章节缺少可见的蓝色背景')
        for page_number in (0, 1, 5):
            page = document[page_number]
            header_text = page.get_text('text', clip=pymupdf.Rect(0, 0, page.rect.width, 20))
            if any(label in header_text for label in labels):
                raise AssertionError('封面、目录或结束页出现了正文导航')
    print('顶部导航通过：三章名称、当前章节高亮、九个跳转目标及前后置页。')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='检查已构建的 Minimalist 起步示例顶部导航')
    parser.add_argument('pdf', nargs='?', type=Path,
                        default=Path(__file__).resolve().parents[1]
                        / 'example/preview/starter-minimalist.pdf')
    check_navigation(parser.parse_args().pdf)
