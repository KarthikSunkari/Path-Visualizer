from queue import PriorityQueue
from Backtrack import reconstruct_path
import pygame,time

def h(p1, p2): #Heuristuc Function
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2) #Manhattan Distance


def Astar(draw, grid, start, end):
	discover = PriorityQueue()
	discover.put((0, 0, start))
	visited = {start}
	parent = {}
	count = 0
	g_score = [[float("inf")]*len(grid) for _ in range(len(grid))]
	row, col = start.get_pos()
	g_score[row][col] = 0
	f_score = [[float("inf")]*len(grid) for _ in range(len(grid))]
	f_score[row][col] = h(start.get_pos(), end.get_pos())

	while not discover.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = discover.get()[2]
		curr_row, curr_col = current.get_pos()
		if current!= start:
			current.make_current()

		if current == end:
			reconstruct_path(parent, end, start, draw)
			end.make_end()
			print(f"Shortest Path length = {g_score[curr_row][curr_col]}")
			return True
			
		for neighbor in current.neighbors:

			temp_g_score = g_score[curr_row][curr_col] + 1
			neighbor_row, neighbor_col = neighbor.get_pos()
			
			if neighbor not in visited:

				if temp_g_score < g_score[neighbor_row][neighbor_col]:
					parent[neighbor] = current
					count+=1
					g_score[neighbor_row][neighbor_col] = temp_g_score
					f_score[neighbor_row][neighbor_col] = temp_g_score + h(neighbor.get_pos(), end.get_pos()) # normal distance + estimated distance
					discover.put((f_score[neighbor_row][neighbor_col], count, neighbor))
					neighbor.make_open()
					visited.add(neighbor)
		# time.sleep(0.5)
		draw()

		if current != start:
			current.make_closed()

	return False

