class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        res_string = ""
        if self.props:
            for prop in self.props:
                res_string += f' {prop}="{self.props[prop]}"'
        return res_string
    
    def __repr__(self):
        return f"HTMLNode(tag='{self.tag}', value='{self.value}', children={self.children}, props='{self.props_to_html()}')"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if not self.value:
            return f"<{self.tag}{self.props_to_html()}>"
            #raise ValueError
        if not self.tag:
            return f"{self.value}"
        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        print(f"LeafNode(tag={self.tag}, value={self.value}, props={super().props_to_html()})")

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, props=props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Missing tag")
        if not self.children:
            raise ValueError("Missing child nodes")
        
        children_html = ""
        for child in self.children:
            if child is not None:
                children_html += child.to_html()

        return f"<{self.tag}{super().props_to_html()}>{children_html}</{self.tag}>"