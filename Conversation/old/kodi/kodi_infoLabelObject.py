import kodi_json
import xbmc
import json
import inspect
import re

class InfoLabelObject:
    _Labels = []
    def __init__(self, windowId = 0, parent = None):
        self._ClassName = self.__class__.__name__
        self.Id = windowId 
        for label in dir(self):
            if(not label.startswith("_") and not inspect.ismethod(getattr(self, label))):
                self._Labels.append(self._ClassName + "." + label)

    def load(self):
        labelResults = kodi_json.kodi_execute_json({"method" : "XBMC.GetInfoLabels", "params" : { "labels" : self._Labels }})
        self.setProperties(self._Labels, labelResults, self._ClassName)

    def setProperties(self, labels, labelResults, prefix, itemType = None):
        for label in labels:
            value = labelResults['result'][label]

            regexResult = re.match('(([\w.]*)\(([0-9]*)\).(\w*))', label)

            xbmc.log(msg = "matching label: " + label)

            if(regexResult is not None):
                # Array thingy
                fieldName = regexResult.group(2).replace(self._ClassName + '.', '')
                fieldIndex = int(regexResult.group(3))
                fieldProperty = regexResult.group(4)

                fieldList = getattr(self, fieldName)

                xbmc.log(msg="type: " + str(fieldList))

                if(len(fieldList) <= fieldIndex):
                    fieldList.append(itemType())
                
                setattr(fieldList[fieldIndex], fieldProperty, value)

            else:
                fieldName = label.replace(prefix + '.', '')
                attr = getattr(self, fieldName)

                if(isinstance(attr, int)):
                    if(len(value) == 0):
                        value = '-1'
                    setattr(self, fieldName, int(value))
                elif(not isinstance(attr, list) and not inspect.ismethod(attr)):
                    setattr(self, fieldName, value)

        return self

            #xbmc.log(msg="label: " + label + " value: " + value)

    def loadItems(self, infoLabel, numberOfItems, listField, itemType):
        xbmc.log(msg = "loadItems(" + infoLabel + ", " + str(numberOfItems) + ", " + str(listField) + ", " + str(itemType) + ")")

        listField = []
        labels = []

        for i in range(0, numberOfItems):
            className = self.__class__.__name__ + "." + infoLabel + "(" + str(i) + ")"

            xbmc.log(msg="className: " + className)

            for label in dir(itemType):
                xbmc.log(msg = "dir label: " + label)
                if(not label.startswith("_") and not inspect.ismethod(getattr(itemType, label))):
                    labels.append(className + "." + label)

        labelResults = kodi_json.kodi_execute_json({"method" : "XBMC.GetInfoLabels", "params" : { "labels" : labels }})
        self.setProperties(labels, labelResults, infoLabel, itemType)


        #if(getattr(self, "_IndexMapping") is not None)
        #    mapping = getattr(self, "_IndexMapping")
        #    for key, value in mapping.iteritems():
        #        countField = getattr(self, value)['CountField']
        #        listType = getattr(self, value)['Type']
        #        listField = getattr(self, key)

        #        for i in range(0, countField):
        #            labels.append(className + "." + listField.__name__ + "(" + str(i) + ")")

