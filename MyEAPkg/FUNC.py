import win32com.client
import xml.etree.ElementTree as ET
from .ACT import ACT, isAct


class FUNC:
    FUNC_TYPE = "Part"
    FUNCACT_TYPE = "ActivityPartition"

    def __new__(cls, element, repository, diagram):
        if isFunc(element) and \
                repository.ObjectType == 2 and diagram.ObjectType == 8:
            return super().__new__(cls)
        else:
            return None

    def __init__(self, element, repository, diagram):
        self.eObj = element
        self.dObj = diagram.GetDiagramObjectByID(element.ElementID, "")
        [x, y] = self.__cal_center()
        self.posx = x
        self.posy = y
        self.DWG = None
        self.eObjCls = repository.GetElementByGuid(self.eObj.MiscData(0))
        self.Acts = {}
        self.__searchActs(repository, diagram)

    def __str__(self):
        lTmp = []
        for tmp in self.Acts.values():
            lTmp.append("\t+ %s" % tmp.eObj.Name)
        return "%s\t->\t%s\n%s" \
            % (self.DWG.eObj.Name, self.eObj.Name, "\n".join(lTmp))

    def __cal_center(self):
        x = self.dObj.Left - (self.dObj.Left - self.dObj.Right) / 2
        y = self.dObj.Bottom + (self.dObj.Top - self.dObj.Bottom) / 2
        return [x, y]

    def __searchActs(self, repository, diagram):
        root = ET.fromstring(Repository.SQLQuery(
            "SELECT Object_ID \
            FROM t_object \
            WHERE Object_Type = \"%s\" AND Classifier = %d"
            % (FUNC.FUNCACT_TYPE, self.eObjCls.ElementID)))
        for c in root.findall(".//Object_ID"):
            eParti = Repository.GetElementByID(c.text)
            for eTmp in eParti.Elements:
                if isAct(eTmp):
                    self.Acts[eTmp.ElementID] = ACT(eTmp, repository)
                    self.Acts[eTmp.ElementID].FUNC = self


def isFunc(element):
    return element.Type == FUNC.FUNC_TYPE


EA = win32com.client.Dispatch("EA.App")

Repository = EA.Repository
dCur = Repository.GetCurrentDiagram()

for oTmp in dCur.SelectedObjects:
    eTmp = Repository.GetElementByID(oTmp.ElementID)

    print(FUNC(eTmp, Repository, dCur))
