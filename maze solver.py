import turtle
import copy



''' 
* Significant turning points:
    1) this is where there is a turning point and
       and there is more than 1 open part.
    2) make sure to capture those significant turning points.
    
    
    download when system says it cannot detect tkinder
    # sudo apt-get install python3-tkinter
'''


#~~~~~~~~~~~~~~~~~~~~~~~~~ Maze creation ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

maze = [
    '####################  X                   #',
    '################ ######################## #',
    '################  ####### ############### #',
    '################  #######                 #',
    '################  ####### #### ########## #',
    '################  ####### ####  ######### #',
    '####    ########  ####### ##### ######### #',
    '   #                            ######### #',
    ' ############################ ##########   ',
    ' ###############     O         ######### # ',
    ' ##############  #######################   ',
    ' ####            ######## #### ########## #',
    ' #### ########## ######## #### ########## #',
    ' ############### ######## #### ##########  ',
    ' ############### ######## #### ##########  ',
    'X     ########## ########  ### ##########  ',
    '#####                                      ',
    '########### ############ ############### # ',
    '########################X############### #X',
]

# maze = [
#     'X ########O ##',
#     '# #      ##  #',
#     '#   # ## ### #',
#     '# # #  # ### #',
#     '# #          #',
#     '# # ##########',
# ]

 
for maze_print in maze:
    print(maze_print)


#~~~~~~~~~~~~~~~~~~~~~~~~~ Setting up Start ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


def path_list():
    
    paths = []
    return paths


def temp_list():
    """ 
    * this function creates a temp list that is used to add the accumulated coordincates
      for every step that is taken.
    * after the steps taken have been used they are then removed from the list.
    """
    
    temp = []
    return temp


def maze_listed():
    ''' 
    * transforms maze into a listed form
    '''

    starting_maze = [] # maze into list
    new_maze = [] # populated using all paths possible
    final_maze = [] # used to print clean maze and populate maze with final path after clean print
    
    for row in maze:
        starting_maze.append(list(map(lambda x: x, row)))
        
    for row in maze:
        new_maze.append(list(map(lambda x: x, row)))

    for row in maze:
        final_maze.append(list(map(lambda x: x, row)))
    
    return starting_maze, new_maze, final_maze


def starting_using_input(end, starting_maze):

    possible_options = ['mazerun top', 'mazerun left', 'mazerun right', 'mazerun bottom']
    
    print('\nPossible Commands: ')
    i = 1
    for command in possible_options:
        print(f'{i}: {command}')
        i = i + 1
    user_input = input('\nWhere do you want me to end up: ')

    while user_input not in possible_options:
        print('Try again!')
        user_input = input('\nWhere do you want me to start: ')

    if user_input == 'mazerun top':
        index = starting_maze[0].index('X')
        end = (0, index)
        return end

    elif user_input == 'mazerun left':
        for i in range(len(starting_maze)):
            if starting_maze[i][0] == 'X':
                end = (i, 0)
                return end

    elif user_input == 'mazerun right':
        for i in range(len(starting_maze)):
            if starting_maze[i][len(starting_maze[i]) - 1] == 'X':
                end = (i, (len(starting_maze[i]) - 1))
                return end

    elif user_input == 'mazerun bottom':
        index = starting_maze[-1].index('X')
        end = (len(starting_maze) - 1, index)
        return end

def find_start_and_end(starting_maze):
    ''' 
    * function finds the start and end point
    * start and end are 'O' and 'X'.
    '''
    
    start = None
    end = None
    for row in starting_maze:
        for char in row:
            if char == 'O':
                start = (starting_maze.index(row), row.index(char))
        if 'O' in row:
            break
            
    for row in starting_maze:
        for char in row:
            if char == 'X':
                end = (starting_maze.index(row), row.index(char))
        if 'X' in row:
            break
                
    return [start, end]


def set_up_printing(start, end):

    row_length = len(maze[0])
    column_length = len(maze)
    print('\nStart: ' + str(start))
    print('End: ' + str(end))
    print('Row Length: ' + str(row_length))
    print('Column Length: ' + str(column_length))

    return row_length, column_length


#~~~~~~~~~~~~~~~~~~~~~~~~~ The Logic Part ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


def obst_forward_check(starting_maze, current_pos, temp):
    ''' 
    * checks if forward  movement is valid
    '''
    final_forward = None
    move_count = 0
    # + 2 because count starts at 0 and not 1
    if (current_pos[0] + 2) == (len(starting_maze) + 1): 
        return False, move_count, final_forward
    
    if starting_maze[current_pos[0] + 1][current_pos[1]] == '#':
        return False, move_count, final_forward
    elif starting_maze[current_pos[0] + 1][current_pos[1]] == '*':
        return None, move_count, final_forward
    elif starting_maze[current_pos[0] + 1][current_pos[1]] == 'O':
        return None, move_count, final_forward
    else:
        move_count += 1
        temp.append((current_pos[0] + 1, current_pos[1]))
        final_forward = (current_pos[0] + 1, current_pos[1])
        return True, move_count, final_forward


