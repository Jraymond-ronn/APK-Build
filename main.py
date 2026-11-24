import os
os.environ["SDL_HINT_ORIENTATIONS"] = "LandscapeLeft LandscapeRight"
import pygame
from sys import exit
from random import randint

def random_color():
	return (randint(0, 255), randint(0, 255), randint(0, 255))

def display_score():
	global score_rect, score_surf
	time = int((pygame.time.get_ticks() / 1000) - start_time + bonus_score)
	score_surf = font.render(f"Score: {time}", False, score_color)
	score_rect = score_surf.get_rect(center = (400, 75))
	screen.blit(score_surf, score_rect)
	return time
	
def player_animation():
	global player_surf, player_index, player_mask
	if player_rect.bottom < 300:
		player_surf = player_jump
		player_index = 0
	else:
		player_index += 0.15
		if player_index >= len(player_frames):
			player_index = 0
		player_surf = player_frames[int(player_index)]
	player_mask = pygame.mask.from_surface(player_surf)
		
def obstacle_movement(obstacle_list):
	if obstacle_list:
		for obstacle_rect in obstacle_list:
			if obstacle_rect.width in (spike_surf.get_width(), cactus_surf.get_width()):
				obstacle_rect.x -= 6
			else:
				obstacle_rect.x -= 7
			if obstacle_rect.bottom < 300:
				screen.blit(fly_surf, obstacle_rect)
			elif obstacle_rect.width == spike_surf.get_width():
				screen.blit(spike_surf, obstacle_rect)
			elif obstacle_rect.width == cactus_surf.get_width():
				screen.blit(cactus_surf, obstacle_rect)
			else:
				screen.blit(snail_surf, obstacle_rect)
		obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
		return obstacle_list
	else: return []
	
def collisions(player, obstacles):
	if obstacles:
		for obstacle_rect in obstacles:
			if obstacle_rect.bottom < 300:
				obs_mask = fly_mask
			elif obstacle_rect.width == spike_surf.get_width():
				obs_mask = spike_mask
			elif obstacle_rect.width == cactus_surf.get_width():
				obs_mask = cactus_mask
			else:
				obs_mask = snail_mask
			offset = (obstacle_rect.x - player.x, obstacle_rect.y - player.y)
			if player_mask.overlap(obs_mask, offset): return False
	return True
	
def coin_blitting(coin_list):
	if coin_list:
		for coin in coin_list:
			coin["rect"].x -= 6
			screen.blit(coin["surf"], coin["rect"])
		coin_list = [coin for coin in coin_list if coin["rect"].x > -100]
		return coin_list
	else: return []
	
popups_list = []

def coin_collision(player, coins):
	global bonus_score
	if coins:
		for coin in coins[:]:
			if player.colliderect(coin["rect"]):
				bonus_score += coin["bonus"]
				coin_sound.play()

				star_copy = star_surf.copy()
				star_rect = star_copy.get_rect(center = coin["rect"].center)
				popups_list.append({"surf": star_copy, "rect": star_rect, "alpha": 255, "move_y": -1, "move_x": -6, "scale": 1.0, "grow": 0.005})

				text_surf = font.render(f"+{coin['bonus']}", False, "Gold")
				text_rect = text_surf.get_rect(midbottom = coin["rect"].midtop)
				popups_list.append({"surf": text_surf, "rect": text_rect, "alpha": 255, "move_y": -1, "move_x": -6, "scale": 1.0, "grow": 0})

				coins.remove(coin)

def popup_blitting(popup_list):
	if popup_list:
		for popup in popup_list[:]:
			popup["rect"].y += popup["move_y"] 
			popup["rect"].x += popup["move_x"]
			popup["alpha"] -= 7
			if popup["alpha"] <= 0:
				popup_list.remove(popup)
			else:
				if popup["grow"] > 0:
					old_center = popup["rect"].center
					scaled_surf = pygame.transform.rotozoom(popup["surf"], 0, popup["scale"])
					popup["rect"] = scaled_surf.get_rect(center = old_center)
					popup["scale"] += popup["grow"]
				else:
					scaled_surf = popup["surf"]
				popup["surf"].set_alpha(popup["alpha"])
				screen.blit(scaled_surf, popup["rect"])
		popup_list = [popup for popup in popup_list if popup["rect"].x > -100]
		return popup_list
	return []				

