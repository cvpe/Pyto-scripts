from  rubicon.objc import *
import pyto_ui as ui
import math
import mainthread


from Foundation import NSBundle
NSBundle.bundleWithPath_('/System/Library/Frameworks/SceneKit.framework').load()


SCNView, SCNScene, SCNBox, SCNNode, SCNMaterial, SCNCamera, SCNLight, SCNAction, SCNLookAtConstraint = map(ObjCClass, ['SCNView', 'SCNScene', 'SCNBox', 'SCNNode', 'SCNMaterial', 'SCNCamera', 'SCNLight', 'SCNAction',  'SCNLookAtConstraint' ])
UIColor = ObjCClass('UIColor')

@mainthread.mainthread
def demo(main_view):

    main_view_objc = main_view.__py_view__.managed
  
    scene_view = SCNView.alloc().initWithFrame_options_(((0, 0),(main_view.width,main_view.height)), None).autorelease()
    scene_view.setAutoresizingMask_(18)
    scene_view.setAllowsCameraControl_(True)
    main_view_objc.addSubview_(scene_view)
    
    scene = SCNScene.scene()
    scene_view.setScene_(scene)
    
    root_node = scene.rootNode
    
    camera = SCNCamera.camera()
    camera_node = SCNNode.node()
    camera_node.setCamera(camera)
    camera_node.setPosition((-30,30,30))
    root_node.addChildNode_(camera_node) 
    
    geometry = SCNBox.boxWithWidth_height_length_chamferRadius_(10, 10, 10, 0)
     
    geometry_node = SCNNode.nodeWithGeometry_(geometry)
    root_node.addChildNode_(geometry_node)
    
    Materials = []
    colors = [UIColor.redColor, UIColor.blueColor, UIColor.greenColor, UIColor.yellowColor, UIColor.orangeColor, UIColor.cyanColor]
    for i in range(0,6):
      Material = SCNMaterial.material()
      Material.contents = colors[i] 
      Materials.append(Material)
    geometry.setMaterials_(Materials)

    # Add a constraint to the camera to keep it pointing to the target geometry
    constraint = SCNLookAtConstraint.lookAtConstraintWithTarget_(geometry_node)
    constraint.gimbalLockEnabled = True
    camera_node.constraints = [constraint]
    
    light_node = SCNNode.node()
    light_node.setPosition_((30, 0, -30))
    light = SCNLight.light()
    #light.setType_('spot')
    light.setType_('probe')
    #light.setType_('directional')
    light.setCastsShadow_(True)
    light.setColor_(UIColor.whiteColor)
    light_node.setLight_(light)
    root_node.addChildNode_(light_node)
    
    rotate_action = SCNAction.repeatActionForever_(SCNAction.rotateByX_y_z_duration_(0, math.pi*2, 0, 10))
    geometry_node.runAction_(rotate_action)
  
    
def main():
  v = ui.View()
  v.frame=(0, 0, 600, 600)
  v.name = 'SceneKit Demo'
  demo(v)
  ui.show_view(v, ui.PRESENTATION_MODE_SHEET)

if __name__ == '__main__':
  main()
