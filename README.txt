  ---------------------------------------------------------------
  ***************************************************************
  *                      Help Drunk Go Home                     *
  ***************************************************************
  *                                                             *
  *       My GitHub Homepage: https://github.com/slycq66/       *
  *                                                             *
  * GNU GENERAL PUBLIC LICENSE 3+  HTTP://WWW.GNU.ORG/licenses/ *
  *                                                             *
  ***************************************************************
  *                        Version   1.0                        *
  ***************************************************************
  ---------------------------------------------------------------
  
 INSTALLING: 

 Download agents.py, DensityMap.py, GameMap.py, main.py, MainWindow.py, SubWindow.py and    drunk.plan(totally seven). They should be put in the same file.

 To run: Simply run main.py through Spyder or other Integrated Development Environment. 
 
 If you don't have Spyderk, you can download it here:
 https://www.spyder-ide.org/
 
  ---------------------------------------------------------------
 
 USE: 

 It is difficult for a person to control his behavior when he is drunk, which will cause  certain difficulties to the public security of the city. Many city planners want to solve  this problem by, for example, modifying roads near bars so that alcoholics can easily find  their way home. The purpose of this model is to simulate the process of drunks going home,  find the place where drunks are most likely to appear, provide data support for road  reconstruction.


 The algorithm is that for each drunk (who will get an id between 1 and 25), move the  drunk randomly left/right/up/down in a loop that picks randomly the way it will go. When it  hits the correctly numbered house, stop the process and start with the next drunk. At each  step for each drunk, add one to the density for that point on the map. To make it easier for   drunks to get home, the police class was added to help them. The police would constantly  patrol the map and take drunks home when they found them wandering.

 The model can do:

 ·Read the data file drunk.plan;
 ·Draw the pub and homes on the map;
 ·Model the drunks leaving the bar and reaching their homes;
 ·Draw the density of drunks passing through each pixel on the map;
 ·Saves the density map to a file as text;
 ·Displays the model as an animation;
 ·A GUI that users can interact with;
 ·Help them find their way home by police.
 
  ---------------------------------------------------------------
 
 IDEAS FOR FURTHER DEVELOPMENT
 
 ·Optimize the speed of the model. The current version of the model is slow and takes a long    time to simulate 25 drunks;

 ·Make drunks sober up and move faster as they move; After a certain amount of time, the       alcoholic will be fully sober and able to make his own way home; 

 ·Fixed the bug that police could drive drunks home through bar.
 
 ---------------------------------------------------------------

 REFERENCE:

 https://blog.csdn.net/zzzzjh/article/details/82985209

 https://www.cnblogs.com/Army-Knife/p/10689599.html
