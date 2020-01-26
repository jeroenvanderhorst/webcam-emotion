import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import os


import continuous

from google.cloud import vision
from google.cloud.vision import types

from google.cloud import vision
import io
client = vision.ImageAnnotatorClient()

#type this in terminal: $env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\Jerry\Downloads\Emotion Detection-9d7952e9b095.json"

counter = 0
totalTranscriptText = ""

try:
    os.remove("tempTextFile.txt")
except:
    pass
#Set up GUI
window = tk.Tk()  #Makes main window
window.wm_title("Digital Microscope")

window.config(background="#FFFFFF")

#Graphics window
imageFrame = tk.Frame(window, width=600, height=500)
imageFrame.grid(row=1, column=1, padx=0, pady=0)

faceText = tk.StringVar()
faceText.set("facial text")
#facial text window
facialText = tk.Message(window, width = 500, font = 30, textvariable = faceText, bg = "white")
facialText.grid(row=7, column=1, padx=0, pady=0)

'''
liveEmotionText = tk.StringVar()
liveEmotionText.set("emotion text")
#emotion text window
emotionText = tk.Message(window, width = 500, font = 30, textvariable = liveEmotionText)
emotionText.grid(row=1, column=25, padx=10, pady=2)
'''

liveEmotionText = tk.Text(window, width = 70, height = 15, font = 10)
liveEmotionText.grid(row = 1, column = 70, padx = 0, pady = 0)

#liveEmotionText.insert("1.0", "Live Emotion goes here")



#text 
transcriptText = tk.Text(window, width = 65, height = 69, font = 20)
transcriptText.grid(row = 10, column = 70, padx = 0, pady = 0)

transcriptText.insert("1.0", "")




window.geometry("+-10+0")
window.geometry("2500x1000")


#Capture video frames
lmain = tk.Label(imageFrame)
lmain.grid(row=0, column=0)
cap = cv2.VideoCapture(0)

def detect_faces(path):
    """Detects faces in an image."""
    
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

                       #-1, 0, 0.25,.5, .75, 1.0
    

    for face in faces:
        global facialText

        if(likelihood_name[face.sorrow_likelihood]!= "VERY_UNLIKELY"):
            facialText.configure(background = "blue")
        elif(likelihood_name[face.anger_likelihood]!= "VERY_UNLIKELY"):
            facialText.configure(background = "red")
        elif(likelihood_name[face.surprise_likelihood]!= "VERY_UNLIKELY"):
            facialText.configure(background = "purple")
        elif(likelihood_name[face.joy_likelihood]!= "VERY_UNLIKELY"):
            facialText.configure(background = "yellow")
        else:
            facialText.configure(background = "white")

            
        
        newStr = ""
        newStr+= 'anger: {}'.format(likelihood_name[face.anger_likelihood])
        newStr+= '\n'
        newStr+= 'joy: {}'.format(likelihood_name[face.joy_likelihood])
        newStr+= '\n'
        newStr+= 'surprise: {}'.format(likelihood_name[face.surprise_likelihood])
        newStr+= '\n'
        newStr+= 'sorrow: {}'.format(likelihood_name[face.sorrow_likelihood])
        newStr+= '\n'
        faceText.set(newStr)

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

    

def show_frame():
    try: 
        global counter
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)

        

        counter+=1

        if(counter >= 30):

            cv2.imwrite(filename='saved_img.jpg', img=frame)
            img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)
            img_resized = cv2.imwrite(filename='saved_img-final.jpg', img=img_)
            file_name = os.path.abspath('saved_img-final.jpg')

            detect_faces(file_name)
            counter = 0

            os.remove("saved_img-final.jpg")
            try:
                with open("tempTextFile.txt", "r") as fh:
                    fileData = fh.readlines()
                    print(fileData)
                    for line in fileData:
                        nextLine = line.strip()
                        #print(nextLine + "**********************")
                        transcriptText.insert(1.0, nextLine + "\n\n")

                os.remove("tempTextFile.txt")
                
                liveEmotionText.delete(1.0, tk.END)
                with open("continuous.txt", "r") as fileHandle:
                    newFileData = fileHandle.readlines()
                    print(newFileData)
                    #randVar = 0
                    for newLine in newFileData:
                        nextLine = newLine.strip()#.lstrip().rstrip()
                        liveEmotionText.insert(1.0, nextLine + "\n")
                        '''
                        if(randVar == 2):
                            nextLinePlaceholder = nextLine.split(" ")[-1]
                            print(nextLinePlaceholder)
                            if(float(nextLinePlaceholder) > 0):
                                backColor = "green"
                            elif(float(nextLinePlaceholder) < 0):
                                backColor = "red"
                            else:
                                backColor = "white"
                        randVar += 1
                        liveEmotionText.configure(background = backColor)
                        '''
                        
                        
            except:
                pass
        
                


        lmain.after(10, show_frame)
        
        

    except(KeyboardInterrupt):
        print("Turning off camera.")
        cap.release()
        print("Camera off.")
        print("Program ended.")
        cv2.destroyAllWindows()
    except:
        print("I don't know what's happening anymore...")



#Slider window (slider controls stage position)
sliderFrame = tk.Frame(window, width=1000, height=900)
sliderFrame.grid(row = 100, column=100)#, padx=10, pady=2)


show_frame()  #Display 2
window.mainloop()  #Starts GUI