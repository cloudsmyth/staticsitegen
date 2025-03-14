from enum import Enum


class BlockType(Enum):
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered"
    ORDERED = "ordered"


def heading_level(block):
    heading_level = 0
    for char in block:
        if char == '#':
            heading_level += 1
        else:
            break
    return heading_level


def block_to_blocktype(block):
    lines = block.split('\n')
    if block.startswith('#'):
        level = heading_level(block)
        if 1 <= level <= 6 and block[level] == ' ':
            return BlockType.HEADING
    if block.startswith('```') and block.endswith('```'):
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
