import pygame,time
from collections import deque 
from Backtrack import reconstruct_path

parent = {}
visited = set()

def dfs(draw, grid, curr, start, end):

    if curr == end:
        return True
    
    if curr!= start:
        curr.make_current()
    visited.add(curr)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    draw()

    for neighbor in curr.neighbors:
        if curr!= start:
            curr.make_open()
        if neighbor not in visited:
            parent[neighbor]=curr
            if neighbor == end:
                reconstruct_path(parent, neighbor, start, draw)
                return True
            if dfs(draw, grid, neighbor,start, end):
                return True

    if curr!= start:
        curr.make_white()

    draw()
    return False


