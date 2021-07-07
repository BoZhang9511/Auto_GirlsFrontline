from auto8_1n_singalZAS import *

time.sleep(0.5)
img = getImage([0.36,0.33,0.38,0.35])
img.show()
time.sleep(1)

img = cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)
#cv2.imwrite("initial_IMG/main_menu.png", img)
