#seed -> the number which the random map will be based on (enables for map saves)
#vec_size -> the vectors' max x and y value
#grid_size -> how many grids on one side of the square will there be(lower number means less randomess)
#pixel_per_grid -> number of pixels in a grid (detail, of each square, also the size of each square)
#startx -> starting corner's x value (enables moving accross the map)
#starty  -> starting corner's y value (enables moving accross the map)
import random

def gen_perlin(seed=0,vec_size=1,grid_size=8,pixels_per_grid=20,startx=0,starty=0):#will generate a make of perlin noise values from 0-1
    
    def coord_ran_seed(seed,x,y):#this function allows to get a unique seed based on the universal seed and 2d coordinates
        random.seed(seed)
        next_seed = random.randint(-1000,1000)
        random.seed(next_seed+x)
        next_seed = random.randint(-1000,1000)
        return (next_seed+y)
    
    #sets the arrays needed
    height_map = []#will hold all the heights 0-1
    vectors =[]#will hold the random vectors

    #makes the important variables based on parameters entered 
    per_grid = pixels_per_grid#gets the number of pixels in a grid
    map_num = grid_size*pixels_per_grid#gets the amount of pixels in the grid
    vector_num = grid_size+1#gives the number of vectors in the grid

    #produces random vectors, seed based
    for x in range(vector_num):
        temp = []#temporary array that allows me to make a 2d array
        
        for y in range(vector_num):
            random.seed(coord_ran_seed(seed,x+startx,y+starty))#gets the seed of the coordinate 
            x1 = random.uniform(-vec_size,vec_size)#chooses the vector's x value at random
            y1 = random.uniform(-vec_size,vec_size)#chooses the vector's y value at random
            temp.append([x1,y1])#adds the vector's value to the temporary array
            
        vectors.append(temp)#slowly adds to the main vector array


    #gets the heihgt for each vector in the map
    for x in range(map_num):
        temp = []#temporary array that allows me to make a 2d array
        
        for y in range(map_num):

            #finds the closest main grid point to the pixel
            backx = int(x/per_grid)
            backy = int(y/per_grid)

            #finds the 4 distace vectors from the closest point
            vectors_to = [[(x-backx*per_grid),(y-backy*per_grid)],
                          [(x-backx*per_grid)-(per_grid),(y-backy*per_grid)],
                          [(x-backx*per_grid),(y-backy*per_grid)-(per_grid)],
                          [(x-backx*per_grid)-(per_grid),(y-backy*per_grid)-(per_grid)]]

            #makes an array points with the dot products, which give the gradient of the 4 points
            #(vector to it and the vector on the point are used for the dot produt)
            points = []
            points.append(vectors[backx][backy][0]*vectors_to[0][0]+vectors[backx][backy][1]*vectors_to[0][1])
            points.append(vectors[backx+1][backy][0]*vectors_to[1][0]+vectors[backx+1][backy][1]*vectors_to[1][1])
            points.append(vectors[backx][backy+1][0]*vectors_to[2][0]+vectors[backx][backy+1][1]*vectors_to[2][1])
            points.append(vectors[backx+1][backy+1][0]*vectors_to[3][0]+vectors[backx+1][backy+1][1]*vectors_to[3][1])

            #interpolating bettwen the points with the fade function
            w = ((x-backx*per_grid)/(per_grid-1))
            AB = points[0]+((w*(w*6-15)+10)*w*w*w)*(points[1]-points[0])
            CD = points[2]+((w*(w*6-15)+10)*w*w*w)*(points[3]-points[2])
            w = ((y-backy*per_grid)/(per_grid-1))
            grad = AB +((w*(w*6-15)+10)*w*w*w)*(CD-AB)

            #turning the height into a value bettwen 0-1 for simplicity 
            final = (grad+(per_grid*vec_size))/(2*(per_grid*vec_size))
            
            temp.append(final)#adds the value to the temporary array
            
        height_map.append(temp)#slowly creates the output 2d array of the program
        
    return height_map#gives the height map
