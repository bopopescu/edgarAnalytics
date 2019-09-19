
def getDeepestTagList(theElement, combinedTags, ignoreTagList):
    elementTags = list()
    for element in theElement.iter():
        if len(element.getchildren()) == 0:
            if element.tag not in ignoreTagList:
                if element.tag in combinedTags:
                    elementTags.append(element.getparent().tag + element.tag.capitalize() + '_')
                else:
                    elementTags.append(element.tag + '_')
    return elementTags


def getDeepestTagListManually(theElement, theTagList, combinedTags, ignoreTagList, skipValues = None):
    if skipValues is None or theElement.tag not in skipValues:
        theChildren = theElement.getchildren()
        if len(theChildren) > 0:
            for item in theElement.iterchildren():
                getDeepestTagListManually(item, theTagList, combinedTags, ignoreTagList, skipValues)
        else:
            if theElement.tag not in ignoreTagList:
                if theElement.tag in combinedTags:
                    theTagList.append(theElement.getparent().tag + theElement.tag.capitalize() + '_')
                else:
                    theTagList.append(theElement.tag + '_')
    return theTagList
