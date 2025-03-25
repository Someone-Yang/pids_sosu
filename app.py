import tkinter as tk
import canvas
import asyncio

# 主窗口
def mainWindow():
  global root
  root = tk.Tk()

  root.geometry("1920x480")
  root.overrideredirect(True)

  global baseCanvas
  baseCanvas = tk.Canvas(root, width=1920, height=480, bg='white')
  baseCanvas.pack()

  global logoImage
  logoImage = tk.PhotoImage(file = "common/logo.gif")

# 示例信息
def loadStations():
  global stations
  global transferLines
  transferLines = {
    "1":
    {
      "name":"1号线",
      "name_eng":"Line 1",
      "display":"1",
      "color":"#854109"
    },
    "2":
    {
      "name":"2号线",
      "name_eng":"Line 2",
      "display":"2",
      "color":"#ab15cd"
    }
  }
  stations = [
    {"name":"邮电大学","name_eng":"University of Posts & Telecommunications","name_eng_display":"University of Posts\n& Telecommunications","transfer":[],"doors":0},
    {"name":"工会","name_eng":"Gonghui","name_eng_display":"Gong hui","transfer":[],"doors":0},
    {"name":"胡罗贝","name_eng":"Huluobei","name_eng_display":"Hu luo bei","transfer":[],"doors":0},
    {"name":"溪口","name_eng":"Xikou","name_eng_display":"Xi kou","transfer":[],"doors":0},
    {"name":"小桥","name_eng":"Xiaoqiao","name_eng_display":"Xiao qiao","transfer":["1","2"],"doors":0},
    {"name":"知识村","name_eng":"Zhishicun","name_eng_display":"Zhi shi cun","transfer":[],"doors":0},
    {"name":"雪村","name_eng":"Xuecun","name_eng_display":"Xue cun","transfer":[],"doors":0},
    {"name":"福瑞大道","name_eng":"Furui Blvd.","transfer":["2"],"doors":0},
    {"name":"前行路","name_eng":"Qianxing Rd.","transfer":[],"doors":0},
    {"name":"中山公园","name_eng":"Zhongshan Park","transfer":[],"doors":0},
  ]

  global nextStation
  nextStation = 4
  # 到站状态
  global nextStationStatus
  nextStationStatus = 0

  global terminus
  terminus = stations[len(stations) - 1]

# 主线路信息
def printMain():
  global logoImage
  global terminus
  global stations
  global stationDes
  global stationDesStatus
  global stationDesEng
  global transferLines
  baseCanvas.create_image(50, 60, anchor=tk.W, image=logoImage)
  baseCanvas.create_text(400, 60, text="测试线路", font=('黑体', 20),anchor="w")
  baseCanvas.create_text(700, 60, text=f"开往：{terminus['name']}", font=('黑体', 20),anchor="sw")
  baseCanvas.create_text(700, 60, text=f"Terminus:{terminus['name_eng']}", font=('Arial', 16),anchor="nw")
  if stations[nextStation].get('name_eng_display'):
    targetEngDisplay = stations[nextStation]['name_eng_display']
  else:
    targetEngDisplay = stations[nextStation]['name_eng']
  if nextStationStatus == 0:
    targetNextDisplay = "下一站："
    targetNextDisplayEng = "Next Station:"
  else:
    targetNextDisplay = "当前站："
    targetNextDisplayEng = "Current Station:"
  targetNextDisplay += stations[nextStation]['name']
  targetNextDisplayEng += targetEngDisplay
  baseCanvas.create_text(1100, 60, text=targetNextDisplay, font=('黑体', 20),anchor="sw")
  baseCanvas.create_text(1100, 60, text=targetNextDisplayEng, font=('Arial', 16),anchor="nw")

  stationDes = ""
  stationDesEng = ""
  if nextStationStatus == 0:
    stationDes += "下一站"
    stationDesEng += "The next station is "
  else:
    stationDes += "当前站"
    stationDesEng += "This station is "

  if nextStation == len(stations) - 1:
    stationDes += "是本次列车的终点站"
    stationDesEng += "the terminal station "

  stationDes += stations[nextStation]['name']
  stationDesEng += stations[nextStation]['name_eng']

  if stations[nextStation]['transfer']:
    stationDes += "，可换乘"
    stationDesEng += ". Transfer to "
    textTransferLeft = len(stations[nextStation]['transfer'])
    for tline in stations[nextStation]['transfer']:
      stationDes += transferLines[tline]['name']
      stationDesEng += transferLines[tline]['name_eng']
      textTransferLeft -= 1
      if textTransferLeft != 0:
        stationDes += "、"
        stationDesEng += ", "
  stationDes += "，开"
  stationDesEng += ". Doors open on the "
  if stations[nextStation]['doors'] == 0:
    stationDes += "左"
    stationDesEng += "left"
  else:
    stationDes += "右"
    stationDesEng += "right"
  stationDes += "侧车门。"
  stationDesEng += "."
  stationDesStatus = True
  root.update()

