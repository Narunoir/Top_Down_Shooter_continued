import pygame as pg, pygame
import sys
from os import path
from settings import *
from sprites import*
from tilemap import *




## HUD Functions ##
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(int(x), int(y), int(fill), BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


class Game:
    def __init__(self):
        # initialize game window, ect
        pg.mixer.pre_init(44100, -16, 1, 2048)
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption(TITLE)
        pg.key.set_repeat(50, 10)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(DEFAULT_FONT_NAME)
        self.load_data()
        self.current_level = 2
        self.fighting_boss = False



    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')
        self.map_folder = path.join(game_folder, 'maps')
        wall_folder = path.join(game_folder, 'img')
        mob_folder  = path.join(game_folder, 'img')
        self.title_font = path.join(game_folder, 'img', TITLE_FONT)
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        #self.player_img = {}
        #self.player_img['pistol'] = pg.image.load(path.join(img_folder, PLAYER_IMG['pistol'])).convert_alpha()
        #self.player_img['shotgun']= pg.image.load(path.join(img_folder, PLAYER_IMG['pistol'])).convert_alpha()
        #self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.player_img1 = pg.image.load(path.join(img_folder, PLAYER_IMG['pistol'])).convert_alpha()
        self.player_img = self.player_img1
        self.player_img2 = pg.image.load(path.join(img_folder, PLAYER_IMG['shotgun'])).convert_alpha()
        self.mob_img = pg.image.load(path.join(mob_folder, MOB_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(wall_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))

        self.bullet_images = {}
        self.bullet_images['lg'] = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_images['sm'] = pg.transform.scale(self.bullet_images['lg'], (10, 10))

        self.boss_image = {}
        self.boss_image[1] = pg.image.load(path.join(img_folder, BOSS[1]['boss_image'])).convert_alpha()
        self.boss_image[1] = pg.transform.scale(self.boss_image[1], (100, 100))
        self.boss_image[2] = pg.image.load(path.join(img_folder, BOSS[2]['boss_image'])).convert_alpha()
        self.boss_image[2] = pg.transform.scale(self.boss_image[2], (250, 250))
        self.boss_image[3] = pg.image.load(path.join(img_folder, BOSS[3]['boss_image'])).convert_alpha()
        self.boss_image[4] = pg.image.load(path.join(img_folder, BOSS[3]['boss_image'])).convert_alpha()
        self.boss_image[5] = pg.image.load(path.join(img_folder, BOSS[3]['boss_image'])).convert_alpha()
        self.boss_image[6] = pg.image.load(path.join(img_folder, BOSS[3]['boss_image'])).convert_alpha()
        self.boss_image[7] = pg.image.load(path.join(img_folder, BOSS[3]['boss_image'])).convert_alpha()
        self.boss_image[8] = pg.image.load(path.join(img_folder, BOSS[3]['boss_image'])).convert_alpha()
        self.boss_image[9] = pg.image.load(path.join(img_folder, BOSS[3]['boss_image'])).convert_alpha()
        self.boss_image[10] = pg.image.load(path.join(img_folder, BOSS[3]['boss_image'])).convert_alpha()



        self.splat = pg.image.load(path.join(img_folder, SPLAT)).convert_alpha()
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        ### Sound loading
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))
        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(snd_folder, snd))
                s.set_volume(.05)
                self.weapon_sounds[weapon].append(s)
        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.25)
            self.zombie_moan_sounds.append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            phs = pg.mixer.Sound(path.join(snd_folder, snd))
            phs.set_volume(1)
            self.player_hit_sounds.append(phs)
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            zhs = pg.mixer.Sound(path.join(snd_folder, snd))
            zhs.set_volume(.15)
            self.zombie_hit_sounds.append(zhs)

    def next_level(self):
        try:
            self.current_level += 1
            self.new()
        except:
            self.playing = False
    def new(self):
        # starts a new game
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.boss = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.draw_text
        self.fighting_boss = False
        self.player_img = self.player_img1
        #self.z_count = 0
        self.map = TiledMap(path.join(self.map_folder, LEVEL[self.current_level]))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        ###Old code for showing the text map  ###
        #for row, tiles in enumerate(self.map.data):
            #for col, tile in enumerate(tiles):
                #if tile == '1':
                    #Wall(self, col, row)
                #if tile == 'M':
                    #Mob(self, col, row)
                #if tile == 'P':
                    #self.player = Player(self, col, row)

        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                            tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'zombie':
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                        tile_object.width, tile_object.height)
            if tile_object.name in ['health_pack', 'shotgun']:
                Item(self, obj_center, tile_object.name)