pygame.init()
game_w, game_h = 800, 400
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.Surface((game_w, game_h))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
font = pygame.font.Font("fonts/Pixeltype.ttf", 50)
game_active = False
start_time = 0
score = 0
bonus_score = 0
time = int(pygame.time.get_ticks() / 1000)

sky_x1 = 0
sky_x2 = 800
sky_surf = pygame.image.load("graphics/Sky.png").convert()
sky_surf2 = pygame.transform.flip(sky_surf, True, False)
ground_x1 = 0
ground_x2 = 800
ground_surf = pygame.image.load("graphics/ground.png").convert()
ground_surf2 = pygame.transform.flip(ground_surf, True, False)
bg_music = pygame.mixer.music.load("music/music.ogg")
pygame.mixer.music.play(loops = -1)

snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_frames = [snail_1, snail_2]
snail_index = 0
snail_surf = snail_frames[snail_index]

fly_1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
fly_2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
fly_frames = [fly_1, fly_2]
fly_index = 0
fly_surf = fly_frames[fly_index]

spike_surf = pygame.image.load("graphics/spike.png").convert_alpha()
cactus_surf = pygame.image.load("graphics/cactus.png").convert_alpha()

obstacle_rect_list = []

bronze_coin = pygame.image.load("graphics/coin/bronze_coin.png").convert_alpha()
silver_coin = pygame.image.load("graphics/coin/silver_coin.png").convert_alpha()
gold_coin = pygame.image.load("graphics/coin/gold_coin.png").convert_alpha()
coins_list = []
coin_sound = pygame.mixer.Sound("music/pickupCoin.wav")
coin_sound.set_volume(2.0)

star_surf = pygame.image.load("graphics/star.png").convert_alpha()

player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
stand_surf = pygame.transform.scale2x(player_stand)
ss_rect = stand_surf.get_rect(center = (400, 200))
player_walk1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_walk2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
player_frames = [player_walk1, player_walk2]
player_index = 0
player_surf = player_frames[int(player_index)]
player_rect = player_surf.get_rect(midbottom = (100, 300))
player_grav = 0
jump_sound = pygame.mixer.Sound("music/jump.wav")

score_color = (255, 255, 255)
game_name = font.render("Pixel Runner", False, "Light Green")
gn_rect = game_name.get_rect(center = (400, 75))
instruction = font.render("Press \"SPACE\" or click to start", False, "Green3")
instr_rect = instruction.get_rect(center = (400, 325))
game_over = font.render("Game Over!", False, "Light Green")
go_rect = game_over.get_rect(center = (400, 75))

player_mask = pygame.mask.from_surface(player_surf)
snail_mask = pygame.mask.from_surface(snail_surf)
fly_mask = pygame.mask.from_surface(fly_surf)
spike_mask = pygame.mask.from_surface(spike_surf)
cactus_mask = pygame.mask.from_surface(cactus_surf)

w, h = window.get_size()
scale = min(w / game_w, h / game_h)
scaled_size = (int(game_w * scale), int(game_h * scale))
offset_x = (w - scaled_size[0]) // 2
offset_y = (h - scaled_size[1]) // 2

random_timer = pygame.USEREVENT + 1
pygame.time.set_timer(random_timer, 350)
spawn_timer = pygame.USEREVENT + 2
pygame.time.set_timer(spawn_timer, 1400)
coin_timer = pygame.USEREVENT + 3
pygame.time.set_timer(coin_timer, 7700)
snail_animation = pygame.USEREVENT + 4
pygame.time.set_timer(snail_animation, 400)
fly_animation = pygame.USEREVENT + 5
pygame.time.set_timer(fly_animation, 250)

