#=============================================#
#                                             #
#                 导入所需模块                 #
#                                             #
#=============================================#

import logging
import cv2
import time
import random
import datetime
import win32api
import win32gui
import win32con
from os import path
import numpy as np
from PIL import ImageGrab
from skimage.metrics import structural_similarity

#=============================================#
#                                             #
#                 定义所需常量                 #
#                                             #
#=============================================#


#=================截图比对区域=================#
IMAGE_PATH = 'initial_IMG/'#读取截图的路径   
FIRST_LOGIN_IMAGE_BOX = [0.60,0.58,0.75,0.65]#每日第一次登录时那个确认窗口判断区域
MAIN_MENU_IMAGE_BOX =  [0.65,0.50,0.75,0.58]#主界面判断区域                       
L_SUPPORT_IMAGE_BOX = [0.05,0.30,0.18,0.39]#后勤完成界面判断区域                
COMBAT_MENU_IMAGE_BOX = [0.05,0.70,0.12,0.80]#战斗菜单界面判断区域  
CHOOSE_8_1_IMAGE_BOX = [0.50,0.32,0.60,0.40]#8-1菜单界面判断区域
MAP_IMAGE_BOX = [0.01,0.08,0.10,0.14]#进入地图判断区域   
SET_TEAM_IMAGE_BOX = [0.85,0.75,0.92,0.78]#队伍放置判断区域 
COMBAT_START_IMAGE_BOX = [0.80,0.82,0.97,0.88]#开启作战判断区域   
COMBAT_FINISH_IMAGE_BOX = [0.05,0.19,0.15,0.23]#战役完成判断区域  
ENEMY_IMAGE_BOX = [0.45,0.60,0.65,0.66]#遇敌判断区域
EVENT_IMAGE_BOX = [0.35,0.49,0.42,0.54]#事件判断区域
RESTART_IMAGE_BOX = [0.22,0.08,0.26,0.14]#重启判断区域 
DESKTOP_IMAGE_BOX = [0.10,0.20,0.22,0.35]#模拟器桌面判断区域 
COMBAT_PAUSE_IMAGE_BOX = [0.45,0.62,0.55,0.67]#战斗终止提示判断区域            
RETURN_COMBAT_IMAGE_BOX = [0.75,0.63,0.90,0.70]#回到作战界面判断区域    
ROUND_IMAGE_BOX = [0.3,0.1,0.4,0.15]#回合数判断区域
PAUSE_IMAGE_BOX = [0.45,0.07,0.55,0.09]#暂停判断区域
HEADQUARTERS_IMAGE_BOX = [0.364,0.55,0.378,0.565]#指挥部判断区域

#=================点击拖动区域=================#

#从主菜单进入作战选择界面
COMBAT_CLICK_BOX =  [0.65,0.50,0.75,0.58]#在主菜单点击战斗（无作战进行中情况）
#[0.65,0.58,0.75,0.63]
COMBAT_ON_CLICK_BOX = [0.65,0.50,0.75,0.58]#在主菜单点击战斗（作战中断情况）

#从作战选择界面进入8-1界面
COMBAT_MISSION_CLICK_BOX =  [0.05,0.28,0.10,0.32]#点击作战任务
#[0.05,0.20,0.10,0.24]
#[0.05,0.28,0.10,0.32]
CHAPTER_DRAG_BOX = [0.16,0.75,0.22,0.80]#向上拖章节选择条
CHAPTER_8_CLICK_BOX = [0.15,0.17,0.20,0.18]#选择第8章
NORMAL_CLICK_BOX = [0.74,0.24,0.77,0.28]#选择普通难度
EPISODE_DRAG_BOX = [0.40,0.75,0.80,0.80]#向上拖小节选择条

#开始8-1
EPISODE_1_CLICK_BOX = [0.40,0.35,0.80,0.40]#选择第1节
ENTER_COMBAT_CLICK_BOX = [0.72,0.70,0.80,0.75]#进入作战
END_COMBAT_STEP1_CLICK_BOX = [0.72,0.62,0.80,0.66]#终止作战
END_COMBAT_STEP2_CLICK_BOX = [0.52,0.60,0.60,0.65]#确认终止作战

#地图缩放、拖动区
MAP_SCALE_BOX = [0.80,0.20,0.90,0.25]
MAP_DRAG_BOX =[0.80,0.20,0.90,0.25]

