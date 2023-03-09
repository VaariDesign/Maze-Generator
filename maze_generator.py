import random
import string
from reportlab.pdfgen import canvas

# set up the maze parameters
maze_width = 100
maze_height = 100
wall_width = 5
cell_size = 20
start = (0, 0)
end = (maze_width - 1, maze_height - 1)

# define the directions for moving in the maze
directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

# create a new canvas for the maze
pdf_canvas = canvas.Canvas("maze.pdf")

# define the function to create the maze
def create_maze(width, height):
    # create the grid
    grid = [[0 for i in range(width)] for j in range(height)]
    # set the starting cell to visited
    visited = set([(0, 0)])
    # create a stack to keep track of visited cells
    stack = [(0, 0)]
    # loop until all cells have been visited
    while stack:
        # get the current cell
        current = stack.pop()
        x, y = current
        # get the neighbors of the current cell
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                neighbors.append((nx, ny))
        # if there are unvisited neighbors, choose one at random
        if neighbors:
            next_cell = random.choice(neighbors)
            nx, ny = next_cell
            # remove the wall between the current cell and the next cell
            if nx > x:
                grid[x][y] |= 1
            elif nx < x:
                grid[nx][ny] |= 1
            elif ny > y:
                grid[x][y] |= 2
            elif ny < y:
                grid[nx][ny] |= 2
            # mark the next cell as visited and add it to the stack
            visited.add(next_cell)
            stack.append(current)
            stack.append(next_cell)
    return grid

# define the function to draw the maze
def draw_maze(grid):
    # calculate the size of the canvas
    canvas_width = maze_width * cell_size + wall_width
    canvas_height = maze_height * cell_size + wall_width
    # set the canvas background color to white
    pdf_canvas.setFillColorRGB(1, 1, 1)
    pdf_canvas.rect(0, 0, canvas_width, canvas_height, stroke=0, fill=1)
    # draw the walls
    pdf_canvas.setFillColorRGB(0, 0, 0)
    for x in range(maze_width):
        for y in range(maze_height):
            if not grid[x][y] & 1:
                pdf_canvas.rect(x * cell_size, y * cell_size, cell_size, wall_width, stroke=0, fill=1)
            if not grid[x][y] & 2:
                pdf_canvas.rect(x * cell_size, y * cell_size, wall_width, cell_size, stroke=0, fill=1)

# define the function to find the solution route
def find_solution(grid, start, end, route):
    stack = [(start, "", {start})]
    rows, cols = len(grid), len(grid[0])
    while stack:
        current, path, visited = stack.pop()
        if current == end:
            return [(x, y) for (x, y) in visited]
        x, y = current
        neighbors = [
            (nx, ny)
            for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0
        ]
        for nx, ny in neighbors:
            if (nx, ny) not in visited:
                next_visited = visited.copy()
                next_visited.add((nx, ny))
                if len(route) < rows + cols - 2:
                    route = "X" * (rows + cols - 2 - len(route)) + route
                next_path = path + route[len(next_visited)-1]
                stack.append(((nx, ny), next_path, next_visited))
    return []

# define the main function
def main():
    # get the user input for the route
    route = input("Enter the route (letters or numbers): ")    
    # create the maze
    grid = create_maze(maze_width, maze_height)
    # draw the maze
    draw_maze(grid)
    # find the solution route
    solution = find_solution(grid, start, end, route)
    # highlight the solution route in green
    pdf_canvas.setStrokeColorRGB(0, 1, 0)
    pdf_canvas.setLineWidth(3)
    for i in range(len(solution)-1):
        x1, y1 = solution[i]
        x2, y2 = solution[i+1]
        pdf_canvas.line(x1 * cell_size + cell_size / 2, y1 * cell_size + cell_size / 2, x2 * cell_size + cell_size / 2, y2 * cell_size + cell_size / 2)
    # save the PDF file
    pdf_canvas.save()

# call the main function
if __name__ == "__main__":
    main()
