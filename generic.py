# Formats the string to follow a paragraph (grammatical) format.
def paragraphCase(msg: str):
    return '. '.join([x.strip().capitalize() for x in msg.split('.')])

def titleCase(title: str):
    return ' '.join([x.strip().capitalize() for x in title.split(' ')])