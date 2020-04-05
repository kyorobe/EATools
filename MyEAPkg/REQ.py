class REQ:
    REQ_TYPE = "Requirement"
    REQ_STEREOTYPE = "USDM要求"

    def __new__(cls, element):
        if isReq(element):
            return super().__new__(cls)
        else:
            return None

    def __init__(self, element):
        self.eObj = element
        self.ReqID = element.Alias
        self.Req = element.Name
        self.Note = element.Notes
        self.Act = None


def isReq(e):
    return e.Type == REQ.REQ_TYPE and e.Stereotype == REQ.REQ_STEREOTYPE
