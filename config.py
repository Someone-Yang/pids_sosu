# 这里是数据配置方法
# 有需要可以自行编写接入其他函数，实现系统间交互

# 当前线路信息
# name: 中文名称
# name_eng: 英文名称
def getCurrentLine():
  return {
    "name":"奇异果线",
    "name_eng": "Kiwi Line",
    "color":"#326EC8"
  }

# 换乘线路信息
# 用以输出换乘站点其他线路简单信息，例如线路名称和颜色
# 整体返回字典，每个成员名是 getStations 中出现的站点的 transfer 数据
# name: 中文名称
# name_eng: 英文名称
# display: 缩写，显示在站点圆圈下方
# color: 颜色
def getTransferLines():
  return {
    "1":
    {
      "name":"1号线",
      "name_eng":"Line 1",
      "display":"1",
      "color":"#F9990B"
    },
    "2":
    {
      "name":"2号线",
      "name_eng":"Line 2",
      "display":"2",
      "color":"#66BD46"
    },
    "3":
    {
      "name":"3号线",
      "name_eng":"Line 3",
      "display":"3",
      "color":"#E13149"
    },
    "4":
    {
      "name":"4号线",
      "name_eng":"Line 4",
      "display":"4",
      "color":"#46D0E6"
    },
    "furry":
    {
      "name":"福瑞(环)线",
      "name_eng":"Furry Ring Line",
      "display":"瑞",
      "color":"#C9C90B"
    }
  }

# 车站线路信息
# name: 中文名称
# name_eng: 英文名称
# name_eng_display: 选填。显示在线路图中的英文名称，有时用来自定义换行
# transfer: 列表，填写上方某些换乘线路
# doors: 开门方向，针对本屏0为左，1为右
def getStations():
  return [
    {"name":"望村","name_eng":"Wangcun","name_eng_display":"Wang cun","transfer":["3"],"doors":0},
    {"name":"芳村","name_eng":"Fangcun","name_eng_display":"Fang cun","transfer":[],"doors":0},
    {"name":"黄雀东","name_eng":"Sparrow East Main Station","name_eng_display":"Sparrow East\nMain Station","transfer":["2","furry"],"doors":0},
    {"name":"石村","name_eng":"Shicun","name_eng_display":"Shi cun","transfer":[],"doors":0},
    {"name":"山村","name_eng":"Shancun","name_eng_display":"Shan cun","transfer":[],"doors":1},
    {"name":"雪村","name_eng":"Xuecun","name_eng_display":"Xue cun","transfer":[],"doors":1},
    {"name":"林樱万花","name_eng":"Linying Wanhua","transfer":["4"],"doors":1},
    {"name":"南村","name_eng":"Nancun (South Village)","name_eng_display":"Nan cun","transfer":[],"doors":1},
    {"name":"十亭","name_eng":"Shiting","transfer":["1","2","3"],"doors":0},
    {"name":"新天","name_eng":"Xintian","name_eng_display":"Xin tian","transfer":[],"doors":0},
    {"name":"福瑞路","name_eng":"Furry Road","transfer":[],"doors":0},
    {"name":"安定","name_eng":"Anding","name_eng_display":"An ding","transfer":[],"doors":0},
    {"name":"司南北站","name_eng":"Sinan North Railway Station","name_eng_display":"Sinan North\nRailway Station","transfer":["furry"],"doors":0},
  ]

# 下站信息
# 元组
# 第一个表示下一站的索引
# 第二个表示运行状态，0为正在前往下一站，1为已到站
# 第三个表示终点站
# 第四个表示运行方向，0为正，1为倒
# 反方向运行时，车站索引仍为正
def getRunningStatus():
  # return (2,0,8,0)
  # 正常接入其他系统，这里返回上面这样的元组即可
  # 为方便测试，这里每次会读入根目录 status.txt 文件，运行时可修改查看不同站效果
  with open('status.txt', 'r') as f:
    content = f.read()
  content = content.split(",")
  status = tuple(int(data) for data in content)
  return status