while True:
	for e in pygame.event.get():
		if game_active:
			if e.type == pygame.QUIT:
				pygame.quit()
				exit()
			if e.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= 300:
				player_grav -= 20
				jump_sound.play()
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_SPACE and player_rect.bottom >= 300:
					player_grav -= 20
					jump_sound.play()
				if e.key == pygame.K_F4 and (e.mod & pygame.KMOD_ALT):
					pygame.quit()
					exit()
			if e.type == random_timer:
				score_color = random_color()
			if e.type == snail_animation:
				if snail_index == 0: snail_index = 1 
				else: snail_index = 0
				snail_surf = snail_frames[snail_index]
				snail_mask = pygame.mask.from_surface(snail_surf)
			if e.type == fly_animation:
				if fly_index == 0: fly_index = 1
				else: fly_index = 0
				fly_surf = fly_frames[fly_index]
				fly_mask = pygame.mask.from_surface(fly_surf)
			if e.type == spawn_timer:
				random_number = randint(0, 5)
				if random_number == 1 or random_number == 2:
					new_obs = snail_surf.get_rect(midbottom = (randint(900, 1100), 300))
				elif random_number == 3:
					new_obs = spike_surf.get_rect(midbottom = (randint(900, 1100), 300))
				elif random_number == 4 or random_number == 5:
					new_obs = cactus_surf.get_rect(midbottom = (randint(900, 1100), 300))
				else:
					new_obs = fly_surf.get_rect(midbottom = (randint(900, 1100), 210))
					
				obs_safe = True
				if obstacle_rect_list:
					last_obs = obstacle_rect_list[-1]
					if new_obs.x - last_obs.right < 320:
						obs_safe = False
				coin_safe = True
				for coin in coins_list:
					c_rect = coin["rect"]
					danger_zone = pygame.Rect(c_rect.x - 100, 0, c_rect.width + 450, 400)
					if danger_zone.colliderect(new_obs):
						coin_safe = False
						break
				if coin_safe and obs_safe:
					obstacle_rect_list.append(new_obs)
			if e.type == coin_timer:
				coin_y = 210 if randint(0, 2) else 300
				random_number = randint(0, 3)
				if random_number == 0 or random_number == 1:
					surf, bonus = bronze_coin, 3
				elif random_number == 2:
					surf, bonus = silver_coin, 5
				else:
					surf, bonus = gold_coin, 7
				new_rect = surf.get_rect(midbottom = (randint(900, 1100), coin_y))
				safe_zone = pygame.Rect(new_rect.x - 350, 0, new_rect.width + 700, 400)
				if not any(safe_zone.colliderect(obs) for obs in obstacle_rect_list):
					coins_list.append({"rect": new_rect, "surf": surf, "bonus": bonus})
		else:
			if e.type == pygame.QUIT:
				pygame.quit()
				exit()
			if e.type == pygame.MOUSEBUTTONDOWN:
				game_active = True
				start_time = int(pygame.time.get_ticks() / 1000)
				bonus_score = 0
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_SPACE:
					game_active = True
					start_time = int(pygame.time.get_ticks() / 1000)
					bonus_score = 0
				if e.key == pygame.K_F4 and (e.mod & pygame.KMOD_ALT):
					pygame.quit()
					exit()
					
	if game_active:
		sky_x1 -= 0.3
		sky_x2 -= 0.3
		if sky_x1 <= -800: sky_x1 = 800
		if sky_x2 <= -800: sky_x2 = 800
		screen.blit(sky_surf, (int(sky_x1), 0))
		screen.blit(sky_surf2, (int(sky_x2), 0))
		ground_x1 -= 6
		ground_x2 -= 6
		if ground_x1 <= -800: ground_x1 = 800
		if ground_x2 <= -800: ground_x2 = 800
		screen.blit(ground_surf, (ground_x1, 300))
		screen.blit(ground_surf2, (ground_x2, 300))
		score = display_score()
		player_animation()
		player_grav += 1
		player_rect.y += player_grav
		if player_rect.bottom >= 300:
			player_rect.bottom = 300
			player_grav = 0
		screen.blit(player_surf, player_rect)
		obstacle_rect_list = obstacle_movement(obstacle_rect_list)
		coins_list = coin_blitting(coins_list)
		coin_collision(player_rect, coins_list)
		popups_list = popup_blitting(popups_list)
		game_active = collisions(player_rect, obstacle_rect_list)
	else:
		screen.fill((94, 129, 162))
		obstacle_rect_list.clear()
		coins_list.clear()
		popups_list.clear()
		player_rect.bottom = 300
		screen.blit(stand_surf, ss_rect)
		score_message = font.render(f"Score: {score}", False, "Green3")
		sm_rect = score_message.get_rect(center = (400, 325))
		if score == 0:
			screen.blit(game_name, gn_rect)
			screen.blit(instruction, instr_rect)
		else:
			screen.blit(score_message, sm_rect)
			screen.blit(game_over, go_rect)
	
	window.blit(pygame.transform.scale(screen, scaled_size), (offset_x, offset_y))		
	pygame.display.flip()
	clock.tick(60)