#队伍放置点
COMMAND_CLICK_BOX = [0.364,0.55,0.378,0.565]#指挥部
#[0.36,0.54,0.39,0.58]
#放置队伍
TEAM_SET_CLICK_BOX = [0.85,0.75,0.92,0.78]

#点击开始作战
START_COMBAT_CLICK_BOX = [0.85,0.82,0.92,0.86]
#结束回合
ROUND_END_CLICK_BOX = [0.88,0.82,0.98,0.88]

#前往各点
POINT_1_CLICK_BOX = [0.375,0.48,0.39,0.50]
POINT_2_CLICK_BOX = [0.448,0.485,0.465,0.505]
POINT_3_CLICK_BOX = [0.535,0.49,0.55,0.51]

#确定进击
CONFIRM_ATTACK_CLICK_BOX = [0.53,0.60,0.64,0.64]

#确认事件
CONTINUE_CLICK_BOX = [0.45,0.45,0.55,0.55]

#重启作战
RESTART_STEP1_CLICK_BOX = [0.22,0.08,0.26,0.14]#点击终止作战
RESTART_STEP2_CLICK_BOX = [0.35,0.60,0.44,0.64]#点击重新作战

#撤退
PAUSE_CLICK_BOX = [0.48,0.07,0.52,0.09]
RETREAT_CLICK_BOX = [0.32,0.07,0.38,0.11]

#战役结算
COMBAT_END_CLICK_BOX = [0.48,0.08,0.52,0.10]#战役结算

#跳至主菜单/战斗菜单/工厂菜单
NAVIGATE_BAR_CLICK_BOX = [0.15,0.10,0.18,0.15]#打开导航条
NAVIGATE_MAIN_MENU_CLICK_BOX = [0.20,0.18,0.28,0.20]#跳转至主菜单

#收后勤支援
L_SUPPORT_STEP1_CLICK_BOX = [0.50,0.50,0.60,0.60]#确认后勤完成
L_SUPPORT_STEP2_CLICK_BOX = [0.53,0.60,0.62,0.65]#再次派出

#启动游戏
START_GAME_STEP1_CLICK_BOX = [0.14,0.23,0.18,0.28]#点击图标启动
START_GAME_STEP2_CLICK_BOX = [0.50,0.70,0.50,0.70]#点击一次
START_GAME_STEP3_CLICK_BOX = [0.50,0.75,0.50,0.75]#点击开始 

#关闭游戏
CLOSE_GAME_CLICK_BOX = [0.56,0.02,0.57,0.04]

#关闭作战断开提醒
CLOSE_TIP_CLICK_BOX = [0.45,0.62,0.55,0.67]

#每日第一次登录的确认
CHECK_INFORMATION_CLICK_BOX = [0.26,0.61,0.27,0.63]#勾选今日不在弹出
CONFIRM_INFORMATION_CLICK_BOX = [0.65,0.60,0.72,0.63]#点击确认
#=============================================#
#                                             #
#                 基本功能函数                 #
#                                             #
#=============================================#

#启动界面，传统艺能
def preface():    
    for x in range(3,-1,-1):
        mystr =">>> "+str(x)+"s 后将开始操作，请切换至模拟器界面"
        print(mystr,end="")
        print("\b" * (len(mystr)*2),end = "",flush=True)
        time.sleep(1)
    logger.debug("开始操作")


#等待若干时间,时间在min~max之间
def wait(minTime,maxTime):
    waitTime = minTime + (maxTime - minTime) * random.random()
    time.sleep(waitTime)


#获取模拟器窗口数据
def getWindowData():
    windowName = "少女前线 - MuMu模拟器"
    windowNameDesktop = "MuMu模拟器"
#    windowName = "Spyder (Python 3.7)"
    hwnd = win32gui.FindWindow(None,windowName)#根据窗口名称找到窗口句柄
    hwnd_desktop = win32gui.FindWindow(None,windowNameDesktop)
    if hwnd == 0 and hwnd_desktop == 0:
        logger.debug("未找到窗口界面,程序自动退出！")
        exit(0)
    elif hwnd != 0:
        left,top,right,bottom = win32gui.GetWindowRect(hwnd)#获取窗口的位置数据
    elif hwnd_desktop != 0:
        left,top,right,bottom = win32gui.GetWindowRect(hwnd_desktop)#获取窗口的位置数据
    width  = right - left
    height = bottom - top
    return [left,top,right,bottom,width,height]
        

