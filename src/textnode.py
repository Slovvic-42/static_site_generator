from enum import Enum

class TextType(Enum):
    PLAIN = 1
    BOLD = 2
    ITALIC = 3
    UNDERLINE = 4
    STRIKETHROUGH = 5
    CODE = 6
    ANCHOR = 7
    IMAGE_ALT_TEXT = 8

class TextNode:
    def __init__(self, text: str, text_type: TextType = TextType.PLAIN, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url  # For ANCHOR type

    # def __str__(self):
    #     return f"{self.text} ({self.text_type.name}) {self.url if self.url else ''}"
    
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url)
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    