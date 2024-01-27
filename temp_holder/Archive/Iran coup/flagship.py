import pygame


"""
Objectives:
Possible Systems:
1. Create communication channel:
a. get info out
-- Create public outroar-> public squeezes industries-> industries squeeze iran
b. get info in
-- action plans

How do coups turn successful? [Think Moriarity][Win-win?]
1. assess ground situation [actively collect data]
2. coup history -> coup factors[Identify coup dynamics][active modelling: cause and effect]
-- What is the environment-> what do i want-> what is my plan to exploit environment to what get i want?
-- how to implement?
3. coup strategy [Contingency plans]
-- what are the points of weakness?
-- use data and algorithms to ensure optimal coup strategy [Feedback loops]
-- determine coup trajectory -> Predict future structure [Direct future structure]
"""

import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = (720, 480)
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

run_state = True
while run_state:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_state = False

    pygame.display.flip()
    display.fill("black")

pygame.quit()



"""
git integration
data visualization
rdbms, dbms
server
api  

system architecture
technologies -> capabilities, essence
"""