#获取指定区域box的截图
def getImage(box):
    #windowData = [left,top,right,bottom,width,height]        
    windowData = getWindowData()
    imgLeft   = windowData[0] + int(windowData[4] * box[0])
    imgTop    = windowData[1] + int(windowData[5] * box[1])
    imgRight  = windowData[0] + int(windowData[4] * box[2])
    imgBottom = windowData[1] + int(windowData[5] * box[3])
    img = ImageGrab.grab((imgLeft,imgTop,imgRight,imgBottom))
    return img
    
    
#点击box内随机一点，如果提供具体xy偏量，则点击精确的点
def mouseClick(box,minTime,maxTime,exact_x = 0,exact_y = 0):
    #box = [left,top,right,bottom]
    windowData = getWindowData()
    width  = box[2] - box[0]
    height = box[3] - box[1]
    if exact_x == 0 and exact_y == 0:
        clickX = windowData[0] + (int)(windowData[4] * box[0] + windowData[4] * width  * random.random())
        clickY = windowData[1] + (int)(windowData[5] * box[1] + windowData[5] * height * random.random())
    else:
        clickX = windowData[0] + (int)(windowData[4] * box[0]) + exact_x
        clickY = windowData[1] + (int)(windowData[5] * box[1]) + exact_y
    clickPos = (clickX,clickY)
    win32api.SetCursorPos(clickPos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
    wait(minTime,maxTime)


#模拟鼠标拖动，box为起始区域,times为拖动次数,distance为单次拖动距离
#dx,dy为组成移动方向向量，frame_interval为鼠标拖动帧间隔,越小鼠标拖动越快
#multi_interval为连续拖动时的时间间隔
def mouseDrag(box,dx,dy,times,distance,frame_interval,multi_interval):
    windowData = getWindowData()
    width  = box[2] - box[0]
    height = box[3] - box[1]
    for i in range(times):
        dragX = windowData[0] + int(windowData[4] * box[0] + windowData[4] * width  * random.random())
        dragY = windowData[1] + int(windowData[5] * box[1] + windowData[5] * height * random.random())
        dragPos = (dragX, dragY)
        win32api.SetCursorPos(dragPos)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
        for i in range(distance):
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,dx,dy,0,0)
            time.sleep(frame_interval)
        time.sleep(0.2)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
        time.sleep(multi_interval)


#模拟Ctrl和滚轮实现缩放地图
#direct = 0 : 放大      direct = 1 : 缩小   times为连续缩放次数i
def scaleMap(box,direct,times):
    windowData = getWindowData()
    width  = box[2] - box[0]
    height = box[3] - box[1]
    scaleX = windowData[0] + int(windowData[4] * box[0] + windowData[4] * width  * random.random())
    scaleY = windowData[1] + int(windowData[5] * box[1] + windowData[5] * height * random.random())
    scalePos = (scaleX, scaleY)
    win32api.SetCursorPos(scalePos)
    win32api.keybd_event(0x11,0,0,0)#按下Ctrl键
    for i in range(times):
        if direct == 0:
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,0,0,1)
        else:
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,0,0,-1)
        wait(0.5,0.7)
    win32api.keybd_event(0x11, 0, win32con.KEYEVENTF_KEYUP,0)    
    time.sleep(1)


#比较两图片吻合度，结构相似性比较法
def imageCompare(img1,img2):
    gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    (score, diff) = structural_similarity(gray_img1, gray_img2, full=True)
    return score > 0.90

#=============================================#
#                                             #
#                 状态判断函数                 #
#                                             #
#=============================================#

#判断是否战役结束
def isCombatFinished():
    initImage = cv2.imread(IMAGE_PATH+"combat_finish.png")
    capImage  = getImage(COMBAT_FINISH_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)
    
def isRestart():
    initImage = cv2.imread(IMAGE_PATH+"restart.png")
    capImage  = getImage(RESTART_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)
     
