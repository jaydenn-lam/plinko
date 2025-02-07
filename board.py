from goal import *
from obstacles import *
from settings import *
import pygame, pymunk

class Board():
    def __init__(self, space):
        self.space = space
        self.display_surface = pygame.display.get_surface()

        # logo
        self.logo = pygame.image.load("graphics/logo.png").convert_alpha()
        self.logo = pygame.transform.scale(self.logo, (80,80))
        self.logo_rect = self.logo.get_rect(topleft = (20,20))

        # ball counter
        self.ball_count = 0
        self.counter_font = pygame.font.Font("graphics/starborn/Starborn.ttf", 24)

        # font
        self.font = pygame.font.Font("graphics/starborn/Starborn.ttf", 18)

        # reset button
        self.clear_button_color = BROWN 
        self.clear_button_hover_color = DARK_BROWN  
        self.clear_button_rect = pygame.Rect(WIDTH // 2 - 180, HEIGHT - 130, 160, 80)
        self.clear_button_text = self.font.render("CLEAR", True, (255, 255, 255))
        self.clear_text_rect = self.clear_button_text.get_rect(center=self.clear_button_rect.center)
        self.is_clear_hover = False

        # drop button
        self.drop_button_color = BROWN
        self.drop_button_hover_color = DARK_BROWN
        self.drop_button_rect = pygame.Rect(self.clear_button_rect.right + 40, HEIGHT - 130, 160, 80)
        self.drop_button_text = self.font.render("DROP", True, (255, 255, 255))
        self.drop_text_rect = self.drop_button_text.get_rect(center=self.drop_button_rect.center)
        self.is_drop_hover = False

        self.pressing_play = True

        # Obstacles
        self.curr_row_count = 3
        self.final_row_count = 10
        self.obstacles_list = []
        self.obstacle_sprites = pygame.sprite.Group()
        self.updated_coords = OBSTACLE_START

        # Get second point for segmentA
        self.segmentA_2 = OBSTACLE_START
        while self.curr_row_count <= self.final_row_count:
            for i in range(self.curr_row_count):
                # Get first point for segmentB
                if self.curr_row_count == 3 and self.updated_coords[0] > OBSTACLE_START[0] + OBSTACLE_PAD:
                    self.segmentB_1 = self.updated_coords
                # Get first point for segmentA
                elif self.curr_row_count == self.final_row_count and i == 0:
                    self.segmentA_1 = self.updated_coords
                # Get second point for segmentB
                elif self.curr_row_count == self.final_row_count and i == self.curr_row_count - 1:
                    self.segmentB_2 = self.updated_coords
                self.obstacles_list.append(self.spawn_obstacle(self.updated_coords, self.space))
                self.updated_coords = (int(self.updated_coords[0] + OBSTACLE_PAD), self.updated_coords[1])
            self.updated_coords = (int(WIDTH - self.updated_coords[0] + (.5 * OBSTACLE_PAD)), int(self.updated_coords[1] + OBSTACLE_PAD))
            self.curr_row_count += 1
        self.multi_x, self.multi_y = self.updated_coords[0] + OBSTACLE_PAD, self.updated_coords[1]

        # Segments (boundaries on side of obstacles)
        self.spawn_segments(self.segmentA_1, self.segmentA_2, self.space)
        self.spawn_segments(self.segmentB_1, self.segmentB_2, self.space)
        # Segments at top of obstacles
        self.spawn_segments((self.segmentA_2[0], 0), self.segmentA_2, self.space)
        self.spawn_segments(self.segmentB_1, (self.segmentB_1[0], 0), self.space)

        # Spawn multis
        self.spawn_multis()

    def draw_cup(self):
        # screen dimension
        screen_width, screen_height = self.display_surface.get_size()

        # Cup dimensions
        cup_width = 650
        cup_height = 660
        cup_x = (screen_width - cup_width) // 2
        cup_y = 250

        # Lid dimensions
        lid_height = 120
        lid_y = cup_y - lid_height

        # Straw dimensions
        straw_width = 100
        straw_height = 100
        straw_x = cup_x + cup_width // 2 - straw_width // 2
        straw_y = lid_y - straw_height

        # Draw the cup body
        pygame.draw.polygon(self.display_surface, MILK_TEA, [(cup_x, cup_y), (cup_x + cup_width, cup_y), 
                                    (cup_x + cup_width - 50, cup_y + cup_height - 80), 
                                    (cup_x + cup_width - 120, cup_y + cup_height),
                                    (cup_x + 120, cup_y + cup_height), 
                                    (cup_x + 50, cup_y + cup_height - 80)])
    
        # Draw the lid
        pygame.draw.rect(self.display_surface, BROWN, (cup_x - 50, lid_y, cup_width + 100, lid_height), border_radius = 10)


        # Draw the straw
        pygame.draw.rect(self.display_surface, STRAW, (straw_x, straw_y, straw_width, straw_height), border_top_left_radius = 5, border_top_right_radius = 5)

        # Draw the lid's top border
        pygame.draw.rect(self.display_surface, DARK_BROWN, (cup_x - 65, lid_y + 30, cup_width + 130, lid_height - 20), border_radius = 10)
    
    def draw_counter(self):
        counter_text = self.counter_font.render(f"BALLS DROPPED: {self.ball_count}", True, BROWN)
        self.display_surface.blit(counter_text, (100, 600))

    def draw_buttons(self):
        clear_color = self.clear_button_hover_color if self.is_clear_hover else self.clear_button_color
        pygame.draw.rect(self.display_surface, clear_color, self.clear_button_rect, border_radius = 25)
        self.display_surface.blit(self.clear_button_text, self.clear_text_rect)

        drop_color = self.drop_button_hover_color if self.is_drop_hover else self.drop_button_color
        pygame.draw.rect(self.display_surface, drop_color, self.drop_button_rect, border_radius = 25)
        self.display_surface.blit(self.drop_button_text, self.drop_text_rect)


    def draw_obstacles(self, obstacles):
        for obstacle in obstacles:
            pos_x, pos_y = int(obstacle.body.position.x), int(obstacle.body.position.y)
            pygame.draw.circle(self.display_surface, (255, 255, 255), (pos_x, pos_y), OBSTACLE_RAD)

    # Used to give a border radius to previous multi display on right side
    def draw_prev_multi_mask(self):
        multi_mask_surface = pygame.Surface((WIDTH / 4, HEIGHT), pygame.SRCALPHA)
        multi_mask_surface.fill(BG_COLOR)
        right_side_of_board = (WIDTH / 16) * 13
        right_side_pad = right_side_of_board / 130
        mask_y = (HEIGHT / 4) + ((HEIGHT / 4) / 9)
        pygame.draw.rect(multi_mask_surface, (0, 0, 0, 0), (right_side_pad, mask_y, SCORE_RECT, SCORE_RECT * 4), border_radius=30)
        self.display_surface.blit(multi_mask_surface, (right_side_of_board, 0))

    def spawn_multis(self):
        self.multi_amounts = [val[1] for val in multi_rgb.keys()]
        self.rgb_vals = [val for val in multi_rgb.values()]
        for i in range(NUM_MULTIS):
            multi = Multi((self.multi_x, self.multi_y), self.rgb_vals[i], self.multi_amounts[i])
            multi_group.add(multi)
            self.multi_x += OBSTACLE_PAD

    def spawn_obstacle(self, pos, space):
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position = pos
        body.friction = 0.6
        shape = pymunk.Circle(body, OBSTACLE_RAD)
        shape.elasticity = 0.4
        shape.filter = pymunk.ShapeFilter(categories=OBSTACLE_CATEGORY, mask=OBSTACLE_MASK)
        self.space.add(body, shape)
        obstacle = Obstacle(body.position.x, body.position.y)
        self.obstacle_sprites.add(obstacle)
        return shape

    def spawn_segments(self, pointA, pointB, space):
        segment_body = pymunk.Body(body_type = pymunk.Body.STATIC)
        segment_shape = pymunk.Segment(segment_body, pointA, pointB, 5) # radius = 5
        self.space.add(segment_body, segment_shape)

    def update(self):
        self.display_surface.blit(self.logo, self.logo_rect)
        self.draw_cup()
        self.draw_obstacles(self.obstacles_list)
        multi_group.draw(self.display_surface)
        multi_group.update()
        self.draw_buttons()
        self.draw_counter()

        if len(list(prev_multi_group)) > 0:
            prev_multi_group.update()
        if len(list(animation_group)) > 0:
            animation_group.update()
        self.draw_prev_multi_mask()

    def handle_clear_button(self, mouse_pos):
        if self.clear_button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]: 
            self.is_clear_hover = True
            self.ball_count = 0 
            return True
        self.is_clear_hover = False
        return False
    
    def handle_drop_button(self, mouse_pos):
        if self.drop_button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]: 
            self.is_drop_hover = True
            self.increment_ball_count()
            return True
        self.is_drop_hover = False
        return False
    
    def increment_ball_count(self):
        self.ball_count += 1

