from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    # Underscore?
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"