from .REQ import REQ, isReq


class ACT:
    ACT_TYPE = "Activity"
    ACT_REQ_CON_TYPE = "Dependency"
    ACT_REQ_CON_STEREOTYPE = "refine"

    def __new__(cls, element, repository):
        if isAct(element) and \
                repository.ObjectType == 2:
            return super().__new__(cls)
        else:
            return None

    def __init__(self, element, repository):
        self.eObj = element
        self.FUNC = None
        self.REQs = {}
        self.__searchReqs(repository)

    def __str__(self):
        lTmp = []
        for tmp in self.REQs.values():
            lTmp.append("\t+ %s\t:%s" % (tmp.ReqID, tmp.Req))
        return "%s\t->\t%s\n%s" \
            % (self.FUNC.eObj.Name, self.eObj.Name, "\n".join(lTmp))

    def __searchReqs(self, repository):
        for tmp in self.eObj.Connectors:
            if isActReqCon(tmp):
                eReq = repository.GetElementByID(tmp.SupplierID)
                if isReq(eReq):
                    self.REQs[eReq.ElementID] = REQ(eReq)
                    self.REQs[eReq.ElementID].Act = self


def isAct(e):
    return e.Type == ACT.ACT_TYPE


def isActReqCon(e):
    return e.Type == ACT.ACT_REQ_CON_TYPE and \
        e.Stereotype == ACT.ACT_REQ_CON_STEREOTYPE