#判断是否进入了8-1地图
def isMap():
    initImage = cv2.imread(IMAGE_PATH+"map.png")
    capImage  = getImage(MAP_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否遇敌
def isEnemy():
    initImage = cv2.imread(IMAGE_PATH+"enemy.png")
    capImage  = getImage(ENEMY_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否发送事件
def isEvent():
    initImage = cv2.imread(IMAGE_PATH+"event.png")
    capImage  = getImage(EVENT_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)
    
#判断是否作战正常开启
def isCombatStart():
    initImage = cv2.imread(IMAGE_PATH+"combat_start.png")
    capImage  = getImage(COMBAT_START_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否是可以选择8-1n的界面
def is8_1():
    initImage = cv2.imread(IMAGE_PATH+"_8_1.png")
    capImage  = getImage(CHOOSE_8_1_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否是战斗选择菜单
def isCombatMenu():
    initImage = cv2.imread(IMAGE_PATH+"combat_menu.png")
    capImage  = getImage(COMBAT_MENU_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否是主界面
def isMainMenu():
    initImage = cv2.imread(IMAGE_PATH+"main_menu.png")
    capImage  = getImage(MAIN_MENU_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)
  
#判断是否是每日第一次登录的确认界面
def isFirstLogin():
    initImage = cv2.imread(IMAGE_PATH+"first_login.png")
    capImage  = getImage(FIRST_LOGIN_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)   

#判断是否是委托完成界面
def isLSupport():
    initImage = cv2.imread(IMAGE_PATH+"L_support.png")
    capImage  = getImage(L_SUPPORT_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否是模拟器桌面
def isDesktop():
    initImage = cv2.imread(IMAGE_PATH+"desktop.png")
    capImage  = getImage(DESKTOP_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否是战斗中断提示界面
def isCombatPause():
    initImage = cv2.imread(IMAGE_PATH+"combat_pause.png")
    capImage  = getImage(COMBAT_PAUSE_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#判断是否有回到作战界面
def isReturnCombat():
    initImage = cv2.imread(IMAGE_PATH+"return_combat.png")
    capImage  = getImage(RETURN_COMBAT_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

#在队伍放置界面
def isSetTeam():
    initImage = cv2.imread(IMAGE_PATH+"set_team.png")
    capImage  = getImage(SET_TEAM_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)
    
def isRound2():
    initImage = cv2.imread(IMAGE_PATH+"round_2.png")
    capImage  = getImage(ROUND_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

def isPauseButton():
    initImage = cv2.imread(IMAGE_PATH+"pause.png")
    capImage  = getImage(PAUSE_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)

def isHeadquarters():
    initImage = cv2.imread(IMAGE_PATH+"headquarters.png")
    capImage  = getImage(HEADQUARTERS_IMAGE_BOX)
    capImage  = cv2.cvtColor(np.asarray(capImage),cv2.COLOR_RGB2BGR)
    return imageCompare(initImage,capImage)
    
#=============================================#
#                                             #
#                 动作执行函数                 #
#                                             #
#=============================================#
    
#从主菜单进入作战菜单
def mainMenuToCombatMenu():
    logger.debug("ACTION: 前往作战菜单")
    mouseClick(COMBAT_CLICK_BOX,5,6)  

#从主菜单进入作战菜单（战斗中断情况）
def mainMenuToCombatMenu_combatOn():
    logger.debug("ACTION: 前往作战菜单-战斗中断")
    mouseClick(COMBAT_ON_CLICK_BOX,5,6)  

#从作战菜单进入8-1界面
def combatMenuTo8_1():
    logger.debug("ACTION: 前往8-1选择界面")
    mouseClick(COMBAT_MISSION_CLICK_BOX,1,2)
    mouseDrag(CHAPTER_DRAG_BOX,0,-1,3,400,0.001,0.8)
    mouseClick(CHAPTER_8_CLICK_BOX,1,2)
    mouseClick(NORMAL_CLICK_BOX,1,2)

#开始8-1
def start8_1():
    logger.debug("ACTION: 启动8-1")
    mouseClick(EPISODE_1_CLICK_BOX,2,3)
    mouseClick(ENTER_COMBAT_CLICK_BOX,4.8,5)  
    
#终止8-1
def end8_1():
    logger.debug("ACTION: 终止8-1")
    mouseClick(EPISODE_1_CLICK_BOX,2,3)
    mouseClick(END_COMBAT_STEP1_CLICK_BOX,2,3)  
    mouseClick(END_COMBAT_STEP2_CLICK_BOX,2,3)  

#战前准备，调整地图
def combatPrepare(tiny = False):
    logger.debug("STATE: 战前整备")
    if tiny:
        scaleMap(MAP_SCALE_BOX,1,1)
        mouseDrag(MAP_DRAG_BOX,-1,1,1,500,0.001,1)  
    else:
        scaleMap(MAP_SCALE_BOX,1,7)
        mouseDrag(MAP_DRAG_BOX,-1,1,1,500,0.001,1)  

#放置队伍
def setTeam():
    logger.debug("ACTION: 放置队伍")
 
    mouseClick(COMMAND_CLICK_BOX,0,0)
    checkCount = 0
    while not isSetTeam() and checkCount < 20:
        time.sleep(0.4)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(0.2)
    
    mouseClick(TEAM_SET_CLICK_BOX,0.5,0.6)
    checkCount = 0
    while not isMap() and checkCount < 40:
        time.sleep(0.2)
        checkCount += 1
    if checkCount >= 40:
        return False
    time.sleep(0.2)
        
    return True

#开始作战
def startCombat():
    logger.debug("ACTION: 开始作战")
    mouseClick(START_COMBAT_CLICK_BOX,0,0)
    checkCount = 0
    while not isCombatStart() and checkCount < 20:
        time.sleep(0.5)
        checkCount += 1
    if checkCount >= 20:
        return False
    time.sleep(2)
    return True

#前往1号点，结束回合
def action_1():
    logger.debug("ACTION: 前往1号点")
    mouseClick(COMMAND_CLICK_BOX,0.8,1)
    mouseClick(POINT_1_CLICK_BOX,1.3,1.4)
    mouseClick(ROUND_END_CLICK_BOX,0,0)
    return True

#前往3号点
def action_2():
    logger.debug("ACTION: 前往3号点")
    mouseClick(POINT_1_CLICK_BOX,0.6,0.7)
    mouseClick(POINT_2_CLICK_BOX,2.3,2.5)
    mouseClick(POINT_3_CLICK_BOX,1.2,1.3)
    mouseClick(CONFIRM_ATTACK_CLICK_BOX,0,0)
    return True

#确认事件
def confirmEvent():
    mouseClick(CONTINUE_CLICK_BOX,0.6,0.8)

def retreat():
    logger.debug("ACTION: 遇敌撤退")
    checkCount = 0
    while not isPauseButton() and checkCount < 50:
        time.sleep(0.3)
        checkCount += 1
    if checkCount >= 50:
        return False
    mouseClick(PAUSE_CLICK_BOX,0.5,0.6)
    mouseClick(RETREAT_CLICK_BOX,0.5,0.6)
    return True

#重启作战
def restartCombat():
    logger.debug("ACTION: 重启作战")
    mouseClick(RESTART_STEP1_CLICK_BOX,1,1.5)
    mouseClick(RESTART_STEP2_CLICK_BOX,0,0)
    checkCount = 0
    while not isMap() and checkCount < 50:
        time.sleep(0.2)
        checkCount += 1
    if checkCount >= 50:
        return False
    time.sleep(0.5)
    return True    


#跳转至主菜单(回主菜单收后勤)
def backToMainMenu():
    logger.debug("ACTION: 跳转至主菜单")
    mouseClick(NAVIGATE_BAR_CLICK_BOX,1,2)
    mouseClick(NAVIGATE_MAIN_MENU_CLICK_BOX,5,6)
    
#收后勤支援
def takeLSupport():
    logger.debug("ACTION: 收派后勤")
    mouseClick(L_SUPPORT_STEP1_CLICK_BOX,2,3)
    mouseClick(L_SUPPORT_STEP2_CLICK_BOX,4,5)

#启动游戏
def startGame():
    logger.debug("ACTION: 启动游戏")
    mouseClick(START_GAME_STEP1_CLICK_BOX,15,15)
    mouseClick(START_GAME_STEP2_CLICK_BOX,10,10)
    mouseClick(START_GAME_STEP3_CLICK_BOX,10,10)

#关闭作战断开提醒
def closeTip():
    mouseClick(CLOSE_TIP_CLICK_BOX,5,5)

#关闭游戏
def closeGame():
    mouseClick(CLOSE_GAME_CLICK_BOX,5,5)

#确认每日第一次登录的公告
def confirmAnnouncement():
    mouseClick(CHECK_INFORMATION_CLICK_BOX,2,2)
    mouseClick(CONFIRM_INFORMATION_CLICK_BOX,2,2)
#=============================================#
#                                             #
#                 本程序主函数                 #
#                                             #
#=============================================#

# 创建Logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# 创建Handler
# 终端Handler
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)  
# 文件Handler
currentPath = path.dirname(__file__)
fileHandler = logging.FileHandler(currentPath+'/log.log', mode='w', encoding='UTF-8')
fileHandler.setLevel(logging.NOTSET)
# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
consoleHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)  
# 添加到Logger中
logger.addHandler(consoleHandler)
logger.addHandler(fileHandler)

if __name__ == "__main__": 
    preface()
    startTime = datetime.datetime.now()
    stepCount = 0
    failCount = 0

    while True:
        if isMap():
            logger.debug("STATE：地图")
            #time.sleep(0.5)
            if not isHeadquarters():
                combatPrepare()
            if not setTeam():
                logger.debug("ERROR：放置1队失败")
                closeGame()
                continue
            if not startCombat():
                logger.debug("ERROR：开启作战失败")
                closeGame()
                continue
            checkCount = 0
            while not isCombatStart() and checkCount < 50:#防止网络卡顿，最多等10s
                checkCount += 1
                time.sleep(0.2)
            if checkCount >= 50:#过了10s还是卡着，启动失败，直接关闭窗口重启
                logger.debug("ERROR：作战启动超时！")
                closeGame()
                continue
            
            if not action_1():#第一回合
                continue
                
            checkCount = 0
            while not isRound2() and checkCount < 30:
                checkCount += 1
                time.sleep(1)
            if checkCount >= 30:
                closeGame()
                continue
            time.sleep(4)#等待第二回合开始
            
            if not action_2():#第二回合
                continue
            
            checkCount = 0
            while not isEvent() and checkCount <50:
                checkCount +=1
                time.sleep(0.1)
            if checkCount >=50:
                closeGame()
                continue
            confirmEvent()
            retreat()          
            
            stepCount += 1
            
            checkCount = 0
            while not isCombatFinished() and checkCount < 50:
                mouseClick([0.70,0.40,0.90,0.65],0.4,0.5)
                checkCount += 1
            if checkCount >= 50:
                closeGame()
                continue
            
            checkCount = 0
            while not is8_1() and checkCount < 50:
                mouseClick(COMBAT_END_CLICK_BOX,0.4,0.5)
                checkCount += 1
            if checkCount >= 50:
                closeGame()
                continue

            currentTime = datetime.datetime.now()
            runtime = currentTime - startTime
            logger.debug('> 已运行：'+str(runtime)+'  踩点数: '+str(stepCount))
            if stepCount%3 == 0: #每3轮收一次后勤
                backToMainMenu()
        elif isRestart():
            logger.debug("STATE：状态未知，可直接重启") 
            restartCombat() 
        elif is8_1():
            logger.debug("STATE： 8-1界面")
            start8_1()
            failCount = 0
        elif isCombatMenu():
            logger.debug("STATE： 战斗菜单")
            combatMenuTo8_1()
            failCount = 0
        elif isCombatPause():
            logger.debug("STATE： 战斗中断提醒界面")
            failCount = 0
            closeTip()
        elif isReturnCombat():
            logger.debug("STATE： 返回作战界面")
            failCount = 0
            mainMenuToCombatMenu_combatOn()
            combatMenuTo8_1()
            end8_1()
        elif isMainMenu():
            logger.debug("STATE： 主菜单界面")
            mainMenuToCombatMenu()
            failCount = 0
        elif isLSupport():
            logger.debug("STATE： 后勤结束界面")
            takeLSupport()
            failCount = 0
        elif isDesktop():
            logger.debug("STATE：模拟器桌面")
            failCount = 0
            startGame()
            continue
        elif isFirstLogin():
            logger.debug("STATE：公告确认")
            failCount = 0
            confirmAnnouncement()
            continue
        else:#不知道在哪
            logger.debug("ERROR： 当前状态未知!")
            failCount += 1
            if failCount == 4:
                mouseClick([0.3,0.45,0.4,0.55],1,1)
            if failCount >= 5:  
                img = getImage([0,0,1,1])
                img.save("errorRecord/"+str(stepCount)+".png")
                logger.debug(" 无法确定当前状态,关闭重启！")
                closeGame()
            else:
                time.sleep(5)
                