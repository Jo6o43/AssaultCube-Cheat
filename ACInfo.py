import pymem
import pymem.process
import time

PROCESS_NAME = "ac_client.exe"

LOCAL_PLAYER_OFFSET = 0x18AC00 
ENTITY_LIST_OFFSET = 0x0591FD4
MAX_PLAYERS_OFFSET = 0x0591FD8

OFF_HEALTH = 0xEC
OFF_X = 0x04
OFF_Y = 0x08
OFF_Z = 0x0C
OFF_EYE_HEIGHT = 0x4C

botPos = []
botHeadPos = []

def getInfo():
    try:
        pm = pymem.Pymem(PROCESS_NAME)
        game_module = pymem.process.module_from_name(pm.process_handle, PROCESS_NAME).lpBaseOfDll
        
        print(f"[*] Conectado ao AssaultCube 1.3.0.2")
        print("[*] A ler dados de todos os jogadores...\n")

        while True:
            my_ptr = pm.read_int(game_module + LOCAL_PLAYER_OFFSET)
            if my_ptr:
                my_hp = pm.read_int(my_ptr + OFF_HEALTH)
                my_x = pm.read_float(my_ptr + OFF_X)
                my_y = pm.read_float(my_ptr + OFF_Y)
                print(f"[EU]    Vida: {my_hp:3} | Pos: X:{my_x:7.1f} Y:{my_y:7.1f}")
            
            possiveis_offsets_lista = [0x191058, 0x18AC04, 0x191068, 0x18AC08]
            possiveis_offsets_count = [0x191064, 0x19106C, 0x18AC0C]

            entity_list_ptr = 0
            num_players = 0

            for off in possiveis_offsets_count:
                val = pm.read_int(game_module + off)
                if 1 < val < 40:
                    num_players = val
                    break
            
            for off in possiveis_offsets_lista:
                val = pm.read_int(game_module + off)
                if val > 0:
                    entity_list_ptr = val
                    break

            print(f"DEBUG ATUALIZADO: Players: {num_players} | Lista: {hex(entity_list_ptr)}")

            if entity_list_ptr > 0:
                loop_limit = num_players if num_players > 0 else 10
                
                for i in range(1, loop_limit):
                    enemy_ptr = pm.read_int(entity_list_ptr + (i * 4))
                    
                    if enemy_ptr > 0:
                        e_hp = pm.read_int(enemy_ptr + OFF_HEALTH) 
                        
                        if 0 <= e_hp <= 100:
                            # 1. Posição dos Pés (World)
                            ex = pm.read_float(enemy_ptr + OFF_X)
                            ey = pm.read_float(enemy_ptr + OFF_Y)
                            ez = pm.read_float(enemy_ptr + OFF_Z)
                            
                            # 2. Altura Relativa da Cabeça (View Offset)
                            # Se este valor for 1.1, a cabeça está 1.1 unidades acima de 'ey'
                            rel_h = pm.read_float(enemy_ptr + OFF_EYE_HEIGHT)
                            
                            # 3. Posição Absoluta da Cabeça no Mundo
                            # X e Z são iguais aos pés, Y é somado
                            head_x = ex
                            head_y = ey + rel_h
                            head_z = ez
                            
                            print(f"Bot {i:2} | HP: {e_hp:3}")
                            print(f"      Pés   -> X:{ex:7.1f} Y:{ey:7.1f} Z:{ez:7.1f}")
                            botPos.append((ex, ey, ez))
                            print(f"      Cabeça-> X:{head_x:7.1f} Y:{head_y:7.1f} Z:{head_z:7.1f}")
                            botHeadPos.append((head_x, head_y, head_z))
                            
            
            
            time.sleep(0.5)
            print("-" * 50)

    except Exception as e:
        print(f"\n[!] Erro: {e}")
        print("Garante que o jogo está aberto e corre o script como Administrador.")