
def getDeepestTagList(theElement):
    elementTags = list()
    for element in theElement.iter():
        if len(element.getchildren()) == 0:
            if element.tag == 'value':
                elementTags.append(element.getparent().tag + 'Value_')
            else:
                elementTags.append(element.tag + '_')
    return  elementTags
