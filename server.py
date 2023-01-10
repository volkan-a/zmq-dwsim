"""
DWSIM server for optimization
"""
import json
import clr
import zmq

PATH = "c:\\Users\\volkan\\AppData\\Local\\DWSIM8\\"
# pylint: disable=no-member
clr.AddReference(PATH + "DWSIM.Automation.dll")
clr.AddReference(PATH + "DWSIM.Interfaces.dll")
# pylint: enable=no-member

# pylint: disable=wrong-import-position
import DWSIM

# pylint: enable=wrong-import-position


sim = DWSIM.Automation.Automation3()
fs = sim.LoadFlowsheet("three_stages.dwxmz")


def test(p_1: float, p_2: float) -> float:
    """
    calculate total compressor work with intermate pressure p1 and p2
    """
    comp1 = fs.GetFlowsheetSimulationObject("COMP1")
    comp2 = fs.GetFlowsheetSimulationObject("COMP2")
    comp1.SetPropertyValue("PROP_CO_4", p_1)
    comp2.SetPropertyValue("PROP_CO_4", p_2)
    sim.CalculateFlowsheet2(fs)
    wc1 = fs.GetFlowsheetSimulationObject("WC1").GetPropertyValue("PROP_ES_0")
    wc2 = fs.GetFlowsheetSimulationObject("WC2").GetPropertyValue("PROP_ES_0")
    wc3 = fs.GetFlowsheetSimulationObject("WC3").GetPropertyValue("PROP_ES_0")
    return wc1 + wc2 + wc3


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


while True:
    message = socket.recv()
    inp = json.loads(message)
    wtot = test(inp["p1"], inp["p2"])
    res = {"wtot": wtot}
    socket.send(bytes(json.dumps(res), "utf-8"))
