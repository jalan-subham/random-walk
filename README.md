# Structure  

## main island  

The main window should be of dynamic sizing  
But same aspect ratio  
  
We assume the programmer / assets manager to be responsible in chosing an apt island image  
Image will not get out of its aspect ratio, only get rescaled  

### General guidelines about island image selection  
1. It should be High Quality, png preferably  
2. 2 / 3rds of the image should be sky  
3. Padding of the island with the cean / sea should be about 1/6 both sides  
4. The image should be symetrical (not necessary)  
5. It should be present inside assets/image folder as island.png

## A coin toss window  
In Progress

## A bifurcation diagram  



# Peripherals  

## Music start at play, till death  

The music copyright scenario is unclear,  
1. Music starts with an entrance fade-in of 5ms  


## death sound  
End music is from mario.  
1. Again, with 5ms fade-in 

## replay option
1. After the death sund plays, there is an Instruction test with **Half the font size**
2. Restart is again from the same initial setups

# References
1. Using os.path.join in pygame.image.load because of : ["You should use os.path.join() for compatibility."](https://www.pygame.org/docs/ref/image.html#pygame.image.load)  
2. os.path.dirname(\_\_file\_\_) gives the name of the folder of the file  
3. ["Blitting is one of the slowest operations in any game, so you need to be careful not to blit too much onto the screen in every frame."](https://www.pygame.org/docs/tut/tom_games2.html)

# TODO
Employing inheritance
Try Except for file not found
