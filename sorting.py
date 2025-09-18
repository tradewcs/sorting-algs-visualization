import logging
import math
import pygame
from draw_information import *

INSERTION_SORT_THRESHOLD = 16

def insertion_sort(draw_info: DrawInformation, begin=0, end=None):
    lst = draw_info.lst
    if end is None:
        end = len(lst) - 1

    for i in range(begin + 1, end + 1):
        j = i
        tmp = lst[j]
        while j > begin and lst[j - 1] > tmp:
            lst[j] = lst[j - 1]
            j -= 1
            lst[j] = tmp
            if draw_list(draw_info, color_positions={j - 1: draw_info.GREEN, j: draw_info.BLUE}, clear_bg=True) is False:
                return False

    if go_through(draw_info, begin, end, color=draw_info.GREEN) is False:
        return False
    return True

def partition(draw_info: DrawInformation, begin=0, end=None):
    lst = draw_info.lst
    if end is None:
        end = len(lst) - 1
    if begin >= end:
        return None

    pivot = begin
    for i in range(begin, end):
        if lst[i] <= lst[end]:
            lst[i], lst[pivot] = lst[pivot], lst[i]
            pivot += 1
            if draw_list(draw_info, color_positions={i: draw_info.CYAN, pivot: draw_info.GREEN_CYAN}, clear_bg=True) is False:
                return None
        if draw_list(draw_info, color_positions={i: draw_info.CYAN, end: draw_info.BLUE}, clear_bg=True) is False:
            return None

    lst[pivot], lst[end] = lst[end], lst[pivot]
    return pivot

def quick_sort(draw_info: DrawInformation, begin=0, end=None):
    if end is None:
        end = len(draw_info.lst) - 1
    if begin >= end:
        return True

    pivot = partition(draw_info, begin, end)
    if pivot is None:
        return False

    if quick_sort(draw_info, begin, pivot - 1) is False:
        return False
    if quick_sort(draw_info, pivot + 1, end) is False:
        return False

    if go_through(draw_info, begin, end, color=(100, 255, 255)) is False:
        return False
    return True

def heapify(draw_info: DrawInformation, begin, end, i):
    if begin >= end or begin < 0:
        return True

    logging.debug(f'draw_info: {begin}, {end}, {i}')
    lst = draw_info.lst
    left = 2 * (i - begin) + 1 + begin
    right = left + 1
    swap = i

    if left <= end and lst[left] > lst[swap]:
        swap = left
    if right <= end and lst[right] > lst[swap]:
        swap = right

    if swap != i:
        lst[i], lst[swap] = lst[swap], lst[i]
        if heapify(draw_info, begin, end, swap) is False:
            return False
        if draw_list(draw_info, color_positions={swap: draw_info.CYAN, i: draw_info.RED}, clear_bg=True) is False:
            return False
    return True

def make_heap(draw_info, begin, end):
    for i in reversed(range(begin, (end - begin + 1) // 2 + begin)):
        if heapify(draw_info, begin, end, i) is False:
            return False
    return True

def heap_sort(draw_info, begin=0, end=None):
    lst = draw_info.lst
    if end is None:
        end = len(lst) - 1

    if make_heap(draw_info, begin, end) is False:
        return False

    for i in reversed(range(begin, end + 1)):
        lst[i], lst[begin] = lst[begin], lst[i]
        if heapify(draw_info, begin, i - 1, begin) is False:
            return False

    if go_through(draw_info, begin, end, color=(255, 100, 100)) is False:
        return False
    return True

def introsort_rec(draw_info, begin=0, end=None, maxdepth=20):
    if end is None:
        end = len(draw_info.lst) - 1

    if end - begin < INSERTION_SORT_THRESHOLD:
        if insertion_sort(draw_info, begin, end) is False:
            return False
    elif maxdepth <= 0:
        if heap_sort(draw_info, begin, end) is False:
            return False
    else:
        pivot = partition(draw_info, begin, end)
        if pivot is None:
            return False
        if introsort_rec(draw_info, begin, pivot - 1, maxdepth - 1) is False:
            return False
        if introsort_rec(draw_info, pivot + 1, end, maxdepth - 1) is False:
            return False

    if go_through(draw_info, begin, end, color=(80, 0, 255)) is False:
        return False
    return True

def intro_sort(draw_info, begin=0, end=None):
    if end is None:
        end = len(draw_info.lst) - 1
    maxdepth = int(2 * math.log2(end - begin + 1))
    return introsort_rec(draw_info, begin, end, maxdepth)

def main():
    clock = pygame.time.Clock()
    logging.basicConfig(level=logging.DEBUG)
    n = 100
    lst = generate_starting_list(n)
    print(lst)
    clock_tick = 100
    draw_info = DrawInformation(1000, 750, lst, clock_tick=clock_tick)
    sorting_algorithm = heap_sort
    sorting_algo_name = "Heap Sort"
    draw(draw_info, sorting_algo_name)
    run = True
    sorting_in_progress = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generate_starting_list(n)
                draw_info.set_list(lst)
                sorting_in_progress = False
                draw(draw_info, sorting_algo_name)
            elif event.key == pygame.K_SPACE:
                if not sorting_in_progress:
                    sorting_in_progress = True
                    sorting_algorithm(draw_info)
                    sorting_in_progress = False
                    draw(draw_info, sorting_algo_name)
            elif event.key == pygame.K_i:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
                draw(draw_info, sorting_algo_name)
            elif event.key == pygame.K_h:
                sorting_algorithm = heap_sort
                sorting_algo_name = "Heap Sort"
                draw(draw_info, sorting_algo_name)
            elif event.key == pygame.K_q:
                sorting_algorithm = quick_sort
                sorting_algo_name = "Quick Sort"
                draw(draw_info, sorting_algo_name)
            elif event.key == pygame.K_d:
                sorting_algorithm = intro_sort
                sorting_algo_name = "Intro Sort"
                draw(draw_info, sorting_algo_name)
    pygame.quit()
    print(lst)

if __name__ == '__main__':
    main()