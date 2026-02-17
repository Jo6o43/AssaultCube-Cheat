import pygame
import win32api
import win32con
import win32gui
import ACInfo
from ScreenView import world_to_screen

def wallHack():
    pygame.init()
    
    width, height = 1920, 1200
    screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
    
    hwnd = pygame.display.get_wm_info()["window"]
    
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) |
                           win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOPMOST)
    
    fuchsia = (255, 0, 128)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        ac_hwnd = win32gui.FindWindow(None, "AssaultCube")
        if ac_hwnd:
            rect = win32gui.GetWindowRect(ac_hwnd)
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, rect[0], rect[1], 0, 0, win32con.SWP_NOSIZE)

        ACInfo.getInfo()
        matrix = ACInfo.get_view_matrix()
        botPos = ACInfo.get_bot_pos()
        botHeadPos = ACInfo.get_bot_head_pos()

        screen.fill(fuchsia) 

        if matrix and botPos and botHeadPos:
            for f_pos, h_pos in zip(botPos, botHeadPos):
                screen_feet = world_to_screen(matrix, f_pos, width, height)
                screen_head = world_to_screen(matrix, h_pos, width, height)

                if screen_feet and screen_head:
                    box_h = abs(screen_feet[1] - screen_head[1])
                    box_w = box_h / 2
                    
                    # Convert to integers
                    x = int(screen_head[0] - box_w / 2)
                    y = int(screen_head[1])
                    w = int(box_w)
                    h = int(box_h)
                    
                    # Draw Red Box
                    pygame.draw.rect(screen, (255, 0, 0), (x, y, w, h), 2)
                    
                    # Draw Snapline
                    pygame.draw.line(screen, (255, 255, 255), 
                                   (width // 2, height), screen_feet, 1)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    wallHack()