def obst_back_check(starting_maze, current_pos, temp):
    ''' 
    * checks if back movement is valid
    '''
    
    final_back = None
    move_count = 0
    if (current_pos[0] - 1) == -1:
        return False, move_count, final_back
    
    if starting_maze[current_pos[0] - 1][current_pos[1]] == '#':
        return False, move_count, final_back
    elif starting_maze[current_pos[0] - 1][current_pos[1]] == '*':
        return None, move_count, final_back
    elif starting_maze[current_pos[0] - 1][current_pos[1]] == 'O':
        return None, move_count, final_back
    else:
        move_count += 1
        temp.append((current_pos[0] - 1, current_pos[1]))
        final_back = (current_pos[0] - 1, current_pos[1])
        return True, move_count, final_back
    

def obst_left_check(starting_maze, current_pos, temp):
    ''' 
    * checks if left movement is valid
    '''
    
    final_left = None
    move_count = 0
    if (current_pos[1] - 1) == -1:
        return False, move_count, final_left
    
    if starting_maze[current_pos[0]][current_pos[1] - 1] == '#':
        return False, move_count, final_left
    elif starting_maze[current_pos[0]][current_pos[1] - 1] == '*':
        return None, move_count, final_left
    elif starting_maze[current_pos[0]][current_pos[1] - 1] == 'O':
        return None, move_count, final_left
    else:
        move_count += 1
        temp.append((current_pos[0], current_pos[1] - 1))
        final_left = (current_pos[0], current_pos[1] - 1)
        return True, move_count, final_left
   
    
def obst_right_check(starting_maze, current_pos, temp):
    ''' 
    * checks if right movement is valid
    '''
    final_right = None
    move_count = 0
    if (current_pos[1] + 2) == (len(starting_maze[0]) + 1):
        return False, move_count, final_right
    
    if starting_maze[current_pos[0]][current_pos[1] + 1] == '#':
        return False, move_count, final_right
    elif starting_maze[current_pos[0]][current_pos[1] + 1] == '*':
        return None, move_count, final_right
    elif starting_maze[current_pos[0]][current_pos[1] + 1] == 'O':
        return None, move_count, final_right
    else:
        move_count += 1
        temp.append((current_pos[0], current_pos[1] + 1))
        final_right = (current_pos[0], current_pos[1] + 1)
        return True, move_count, final_right


def path_action(starting_maze, start, end, paths, temp):
    """ 
    * the function implemenets all the movement check functions and 
      makes movements based on the boolean return from the movement checks.
    * the path_track looks at the number of open tracks that the program has to consider
      when at a specific point (Wherever there are multiple turns).
    * when there is more than 1 track open, the function multiple_turn_consideration 
      gets called.
    * any none '#' value is populated with a '*' in new_maze while following a path 
      that leads to the end.
    """
    
    if len(paths) == 0:
        paths.append([start])
    
    for avail_path in paths:
        forward_check, f_count, final_forward = obst_forward_check(starting_maze, avail_path[-1], temp)
        back_check, b_count, final_back = obst_back_check(starting_maze, avail_path[-1], temp)
        left_check, l_count, final_left = obst_left_check(starting_maze, avail_path[-1], temp)
        right_check, r_count, final_right = obst_right_check(starting_maze, avail_path[-1], temp)
        
        path_track = f_count + b_count + l_count + r_count
        
        if path_track > 1:
            multiple_turn_consideration(avail_path, end, paths, temp, starting_maze)
            path_action(starting_maze, start, end, paths, temp)
            return 1
        
        position = paths.index(avail_path)
        if forward_check == True:
            paths[position].append(final_forward)
            starting_maze[final_forward[0]][final_forward[1]] = '*'
        if back_check == True:
            paths[position].append(final_back)
            starting_maze[final_back[0]][final_back[1]] = '*'
        if left_check == True:
            paths[position].append(final_left)
            starting_maze[final_left[0]][final_left[1]] = '*'
        if right_check == True:
            paths[position].append(final_right)
            starting_maze[final_right[0]][final_right[1]] = '*'
        
        pop_temp_list(temp)
        

def multiple_turn_consideration(avail_path, end, paths, temp, starting_maze):
    """ 
    * this function focuses on multiple turns that have to be
      made by the robot.
    * if the robot has to turn in multiple paths then 2 or more new
      paths are created.
    * in that the orginal available path that leads to multiple opennings ends
      up getting pop from the paths list.
    """
    
    for co_ord in temp:
        new_array = copy.copy(avail_path)
        new_array.append(co_ord)
        paths.append(new_array)
        
    for tuple in temp:
        starting_maze[tuple[0]][tuple[1]] = '*'
        if tuple == end:
            return 1
    
    position = paths.index(avail_path)
    paths.pop(position)
    pass


def pop_temp_list(temp):
    """ 
    * pops tuples that are inside of the list to create space for the
      the next step.
    """
    
    for i in range(len(temp)):
            temp.pop(0)


def movement_details(row_length):

    steps_moved = 12
    x_start = -((row_length/2) * steps_moved)
    y_start = 200

    return steps_moved, x_start, y_start


