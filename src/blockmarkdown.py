from enum import Enum


class BlockType(Enum):
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered"
    ORDERED = "ordered"


def block_to_blocktype(md):
    lines = md.split('\n')
    if md.startswith('#'):
        heading_level = 0
        for char in md:
            if char == '#':
                heading_level += 1
            else:
                break
            if 1 <= heading_level <= 6 and md[heading_level] == ' ':
                return BlockType.HEADING
    if md.startswith('```') and md.endswith('```'):
        return BlockType.CODE
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED
    if len(lines) > 0:
        is_ordered = True
        for i, line in enumerate(lines, 1):
            if not line.startswith(f"{i}. "):
                is_ordered = False
                break
        if is_ordered:
            return BlockType.ORDERED
    return BlockType.PARAGRAPH


def markdown_to_blocks(text):
    blocks = text.split('\n\n')
    result = []
    for block in blocks:
        strip_block = block.strip()
        if strip_block:
            result.append(strip_block)
    return result