def printLine():
  global nsashow
  nsashow = False
  global printEach
  global printArrow
  global nextStationLoc
  global nextStationArrowLoc
  global stations
  global transferLines
  printSta = 0
  printLoc = 60
  printEach = (1920 - printLoc - printLoc - 432)/((len(stations) - 1)*2)
  printArrow = (printEach - 16) / 2
  nextStationLoc = 0
  nextStationArrowLoc = 0
  for station in stations:
    if printSta < nextStation:
      targetTextColor = "grey"
    elif printSta >= nextStation:
      targetTextColor = "black"
    baseCanvas.create_text(printLoc, 300, text=station['name'], font=('黑体', 22), angle=45, anchor=tk.SW, fill=targetTextColor)
    if station.get('name_eng_display'):
      targetEngDisplay = station['name_eng_display']
    else:
      targetEngDisplay = station['name_eng']
    baseCanvas.create_text(printLoc, 300, text=targetEngDisplay, font=('Arial', 14), angle=45, anchor=tk.NW, fill=targetTextColor)
    if printSta < nextStation:
      canvas.draw_gradient_ball(baseCanvas,printLoc,340,22,(0xFF, 0xFF, 0xFF),(0xAA, 0xAA, 0xAA),10)
    elif printSta >= nextStation:
      canvas.draw_gradient_ball(baseCanvas,printLoc,340,22,(0xFF, 0xFF, 0xFF),(0x00, 0x99, 0x00),10)
    if printSta == nextStation:
      nextStationLoc=printLoc

    printTransferLoc = 390
    for tline in station['transfer']:
      canvas.draw_transfer(baseCanvas,printLoc,printTransferLoc,transferLines[tline]['display'],transferLines[tline]['color'])
      printTransferLoc += 40
    
    printLoc = printLoc + printEach
    # arrow
    if printSta + 1 < len(stations):
      if printSta + 1 <= nextStation:
        arrowColor = "#AAAAAA"
      elif printSta + 1 > nextStation:
        arrowColor = "#00FF00"
      canvas.draw_arrow(baseCanvas,printLoc,340,arrowColor)
      canvas.draw_arrow(baseCanvas,printLoc - printArrow,340,arrowColor)
      canvas.draw_arrow(baseCanvas,printLoc + printArrow,340,arrowColor)
      if printSta + 1 == nextStation:
        nextStationArrowLoc=printLoc
    printLoc = printLoc + printEach
    printSta = printSta + 1
    root.update()

def shiftArrows():
  global nsashow
  global root
  if nsashow:
    if nextStationStatus == 0:
      baseCanvas.delete("nextarr")
      baseCanvas.delete("nextball")
      nsashow = False
  else:
    if nextStationStatus == 0 and nextStation > 0:
      canvas.draw_arrow(baseCanvas,nextStationArrowLoc,340,"#CC0000","nextarr")
      canvas.draw_arrow(baseCanvas,nextStationArrowLoc - printArrow,340,"#CC0000","nextarr")
      canvas.draw_arrow(baseCanvas,nextStationArrowLoc + printArrow,340,"#CC0000","nextarr")
    canvas.draw_gradient_ball(baseCanvas,nextStationLoc,340,22,(0xFF, 0xFF, 0xFF),(0xFF, 0x00, 0x00),10,"nextball")
    nsashow = True
  root.update()

def shiftInfo():
  global stationDesStatus
  global stationDes
  global stationDesEng
  if stationDesStatus:
    baseCanvas.delete("infoeng")
    baseCanvas.create_text(60, 140, text=stationDes, font=('黑体', 20),anchor="nw",tags="infocn")
    stationDesStatus = False
  else:
    baseCanvas.delete("infocn")
    baseCanvas.create_text(60, 140, text=stationDesEng, font=('Arial', 20),anchor="nw",tags="infoeng")
    stationDesStatus = True
  root.update()

async def runShiftInfo():
  while True:
    shiftInfo()
    await asyncio.sleep(3)

async def runShiftArrows():
  while True:
    shiftArrows()
    await asyncio.sleep(1)

async def mainRefresh():
  await asyncio.gather(runShiftInfo(), runShiftArrows())

if __name__ == "__main__":
  mainWindow()
  loadStations()
  printMain()
  printLine()
  asyncio.run(mainRefresh())
    

  