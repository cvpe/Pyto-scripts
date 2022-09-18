# see also http://battleofbrothers.com/sirryan/understanding-shaders-in-spritekit/
import pyto_ui as ui
from rubicon.objc import *
from Foundation import NSBundle
from mainthread import mainthread
from PIL import Image
import io

NSBundle.bundleWithPath_('/System/Library/Frameworks/SpriteKit.framework').load()

UIApplication = ObjCClass('UIApplication')
SKView = ObjCClass('SKView')
SKScene = ObjCClass('SKScene')
SKSpriteNode = ObjCClass('SKSpriteNode')
SKShader = ObjCClass('SKShader')
SKTexture = ObjCClass('SKTexture')
UIColor = ObjCClass('UIColor')
SKUniform = ObjCClass('SKUniform')

def pil2ui(pilimage):
  with io.BytesIO() as bIO:
    pilimage.save(bIO, 'PNG')
    uiimage = ObjCClass('UIImage').alloc().initWithData_(bIO.getvalue())
  return uiimage


def get_screen_size():				
  app = UIApplication.sharedApplication.keyWindow
  for window in UIApplication.sharedApplication.windows:
    ws = window.bounds.size.width
    hs = window.bounds.size.height
    break
  return ws,hs

class DemoView(ui.View):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    #self.pil = Image.open('water_texture.jpg')
    self.pil = Image.open('IMG_8955.jpg')
    self.uiimage = pil2ui(self.pil)

    
  @mainthread
  def did_appear(self):
    # SKView can only be created on a presented view
    # Setup SKView
    screen_size = get_screen_size()
    sz = CGSize(screen_size[0], screen_size[1]-100)
    rect = CGRect(CGPoint(0, 0), sz)
    skview = SKView.alloc().initWithFrame_(rect)
    self.__py_view__.managed.addSubview(skview)
    self.skview = skview
    
    scene = SKScene.sceneWithSize_(rect.size)
    scene.backgroundColor = UIColor.yellowColor
    
    #node = SKSpriteNode.alloc().init()
    # initWithImageNamed_ does not find file, that is why I load file in FloatingPointError
    # file seems to be in a specific Pyto folder, but where?
    #node = SKSpriteNode.alloc().initWithImageNamed_('IMG_8955.jpg')
    texture = SKTexture.textureWithImage_(self.uiimage)
    node = SKSpriteNode.alloc().initWithTexture_(texture)
    wi,hi = self.pil.size
    w = 300
    h = w * hi/wi
    node.size = CGSize(w, h)
    node.position = CGPoint(screen_size[0]/2, screen_size[1]/2)
    
    spritew = SKUniform.uniformWithName_float_('spritew',w)
    spriteh = SKUniform.uniformWithName_float_('spriteh',h)

    shader_text1 = '''
    // only to use position.y
    void main() { 
    vec2 position = gl_FragCoord.xy; 
    vec4 color = texture2D(u_texture, v_tex_coord);
    //color.r = 0; // ignore red
    color.g = position.y/spriteh; // green variable in function of y
    gl_FragColor = color;
    }
    '''
    shader_text2 = '''
    // invert colors
    void main() {
    // find the current pixel color
    vec4 current_color = texture2D(u_texture, v_tex_coord);
    // subtract its current RGB values from 1 and use its current alpha; 
    // multiply by the node alpha so we can fade in or out
    gl_FragColor = vec4(1.0 - current_color.rgb, current_color.a) * current_color.a * v_color_mix.a;
    }
    '''
    shader_text3 = '''
    // ripple effect https://github.com/matthewreagan/SpriteKitShaders/blob/master/SpriteKitShaders/Shaders/simpleLiquidShader.fsh
    void main() {
    // Set up some animation parameters for the waveform
    float speed = u_time * 0.35;
    float frequency = 14.0;
    float intensity = 0.006;
    // Get the coordinate for the target pixel
    vec2 coord = v_tex_coord;
    // Modify (offset slightly) using a sine wave
    coord.x += cos((coord.x + speed) * frequency) * intensity;
    coord.y += sin((coord.y + speed) * frequency) * intensity;
    // Rather than the original pixel color, using the offset target pixel
    vec4 targetPixelColor = texture2D(u_texture, coord);
    // Finish up by setting the actual color on gl_FragColor
    gl_FragColor = targetPixelColor;
    }
    '''
    
    shader_text4 = '''    
    // erase by circles
    void main() {
    vec4 color = texture2D(u_texture,v_tex_coord);
    // center of image is at v_tex_coord = 0.5,0.5
    float r = sqrt(pow(v_tex_coord.x-0.5,2.)+pow(v_tex_coord.y-0.5,2.));
    if (r > cos(u_time/2.)) color.rgb = vec3(1.,1.,0.);
    gl_FragColor = vec4(color.rgb, 1);
    }
    '''
    
    shader_text5 = '''
    // pixelisation      
    void main() {
    float px = 20.;
    float dx = px*cos(u_time/4.)*(1./spritew);
    float dy = px*cos(u_time/4.)*(1./spriteh);
    vec2 coord = vec2(dx*floor(v_tex_coord.x/dx), dy*floor(v_tex_coord.y/dy));
    gl_FragColor = texture2D(u_texture,coord);
    }
    '''
    
    shader = SKShader.shaderWithSource(shader_text3)
    shader.uniforms = [spritew,spriteh]
    
    node.setShader_(shader)
    scene.addChild_(node)
        
    skview.presentScene_(scene)
    self.scene = scene

  def did_disappear(self):
    self.skview.paused = True


if __name__ == '__main__':
  view = DemoView()
  view.title = 'GLSL shader'
  ui.show_view(view,ui.PRESENTATION_MODE_FULLSCREEN)