import tkinter as tk

# 主窗口
root = tk.Tk()

root.geometry("1920x420")
root.overrideredirect(True)
baseCanvas = tk.Canvas(root, width=1920, height=420, bg='white')
baseCanvas.pack()

logoImage = tk.PhotoImage(file = "common/logo.gif")
greyImage = tk.PhotoImage(file = "common/grey.gif").subsample(2,2)
redImage = tk.PhotoImage(file = "common/red.gif").subsample(2,2)
greenImage = tk.PhotoImage(file = "common/green.gif").subsample(2,2)
greyArrowImage = tk.PhotoImage(file = "common/greyarrow.gif").subsample(2,2)
redArrowImage = tk.PhotoImage(file = "common/redarrow.gif").subsample(2,2)
greenArrowImage = tk.PhotoImage(file = "common/greenarrow.gif").subsample(2,2)

# 示例信息
stations = [
  {"name":"工会","name_eng":"Gong hui","transfer":[],"doors":0},
  {"name":"胡罗贝","name_eng":"Hu luo bei","transfer":[],"doors":0},
  {"name":"溪口","name_eng":"Xi kou","transfer":[],"doors":0},
  {"name":"小桥","name_eng":"Xiao qiao","transfer":[],"doors":0},
  {"name":"知识村","name_eng":"Zhi shi cun","transfer":[],"doors":0},
  {"name":"雪村","name_eng":"Xue cun","transfer":[],"doors":0},
  {"name":"福瑞大道","name_eng":"Furui Blvd.","transfer":[],"doors":0},
  {"name":"前行路","name_eng":"Qianxing Rd.","transfer":[],"doors":0},
]
nextStation = 3

terminus = stations[len(stations) - 1]

baseCanvas.create_image(50, 60, anchor=tk.W, image=logoImage)
baseCanvas.create_text(400, 60, text="114", font=('黑体', 20))
baseCanvas.create_text(600, 60, text=f"开往：{terminus['name']}\nTerminus:{terminus['name_eng']}", font=('黑体', 20))
baseCanvas.create_text(1200, 60, text=f"下一站：{stations[nextStation]['name']}\nNext Station:{stations[nextStation]['name_eng']}", font=('黑体', 20))

printSta = 0
printLoc = 60
printEach = (1920 - printLoc - printLoc - 432)/((len(stations) - 1)*2)
for station in stations:
  print(printLoc)
  baseCanvas.create_text(printLoc, 300, text=station['name'], font=('黑体', 22), angle=45, anchor=tk.SW)
  baseCanvas.create_text(printLoc + 20, 300, text=station['name_eng'], font=('黑体', 14), angle=45, anchor=tk.SW)
  if printSta < nextStation:
    targerImage = greyImage
  elif printSta > nextStation:
    targerImage = greenImage
  else:
    targerImage = redImage
  baseCanvas.create_image(printLoc, 320, anchor=tk.CENTER, image=targerImage)
  printLoc = printLoc + printEach
  # arrow
  if printSta + 1 < len(stations):
    if printSta + 1 < nextStation:
      targerImage = greyArrowImage
    elif printSta + 1 > nextStation:
      targerImage = greenArrowImage
    else:
      targerImage = redArrowImage
    baseCanvas.create_image(printLoc, 320, anchor=tk.CENTER, image=targerImage)
  printLoc = printLoc + printEach
  printSta = printSta + 1

root.mainloop()