#####################################################################################
            #if tile_object.name == 'Boss':
                #Boss(self, obj_center.x, obj_center.y)


        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        self.effects_sounds['level_start'].set_volume(.25)
        self.effects_sounds['level_start'].play()



    def run(self):
        # Game Loop
        self.playing = True
        pg.mixer.music.play(loops = -1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()


    def update(self):
        # Updates the whole general loop
        self.all_sprites.update()
        self.camera.update(self.player)
        ## level over ##
        if len(self.mobs) == 0 and self.fighting_boss == True:
            self.next_lvl_screen()
            self.next_level()
        if len(self.mobs) == 0:
            self.fighting_boss = True
            Boss(self, 180, 620)

        ## Player item pick up ##
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health_pack' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_AMOUNT)
            if hit.type == 'shotgun':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'shotgun'
                self.player_img = self.player_img2
        ## Mobs Hit Player  ##
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            if random.random() < 0.7:
                choice(self.player_hit_sounds).play()
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.got_hit()
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        ##### Boss hits player  ####
        hits = pg.sprite.spritecollide(self.player, self.boss, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= BOSS[self.current_level]['boss_damage']
        ## Bullets hit Mobs  ##
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for mob in hits:
            #hit.health -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])
            for bullet in hits[mob]:
                mob.health -= bullet.damage
            mob.vel = vec(0,0)

    def events(self):
        # events that need to be stored like actions and movement
        for event in pygame.event.get():
            # closeing Windows
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    self.paused = not self.paused


    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (int(x), int(y))
        self.screen.blit(text_surface, text_rect)



    def draw_grid(self):
        for x in range(0,WIDTH,TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x,0), (x,HEIGHT))
        for y in range(0,HEIGHT,TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0,y), (WIDTH,y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        #self.screen.fill(BGCOLOR)
        #self.draw_grid()

        ### Draws everything ###
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pass
                #pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
        ## HUD  ##
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        ##Zombie counter ##
        self.draw_text('Zombies: {}'.format(len(self.mobs)),self.font_name, 30, WHITE, WIDTH / 2, 15, 'center')
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 205, RED, WIDTH / 2, HEIGHT / 2, 'center')


        # always last to view changes
        pygame.display.flip()

    def show_start_screen(self):
        # opens a start screen
        # opens a game over screen
        self.screen.fill(BLACK)
        self.draw_text('ZOMBIES ATE MY BLOCKS', self.title_font, 100, RED, WIDTH / 2, HEIGHT / 2, align='center')
        self.draw_text('Press any Key to Begin',self.title_font, 75, WHITE,
                        WIDTH / 2, HEIGHT /2 + 140, align='center')
        pg.display.flip()
        self.wait_for_key()


    def next_lvl_screen(self):
        # opens a Next Level screen
        self.screen.fill(BLACK)
        self.draw_text('Next Level, Get Ready', self.title_font, 100, RED, WIDTH / 2, HEIGHT / 2, align='center')
        self.draw_text('Press a Key to Play Again',self.title_font, 75, WHITE,
                        WIDTH / 2, HEIGHT /2 + 140, align='center')
        pg.display.flip()
        self.wait_for_key()


    def show_game_over_screen(self):
        # opens a game over screen
        self.screen.fill(BLACK)
        self.draw_text('GAME OVER', self.title_font, 100, RED, WIDTH / 2, HEIGHT / 2, align='center')
        self.draw_text('Press a Key to Play Again',self.title_font, 75, WHITE,
                        WIDTH / 2, HEIGHT /2 + 140, align='center')
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False



g = Game()

g.show_start_screen()
while g.running:
    g.new()
    g.run()
    g.show_game_over_screen()

pygame.quit()
