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
def draw_maze(grid, cell_size, filename):
    """
    Draws the maze to a PDF file.
    """
    # initialize the PDF canvas
    pdf_canvas = canvas.Canvas(filename)
    pdf_canvas.setPageSize((len(grid[0]) * cell_size, len(grid) * cell_size))

    # loop over the grid and draw the walls
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            # draw the walls
            if cell & 1:
                pdf_canvas.line(x * cell_size, y * cell_size, x * cell_size, (y + 1) * cell_size)
            if cell & 2:
                pdf_canvas.line(x * cell_size, y * cell_size, (x + 1) * cell_size, y * cell_size)
            if cell & 4:
                pdf_canvas.line(x * cell_size, (y + 1) * cell_size, (x + 1) * cell_size, (y + 1) * cell_size)
            if cell & 8:
                pdf_canvas.line((x + 1) * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size)

    # draw the start and end positions
    pdf_canvas.setFont("Helvetica", cell_size * 0.4)
    pdf_canvas.drawCentredString(cell_size / 2, cell_size / 2, "Start")
    pdf_canvas.drawCentredString(len(grid[0]) * cell_size - cell_size / 2, len(grid) * cell_size - cell_size / 2, "End")

    # save the PDF file
    pdf_canvas.save()
    

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
                if len(next_visited) < len(route):
                    next_path = path + route[len(next_visited)-1]
                else:
                    next_path = path + "X"
                stack.append(((nx, ny), next_path, next_visited))
    return []

# define the main function
def main():
    # get the user input for the route
    route = input("Enter the route (letters or numbers): ")    
    # create the maze
    grid = create_maze(maze_width, maze_height)
    # draw the maze
    draw_maze(grid, cell_size, 'maze.pdf')
    # find the solution route
    solution = find_solution(grid, start, end, route)
    print(grid)
    print(solution)
    # highlight the solution route in green
    pdf_canvas.setStrokeColorRGB(0, 1, 0)
    pdf_canvas.setLineWidth(3)
    for i in range(len(solution)-1):
        x1, y1 = solution[i]
        x2, y2 = solution[i+1]
        pdf_canvas.line(x1 * cell_size + cell_size / 2, y1 * cell_size + cell_size / 2, x2 * cell_size + cell_size / 2, y2 * cell_size + cell_size / 2)
    # save the PDF file
    #pdf_canvas.save()


# call the main function
if __name__ == "__main__":
    main()
