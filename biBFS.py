import pygame
from queue import Queue
from Backtrack import reconstruct_path
    
def bi_bfs(draw, grid, start, end):
    discover_from_src = Queue()
    discover_from_dest = Queue()
    d1 = [[0]*len(grid) for _ in range(len(grid))] #dist from source
    d2 = [[0]*len(grid) for _ in range(len(grid))] #dist from destination
    parent1={}
    parent2={}
    visited1={start}
    visited2={end}
    discover_from_src.put(start)
    discover_from_dest.put(end)
    while(not discover_from_src.empty() and not discover_from_dest.empty()):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
        curr_src = discover_from_src.get()
        curr_dest = discover_from_dest.get()

        curr_row_dest, curr_col_dest = curr_dest.get_pos()
        curr_row_src, curr_col_src = curr_src.get_pos()

        if curr_src!= start:
            curr_src.make_current()

        if curr_dest!= end:
            curr_dest.make_current()

        draw()

        if curr_src in visited2:
            reconstruct_path(parent1, curr_src, start, draw)
            reconstruct_path(parent2, curr_src, end, draw)
            end.make_end()
            print(f"Shortest Path length {d1[curr_row_src][curr_col_src] + d2[curr_row_src][curr_col_src] -1}")
            return True

        if curr_dest in visited1:
            reconstruct_path(parent1, curr_dest, start, draw)
            reconstruct_path(parent2, curr_dest, end, draw)
            end.make_end()
            print(f"Shortest Path length {d1[curr_row_dest][curr_col_dest] + d2[curr_row_dest][curr_col_dest] -1}")
            return True

        for neighbor in curr_src.neighbors:
            neighbor_row, neighbor_col = neighbor.get_pos()

            if neighbor not in visited1:
                parent1[neighbor]=curr_src
                d1[neighbor_row][neighbor_col] = 1 + d1[curr_row_src][curr_col_src]
                discover_from_src.put(neighbor)
                visited1.add(neighbor)
                neighbor.make_open()

        for neighbor in curr_dest.neighbors:
            neighbor_row, neighbor_col = neighbor.get_pos()

            if neighbor not in visited2:
                parent2[neighbor]=curr_dest
                d2[neighbor_row][neighbor_col] = 1 + d2[curr_row_dest][curr_col_dest]
                discover_from_dest.put(neighbor)
                visited2.add(neighbor)
                neighbor.make_open()       

        draw()

        if curr_src!=start:
            curr_src.make_closed()

        if curr_dest!=end:
            curr_dest.make_closed()
        
    return False
