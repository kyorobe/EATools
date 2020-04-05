import win32com.client
import xml.etree.ElementTree as ET
import MyEAPkg


EA = win32com.client.Dispatch("EA.App")

Repository = EA.Repository
dCur = Repository.GetCurrentDiagram()

for oTmp in dCur.SelectedObjects:
    eTmp = Repository.GetElementByID(oTmp.ElementID)
    DWGTmp = MyEAPkg.DWG(eTmp, Repository, dCur)
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

"""
root = ET.fromstring(Repository.SQLQuery(
    "SELECT * \
    FROM t_object \
    WHERE Object_Type = \"%s\""
    % (FUNC.FUNCACT_TYPE)))

tree = ET.ElementTree(root)
fl = 'test.xml'
tree.write(fl)
"""