def draw_maze(final_pathed_maze, x_start, y_start, steps_moved):
    """
    * this function draws the maze using turtle.
    """

    visual_maze = turtle.Turtle()
    visual_maze.hideturtle()
    visual_maze.penup()
    visual_maze.speed(100)
    visual_maze.setposition(x_start, y_start)
    x = x_start
    y = y_start

    for row in final_pathed_maze:
        for char in row:
            visual_maze.begin_fill()

            if char == ' ':
                visual_maze.penup()
                pass

            elif char == '#':
                visual_maze.pendown()
                visual_maze.fillcolor('black')
                for i in range(4):
                    visual_maze.forward(steps_moved)
                    visual_maze.left(90)
                visual_maze.end_fill()

            elif char == 'X':
                visual_maze.pendown()
                visual_maze.fillcolor('red')
                for i in range(4):
                    visual_maze.forward(steps_moved)
                    visual_maze.left(90)
                visual_maze.end_fill()

            elif char == 'O':
                visual_maze.pendown()
                visual_maze.fillcolor('green')
                for i in range(4):
                    visual_maze.forward(steps_moved)
                    visual_maze.left(90)
                visual_maze.end_fill()

            elif char == '*':
                visual_maze.pendown()
                visual_maze.fillcolor('blue')
                for i in range(4):
                    visual_maze.forward(steps_moved)
                    visual_maze.left(90)
                visual_maze.end_fill()

            x = x + steps_moved
            visual_maze.goto(x, y)  
        
        x = x_start
        y = y - steps_moved
        visual_maze.penup()
        visual_maze.goto(x, y)


def fill_maze(final_path, start, x_start, y_start, steps_moved):
    """ 
    * the function is used to fill the path that lead to the end point.
    * this foucses on the user interface.
    """

    player = turtle.Turtle()
    player.hideturtle()
    player.speed(100)
    player.penup()
    player.setposition(x_start + (start[1] * steps_moved), y_start - (start[0] * steps_moved))

    # The first part fills the start block.
    player.begin_fill()
    player.fillcolor('blue')
    player.pendown()
    for i in range(4):
        player.forward(steps_moved)
        player.left(90)
    player.end_fill()

    previous_coord = 0

    for coordinate in final_path:
        
        player.begin_fill()
        player.fillcolor('blue')
        if coordinate == start:
            pass

        elif previous_coord[0] == coordinate[0] and previous_coord[1] < coordinate[1]:
            player.fillcolor('blue')
            player.forward(steps_moved)

            for i in range(4):
                player.forward(steps_moved)
                player.left(90)
            player.end_fill()

        elif previous_coord[0] == coordinate[0] and previous_coord[1] > coordinate[1]:
            player.fillcolor('blue')
            player.back(steps_moved)

            for i in range(4):
                player.forward(steps_moved)
                player.left(90)
            player.end_fill()

        elif previous_coord[0] < coordinate[0]:
            player.fillcolor('blue')
            player.right(90)
            player.forward(steps_moved)
            player.left(90)

            for i in range(4):
                player.forward(steps_moved)
                player.left(90)
            player.end_fill()

        elif previous_coord[0] > coordinate[0]:
            player.fillcolor('blue')
            player.left(90)
            player.forward(steps_moved)
            player.right(90)

            for i in range(4):
                player.forward(steps_moved)
                player.left(90)
            player.end_fill()

        previous_coord = coordinate


def run_maze():
    """ 
    * run maze starts the process of solving the maze.
    """

    #~~~~~~~~~~~~~~~~~~~~~~~ Initialize variables to use ~~~~~~~~~~~~~~~~~~~~~~~~#

    paths = path_list()
    temp = temp_list()
    starting_maze, new_maze, final_maze = maze_listed()
    start, end = find_start_and_end(starting_maze)
    end = starting_using_input(end, starting_maze)
    row_length, column_length = set_up_printing(start, end)
    final_path = None
    steps_moved, x_start, y_start = movement_details(row_length)


    while True:

        path_action(starting_maze, start, end, paths, temp) # this function runs all the logic functions
        
        """ 
        * the condtional looks to populate the final_maze with the final path that includes
          the start and end point.
        """
        if starting_maze[end[0]][end[1]] == '*':
            i = 0
            for path in paths:
                if end in path:
                    while len(path) != (path.index(end) + 1): # removes everthing that comes after the 'end' var. 
                        path.pop(-1)
                    
                    for tuple in path:
                        new_maze[tuple[0]][tuple[1]] = '*'

                    final_path = path
                    if i == 0:
                        print('Path Length: ' + str(len(path)) + '\n')
                        i += 1

            draw_maze(final_maze, x_start, y_start, steps_moved)

            i = 1
            for path in paths:
                print(f'\n{i}: {path}')

                if path == paths[-1]:
                    print('\n')
                i += 1

            for row in new_maze:
                print(''.join(row))

            fill_maze(final_path, start, x_start, y_start, steps_moved)

            close = input("\nType OFF: ").lower()

            while close != 'off':
                print("Try again!!!\n")
                close = input("Type OFF: ").lower()


            return 1


run_maze()