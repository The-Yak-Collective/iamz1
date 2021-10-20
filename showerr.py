#expect output file name in command line. read from stdin a line with 18 numbers - each is an error amount in range 0..255
#Import the library
from PIL import Image, ImageDraw
import sys
outputname='test.jpg'
if len(sys.argv)>1:
    outputname=sys.argv[1]
line=input()
#print(line)
errors=line.split()
errors=[0]+[int(x) for x in errors]
gerror=int(sum(errors)/18) #normalize to 0..255
#Creating new Image object for background. The color 'scheme' is 'RGB' and the size 500x500pixels
img = Image.new("RGB", (100,100)) 

#Creating object from img to draw on.
draw = ImageDraw.Draw(img) 

globalerror=(gerror,255-gerror,0)

draw.ellipse((10, 10, 90, 90), fill=(50,50,50), outline=globalerror)     
indiverror=[(0,0,0)]*19
for i in range(1,19):
    indiverror[i]=(errors[i],255-errors[i],0)

for side in range(2):
    for leg in range(3):
        for joint in range(3):
            servoid=side*9+leg*3+joint+1
            rectx=55+(10*joint) if side==0 else 45-10*joint
            recty=30+20*leg
            draw.rectangle([rectx-4,recty-4,rectx+4,recty+4], fill=indiverror[servoid])
draw.rectangle([48,30,52,75],fill=(255,255,255))
draw.ellipse([45,75,55,85],fill='white')
img=img.rotate(180)
    #Showing the image
img.save(outputname)
