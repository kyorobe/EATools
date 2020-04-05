import win32com.client
from .FUNC import FUNC, isFunc


class DWG:
    DWG_TYPE = "Boundary"

    def __new__(cls, element, repository, diagram):
        if isDWG(element) and \
                repository.ObjectType == 2 and diagram.ObjectType == 8:
            return super().__new__(cls)
        else:
            return None

    def __init__(self, element, repository, diagram):
        self.eObj = element
        self.dObj = diagram.GetDiagramObjectByID(element.ElementID, "")
        self.FUNCs = {}
        self.__searchFuncs(repository, diagram)

    def __str__(self):
        lTmp = []
        for tmp in self.FUNCs.values():
            lTmp.append("\t+ %s" % (tmp.eObj.Name))
        return "%s\t\n%s" \
            % (self.eObj.Name, "\n".join(lTmp))

    def __searchFuncs(self, repository, diagram):
        for oFunc in diagram.DiagramObjects:
            eFunc = repository.GetElementByID(oFunc.ElementID)
            if isFunc(eFunc):
                FUNCTmp = FUNC(eFunc, repository, diagram)
                if self.dObj.Left < FUNCTmp.posx < self.dObj.Right and \
                        self.dObj.Bottom < FUNCTmp.posy < self.dObj.Top:
                    FUNCTmp.DWG = self
                    self.FUNCs[eFunc.ElementID] = FUNCTmp


def isDWG(element):
    return element.Type == DWG.DWG_TYPE


EA = win32com.client.Dispatch("EA.App")

Repository = EA.Repository
dCur = Repository.GetCurrentDiagram()

for oTmp in dCur.SelectedObjects:
    eTmp = Repository.GetElementByID(oTmp.ElementID)
    DWGTmp = DWG(eTmp, Repository, dCur)
    print("----")
    print("DWG:")
    print(DWGTmp)
    if DWGTmp is not None:
        print("----")
        print("FUNC:")
        for v in DWGTmp.FUNCs.values():
            print(v)
            if v is not None:
                print("----")
                print("ACT:")
                for vv in v.Acts.values():
                    print(vv)
