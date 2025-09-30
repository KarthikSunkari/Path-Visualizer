import pygame
import math
from Astar import Astar
from BFS import bfs
from DFS import dfs
from biBFS import bi_bfs

WIDTH = 700
UI_WIDTH = 350

pygame.init()
WIN = pygame.display.set_mode((WIDTH+UI_WIDTH, WIDTH))	# total rows=total columns
pygame.display.set_caption("Path Finding Visualizer")

NORTH = [0,1]
EAST = [1,0]
SOUTH = [0,-1]
WEST = [-1,0]

neighbors = [EAST,WEST,SOUTH,NORTH]

path_algo = (
	'A*',
	'BFS/Djkistra',
	'DFS',
	'Bi-directional BFS',
	'Quit',
)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
LIGHTBLUE = (64, 224, 208)
BLUE = (0, 0, 255)

class Node:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == LIGHTBLUE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_current(self):
		self.color = GREY

	def make_open(self):
		self.color = GREEN

	def make_white(self):
		self.color = WHITE

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = LIGHTBLUE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		for neighbor in neighbors:
			neighbor_row = self.row + neighbor[0]
			neighbor_col = self.col + neighbor[1]
			if neighbor_row < self.total_rows and neighbor_row >= 0 and \
				neighbor_col < self.total_rows and neighbor_col >= 0 and \
				not grid[neighbor_row][neighbor_col].is_barrier():
				self.neighbors.append(grid[neighbor_row][neighbor_col])

	def __lt__(self, other):
		return False


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i, j, gap, rows)
			grid[i].append(node)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE,(0, 0, WIDTH, WIDTH))

	for row in grid:
		for node in row:
			node.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

def drawUI(win):
	win.fill(GREY,(WIDTH, 0, WIDTH+UI_WIDTH, WIDTH))
	fontHeading = pygame.font.Font('freesansbold.ttf', 32)  
	font = pygame.font.SysFont('Times New Roman', 22)

	# Render the text in new surface  

	text = fontHeading.render("INFO:", True, WHITE)
	text1 = font.render("■ - source", True, ORANGE )
	text2 = font.render("■ - destination", True, LIGHTBLUE)
	text3 = font.render("■ - PATH", True, PURPLE)
	text4 = font.render("■ - closed nodes", True, RED  )
	text5 = font.render("■ - open nodes", True, GREEN )
	text6 = font.render("■ - barrier", True, BLACK)

	# copying the text surface object to the text surface object 
	win.blit(text,(WIDTH+12,0))
	win.blit(text1,(WIDTH+12,40))
	win.blit(text2,(WIDTH+12,60))
	win.blit(text3,(WIDTH+12,80))
	win.blit(text4,(WIDTH+12,100))
	win.blit(text5,(WIDTH+12,120))
	win.blit(text6,(WIDTH+12,140))

	text = fontHeading.render("INSTRUCTIONS:", True, BLACK)
	text6 = font.render("Left click to add BARRIERS", True, BLACK )
	text7 = font.render("Right click to remove BARRIERS", True, BLACK )
	text1 = font.render("Hit <space> to run Astar", True, BLACK )
	text2 = font.render("Hit 'b' to run BFS/Djkistra", True, BLACK)
	text3 = font.render("Hit 'i' to run Bi-directional BFS", True, BLACK)
	text4 = font.render("Hit 'd' to run DFS", True, BLACK)
	text5 = font.render("Hit 'c' to CLEAR", True, BLACK)

	win.blit(text,(WIDTH+12,200))
	win.blit(text6,(WIDTH+12,240))
	win.blit(text7,(WIDTH+12,260))
	win.blit(text1,(WIDTH+12,280))
	win.blit(text3,(WIDTH+12,300))
	win.blit(text2,(WIDTH+12,320))
	win.blit(text4,(WIDTH+12,340))
	win.blit(text5,(WIDTH+12,360))


def main(win, width):
	ROWS = 40
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	traverse = False
	while run:
		draw(win, grid, ROWS, width)

		drawUI(win)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			# if event.type == USEREVENT and event.code == 'MENU':
			# 	print('menu event: %s.%d: %s' % (e.name,e.item_id,e.text))

			if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
				
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				node = None
				if row<len(grid) and col<len(grid[0]):
					node = grid[row][col]


				if node and pygame.mouse.get_pressed()[0]: # LEFT
					if not start and node != end:
						start = node
						start.make_start()

					elif not end and node != start:
						end = node
						end.make_end()

					elif node != end and node != start:
						node.make_barrier()

				elif node and pygame.mouse.get_pressed()[2]: # RIGHT
					node.reset()
					if node == start:
						start = None
					elif node == end:
						end = None

			if event.type == pygame.KEYDOWN and start and end:
				

				if event.key == pygame.K_SPACE:
					
					for row in grid:
						for node in row:
							node.update_neighbors(grid)
					Astar(lambda: draw(win, grid, ROWS, width), grid, start, end)

				elif event.key == pygame.K_b:
					
					for row in grid:
						for node in row:
							node.update_neighbors(grid)
					bfs(lambda: draw(win, grid, ROWS, width), grid, start, end)

				elif event.key == pygame.K_d:
					
					for row in grid:
						for node in row:
							node.update_neighbors(grid)
					dfs(lambda: draw(win, grid, ROWS, width), grid, start, start, end)

				elif event.key == pygame.K_i:
					
					for row in grid:
						for node in row:
							node.update_neighbors(grid)
					bi_bfs(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

		pygame.display.update() 
	
	pygame.quit()

main(WIN, WIDTH)