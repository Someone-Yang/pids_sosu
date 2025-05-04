import tkinter as tk
import asyncio
import canvas
import config

# 主窗口
def mainWindow():
  global root
  root = tk.Tk()

  root.geometry("1920x360")
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
  global stationDesStep
  global transferLines
  global runningStatus
  baseCanvas.create_image(50, 60, anchor=tk.W, image=logoImage)

  currentLine = config.getCurrentLine()
  baseCanvas.create_text(500, 60, text=currentLine['name'], font=('黑体', 24),anchor="s")
  baseCanvas.create_text(500, 60, text=currentLine['name_eng'], font=('Arial', 20),anchor="n")

  terminalEngDisplay = stations[terminus]['name_eng']
  
  baseCanvas.create_text(700, 60, text="开往", font=('黑体', 20),anchor="s")
  baseCanvas.create_text(700, 60, text="Terminus", font=('Arial', 16),anchor="n")
  baseCanvas.create_text(750, 60, text=stations[terminus]['name'], font=('黑体', 20),anchor="sw")
  baseCanvas.create_text(750, 60, text=terminalEngDisplay, font=('Arial', 16),anchor="nw")

  targetEngDisplay = stations[nextStation]['name_eng']
  if nextStationStatus == 0:
    targetNextDisplay = "下一站"
    targetNextDisplayEng = "Next Station"
  else:
    targetNextDisplay = "当前站"
    targetNextDisplayEng = "Current Station"

  baseCanvas.create_text(1100, 60, text=targetNextDisplay, font=('黑体', 20),anchor="s")
  baseCanvas.create_text(1100, 60, text=targetNextDisplayEng, font=('Arial', 16),anchor="n")
  baseCanvas.create_text(1180, 60, text=stations[nextStation]['name'], font=('黑体', 20),anchor="sw")
  baseCanvas.create_text(1180, 60, text=targetEngDisplay, font=('Arial', 16),anchor="nw")

  stationDes = []

  stationDesStep = 0

  stationDesSta = ""
  stationDesStaEng = ""
  if nextStationStatus == 0:
    stationDesSta += "下一站"
    stationDesStaEng += "The next station is "
  else:
    stationDesSta += "当前站"
    stationDesStaEng += "This station is "

  if nextStation == terminus:
    stationDesSta += "是本次列车的终点站"
    stationDesStaEng += "the terminal station "

  stationDesSta += stations[nextStation]['name']
  stationDesStaEng += stations[nextStation]['name_eng']

  stationDes.insert(0,stationDesSta)
  stationDes.append(stationDesStaEng)

  stationDesDoor = "请从列车运行方向"
  stationDesDoorEng = "Please get ready to exit from the "
  if stations[nextStation]['doors'] == 0:
    stationDesDoor += "左"
    stationDesDoorEng += "left"
  else:
    stationDesDoor += "右"
    stationDesDoorEng += "right"
  stationDesDoor += "侧车门下车"
  stationDesDoorEng += " side"

  stationDes.insert(len(stationDes) // 2,stationDesDoor)
  stationDes.append(stationDesDoorEng)

  if stations[nextStation].get("transfer"):
    stationDesTrs = "乘客可以换乘"
    stationDesTrsEng = "Passengers can transfer to "
    textTransferLeft = len(stations[nextStation]['transfer'])
    for tline in stations[nextStation]['transfer']:
      stationDesTrs += transferLines[tline]['name']
      stationDesTrsEng += transferLines[tline]['name_eng']
      textTransferLeft -= 1
      if textTransferLeft != 0:
        stationDesTrs += "、"
        stationDesTrsEng += ", "
    stationDes.insert(len(stationDes) // 2,stationDesTrs)
    stationDes.append(stationDesTrsEng)

  if stations[nextStation].get("interests"):
    stationDes.insert(len(stationDes) // 2,stations[nextStation]['interests'])

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
  global lineLoc
  printSta = 0
  printLoc = 32
  printEach = (1920 - 32 - 50 - 450)/((len(stations) - 1)*2)
  printArrow = (printEach - 16) / 2
  nextStationLoc = 0
  nextStationArrowLoc = 0
  lineLoc = 305
  for station in stations:
    if printSta < nextStation or printSta > terminus:
      targetTextColor = "grey"
    elif printSta >= nextStation:
      targetTextColor = "black"
    baseCanvas.create_text(printLoc, lineLoc - 38, text=station['name'], font=('黑体', 22), angle=45, anchor=tk.SW, fill=targetTextColor)
    if station.get('name_eng_display'):
      targetEngDisplay = station['name_eng_display']
    else:
      targetEngDisplay = station['name_eng']
    baseCanvas.create_text(printLoc, lineLoc - 38, text=targetEngDisplay, font=('Arial', 14), angle=45, anchor=tk.NW, fill=targetTextColor)
    if printSta < nextStation or printSta > terminus:
      canvas.draw_gradient_ball(baseCanvas,printLoc,lineLoc,22,(0xFF, 0xFF, 0xFF),(0xAA, 0xAA, 0xAA),10)
    elif printSta >= nextStation:
      canvas.draw_gradient_ball(baseCanvas,printLoc,lineLoc,22,(0xFF, 0xFF, 0xFF),(0x00, 0x99, 0x00),10)
    if printSta == nextStation:
      nextStationLoc=printLoc

    if station.get("transfer"):
      printTransferLoc = 344
      printTransferLocRow = printLoc - (len(station['transfer'])-1) * 14
      for tline in station['transfer']:
        canvas.draw_transfer(baseCanvas,printTransferLocRow,printTransferLoc,transferLines[tline]['display'],transferLines[tline]['color'])
        printTransferLocRow = printTransferLocRow + 28
    
    printLoc = printLoc + printEach
    # arrow
    if printSta + 1 < len(stations):
      if printSta + 1 <= nextStation or printSta + 1 > terminus:
        arrowColor = "#AAAAAA"
      elif printSta + 1 > nextStation:
        arrowColor = "#00FF00"
      canvas.draw_arrow(baseCanvas,printLoc,lineLoc,arrowColor)
      canvas.draw_arrow(baseCanvas,printLoc - printArrow,lineLoc,arrowColor)
      canvas.draw_arrow(baseCanvas,printLoc + printArrow,lineLoc,arrowColor)
      if printSta + 1 == nextStation:
        nextStationArrowLoc=printLoc
    printLoc = printLoc + printEach
    printSta = printSta + 1
    root.update()

def shiftArrows():
  global nsashow
  global root
  global lineLoc
  if nsashow:
    if nextStationStatus == 0:
      baseCanvas.delete("nextarr")
      baseCanvas.delete("nextball")
      nsashow = False
  else:
    if nextStationStatus == 0 and nextStation > 0:
      canvas.draw_arrow(baseCanvas,nextStationArrowLoc,lineLoc,"#CC0000","nextarr")
      canvas.draw_arrow(baseCanvas,nextStationArrowLoc - printArrow,lineLoc,"#CC0000","nextarr")
      canvas.draw_arrow(baseCanvas,nextStationArrowLoc + printArrow,lineLoc,"#CC0000","nextarr")
    canvas.draw_gradient_ball(baseCanvas,nextStationLoc,lineLoc,22,(0xFF, 0xFF, 0xFF),(0xFF, 0x00, 0x00),10,"nextball")
    nsashow = True
  root.update()

def shiftInfo():
  global stationDesStep
  global stationDes
  if stationDesStep >= len(stationDes):
    stationDesStep = 0
  baseCanvas.delete("info")
  targetFont = ""
  if stationDesStep >= (len(stationDes) / 2):
    targetFont = "Arial"
  else:
    targetFont = "黑体"
  baseCanvas.create_text(60, 120, text=stationDes[stationDesStep], font=(targetFont, 20),anchor="nw",tags="info")
  stationDesStep = stationDesStep + 1
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