import pygame,time
from queue import Queue
from Backtrack import reconstruct_path
    
def bfs(draw, grid, start, end):
    discover = Queue()
    d = [[0]*len(grid) for _ in range(len(grid))] #dist from source
    parent={}
    visited={start}
    discover.put(start)
    while(not discover.empty()):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
        curr = discover.get()
        curr_row, curr_col = curr.get_pos()

        if curr!= start:
            curr.make_current()

        draw()

        if curr == end:
            reconstruct_path(parent, curr, start, draw)
            end.make_end()
            print(f"Shortest Path length {d[curr_row][curr_col]}")
            return True

        for neighbor in curr.neighbors:
            neighbor_row, neighbor_col = neighbor.get_pos()

            if neighbor not in visited:
                parent[neighbor]=curr
                d[neighbor_row][neighbor_col] = 1 + d[curr_row][curr_col]
                discover.put(neighbor)
                visited.add(neighbor)
                neighbor.make_open()
        # time.sleep(1)
        draw()

        if curr!=start:
            curr.make_closed()
        
    return False
