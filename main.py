from Camera import *

pygame.init()
settings = {}
sprites_group = pygame.sprite.Group()
solids_objs = pygame.sprite.Group()
mob_group = pygame.sprite.Group()
all_objs = pygame.sprite.Group()

for i in range(10):
    mob = testEnemy((r.randrange(0, 1920), r.randrange(0, 1080)))
    mob.radius = r.choice([150, 300])
    mob.ai_list[0] = i
    mob.ai_list[1] = i
    mob_group.add(mob)
    all_objs.add(mob)

with open("settings.txt", "r", encoding="utf-8") as f:
    for i in f.read().split("\n"):
        a, b = i.split(":")
        settings[a] = b.split()

# Здесь будет происходить выгрузка параметров из файла settings.txt
size = list(map(int, settings["size"]))
FPS = int(*settings["FPS"])

screen = pygame.display.set_mode(size)
run = True

obj = SolidObj('textures/morgenshtern.jpg', (100, 400))
player = Player('textures/morgenshtern.jpg', (300, 300))
solids_objs.add(obj)
sprites_group.add(player)
all_objs.add(player, obj)
for i in range(5):
    obj = SolidObj('textures/morgenshtern.jpg', (0 + r.randrange(0, 1980, 50), 400 + r.randrange(0, 1080, 50)))
    solids_objs.add(obj)
    all_objs.add(obj)

cam = Camera(player)
clock = pygame.time.Clock()
while run:
    cam.update(screen, all_objs)
    screen.fill((0, 0, 0))
    events = [event for event in pygame.event.get()]
    m_pos = pygame.mouse.get_pos()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
            break

    mob_group.draw(screen)
    mob_group.update(solids_objs, sprites_group, sprites_group.sprites()[0], screen)

    sprites_group.draw(screen)

    solids_objs.draw(screen)
    solids_objs.update()
    sprites_group.update(events, m_pos, pygame.key.get_pressed(), solids_objs, screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
