# Curvature Cache
 Simple tool for quickly baking curvature information into an object's vertex colors. Useful for edge masking etc


 ## What & How 
 The addon works by using the "Dirty Vertex" function inside of Blender to capture mesh curvature information into its vertex colors. But not only that, the addon provides an easy one-click button that will copy your current base mesh, apply all of the copy's modifiers and then set up a vertex color data transfer.

 The benefit here is that you don't need to finalize your mesh to get the vertex colors. These vertex colors can then be used to make interesting materials with edge weathering etc.

 The ideal use case is for hard surface modeling where you often have active bevel modifiers and don't want to destructively apply them. It's also usable for any other mesh, BUT it will be significantly slower if your mesh is extremely dense, so it might not be ideal for high detail character sculpts etc.

 The button can be found in the 3D view under "Curvature Generator".





