from Camera import *
# Дедлайн сегодня
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


def print_text(message, x, y, font_color=(0, 0, 0), font_type='PINGPONG.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.enactive_color = (13, 162, 58)
        self.active_color = (23, 204, 58)

    def draw(self, x, y, text, action=None, font_size=30):
        print('Зашёл в Draw')
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width:
            print('Зашёл в проверку x')
            if y < mouse[1] < y + self.height:
                print('Зашёл в проверку y')
                pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))

                if click[0] == 1:
                    print('Ку-ку')
                    action()


        else:
            pygame.draw.rect(screen, self.enactive_color, (x, y, self.width, self.height))

        print_text(message=text, x=x + 10, y=y + 10, font_size=font_size)


def menu():
    show = True

    menu_back = pygame.image.load('textures/menu.jpg')

    start_btn = Button(200, 100)

    while show:
        events = [event for event in pygame.event.get()]

        for event in events:
            if event.type == pygame.QUIT:
                show = False
                break

        screen.blit(menu_back, (0, 0))
        start_btn.draw(250, 200, 'Play', start_game, 50)

        pygame.display.update()

        pygame.display.flip()


def start_game():
    game()


def game():
    global run
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


if __name__ == '__main__':
    menu()
