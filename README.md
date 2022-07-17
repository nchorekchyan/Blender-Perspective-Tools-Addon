# Blender-Perspective-Tools-Addon
This is a beta version of a add-on for blender that allows you to create a simple one point and two point perspective grid, with goals of adding three point, fisheye, and potentially 5/6 point perspective as well.
It also comes with assists for the two point perspective mode which should help in drawing dynamically in 3d space.

As this is still in test mode, I recommend not using this on a file you have in progress. Start a new file with it.

The real goal is to add similar functionality to Krita's perspective assists to blender.

Instructions:
For One Point Perspective:
1. Click Create 1PP VP to create your base object. A single point will be created in grease pencil, move it wherever you want.
2. Clicking Create 1PP VP multiple times will purge vanishing points or lines associated with it (it deletes/recreates)
3. Click Create 1PP Map to create a set of lines pointing to the vanishing point.
4. In the One Point Perspective objects Edit Mode, you can move the vanishing point and click Create 1PP Map to create additional lines pointing to the vanishing point.

For Two Point Perspective:
1. Click Create 2PP VPs to create your base object. A line with two points will be created. The points are your vanishing points.
2. Clicking Create 2PP VPs multiple times will purge vanishing points or lines associated with it (it deletes/recreates)
3. Click Create 2PP Grid to create a two point perspective grid.
4. In the Two Point Perspective objects Edit Mode, you can move the vanishing point and click Create 1PP Map to create additional lines pointing to the vanishing point.
  NOTE: Currently, it must be along the same X axis (so while moving the points, tap 'X' on your keyboard to lock it. 
    Math is missing for dutch angles. For now, just rotate the grease pencil object if you need a dutch angle grid.

For Assists:
  1. Make sure you have a Two Point Perspective object (click Create 2PP VPs).
  2. Select the Grease Pencil Object you will be using to draw from the collection/object dropdowns.
  3. Click Lock Other Objects. 
    This sets other object to be unselectable. Due to the nature of the addon, if you don't do this and you click the camera while using assists, it will hijack the rotation and mess with your view.
  4. Select the grease pencil object from the OUTLINER (in addition to selecting it from the dropdown menu in the panel. Enter draw mode on the grease pencil object you will be drawing on.
  5. Click 2PP Assists. You will now have assists. Still working out bugs with this.
  6. Click ESC on your keyboard to get rid of the assists.
  7. Click Release Locks to make other objects selectable.
    
    

Known Issues:
  May crash when undoing, particularly using Assists (though this may be resolved)
  Assists stop following your mouse cursor on mousedown.
  
 Future Goals: 
  Additional Perspective Modes
  Add dutch angle support for two point perspective
  Rulers
  Snapping
  Switching to use OpenGL instead of Grease Pencil for grids/assists
  Add additional error handling 
  Figure out an alternative for locking objects.
