import tkinter as tk
import asyncio
import canvas
import config

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
  global runningStatus
  transferLines = config.getTransferLines()
  stations = config.getStations()
  runningStatus = config.getRunningStatus()

  global nextStation
  nextStation = runningStatus[0]

  global nextStationStatus
  nextStationStatus = runningStatus[1]

  global terminus
  terminus = runningStatus[2]

  if runningStatus[3] == 1:
    stations.reverse()
    nextStation = len(stations) - nextStation - 1
    terminus = len(stations) - terminus - 1


# 主线路信息
def printMain():
  global logoImage
  global terminus
  global stations
  global stationDes
  global stationDesStatus
  global stationDesEng
  global transferLines
  global runningStatus
  baseCanvas.create_image(50, 60, anchor=tk.W, image=logoImage)

  currentLine = config.getCurrentLine()
  baseCanvas.create_text(500, 60, text=currentLine['name'], font=('黑体', 24),anchor="s")
  baseCanvas.create_text(500, 60, text=currentLine['name_eng'], font=('Arial', 20),anchor="n")

  if stations[terminus].get('name_eng_display'):
    terminalEngDisplay = stations[terminus]['name_eng_display']
  else:
    terminalEngDisplay = stations[terminus]['name_eng']
  
  baseCanvas.create_text(700, 60, text="开往：", font=('黑体', 20),anchor="s")
  baseCanvas.create_text(700, 60, text="Terminus:", font=('Arial', 16),anchor="n")
  baseCanvas.create_text(750, 60, text=stations[terminus]['name'], font=('黑体', 20),anchor="sw")
  baseCanvas.create_text(750, 60, text=terminalEngDisplay, font=('Arial', 16),anchor="nw")

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

  baseCanvas.create_text(1100, 60, text=targetNextDisplay, font=('黑体', 20),anchor="s")
  baseCanvas.create_text(1100, 60, text=targetNextDisplayEng, font=('Arial', 16),anchor="n")
  baseCanvas.create_text(1180, 60, text=stations[nextStation]['name'], font=('黑体', 20),anchor="sw")
  baseCanvas.create_text(1180, 60, text=targetEngDisplay, font=('Arial', 16),anchor="nw")

  stationDes = ""
  stationDesEng = ""
  if nextStationStatus == 0:
    stationDes += "下一站"
    stationDesEng += "The next station is "
  else:
    stationDes += "当前站"
    stationDesEng += "This station is "

  if nextStation == terminus:
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
  stationDesEng += ". "

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
  global runningStatus
  printSta = 0
  printLoc = 32
  printEach = (1920 - 32 - 50 - 450)/((len(stations) - 1)*2)
  printArrow = (printEach - 16) / 2
  nextStationLoc = 0
  nextStationArrowLoc = 0
  for station in stations:
    if printSta < nextStation or printSta > terminus:
      targetTextColor = "grey"
    elif printSta >= nextStation:
      targetTextColor = "black"
    baseCanvas.create_text(printLoc, 300, text=station['name'], font=('黑体', 22), angle=45, anchor=tk.SW, fill=targetTextColor)
    if station.get('name_eng_display'):
      targetEngDisplay = station['name_eng_display']
    else:
      targetEngDisplay = station['name_eng']
    baseCanvas.create_text(printLoc, 300, text=targetEngDisplay, font=('Arial', 14), angle=45, anchor=tk.NW, fill=targetTextColor)
    if printSta < nextStation or printSta > terminus:
      canvas.draw_gradient_ball(baseCanvas,printLoc,340,22,(0xFF, 0xFF, 0xFF),(0xAA, 0xAA, 0xAA),10)
    elif printSta >= nextStation:
      canvas.draw_gradient_ball(baseCanvas,printLoc,340,22,(0xFF, 0xFF, 0xFF),(0x00, 0x99, 0x00),10)
    if printSta == nextStation:
      nextStationLoc=printLoc

    printTransferLoc = 380
    for tline in station['transfer']:
      canvas.draw_transfer(baseCanvas,printLoc,printTransferLoc,transferLines[tline]['display'],transferLines[tline]['color'])
      printTransferLoc += 32
    
    printLoc = printLoc + printEach
    # arrow
    if printSta + 1 < len(stations):
      if printSta + 1 <= nextStation or printSta + 1 > terminus:
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

async def runSync():
  global runningStatus
  prevStatus = runningStatus
  while True:
    if prevStatus != runningStatus:
      mainInit()
      shiftInfo()
      shiftArrows()
    prevStatus = config.getRunningStatus()
    await asyncio.sleep(1)

async def mainRefresh():
  await asyncio.gather(runShiftInfo(), runShiftArrows(),runSync())

def mainInit():
  baseCanvas.delete("all")
  loadStations()
  printMain()
  printLine()

if __name__ == "__main__":
  mainWindow()
  mainInit()
  asyncio.run(mainRefresh())