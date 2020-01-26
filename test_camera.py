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
imageFrame = tk.Frame(window, width=600, height=700)
imageFrame.grid(row=1, column=1, padx=0, pady=0)

#Windows for each emotion (sorrow, anger, surprise, joy)
sorrowText = tk.StringVar()
angerText = tk.StringVar()
surpriseText = tk.StringVar()
joyText = tk.StringVar()

sorrowText.set("Sorrow text")
angerText.set("Anger text")
surpriseText.set("Surprise text")
joyText.set("Joy text")

sorrowDisplay=tk.Message(window, width = 200, font = 30, textvariable = sorrowText, bg = "white")
angerDisplay=tk.Message(window, width = 200, font = 30, textvariable = angerText, bg = "white")
surpriseDisplay=tk.Message(window, width = 200, font = 30, textvariable = surpriseText, bg = "white")
joyDisplay=tk.Message(window, width = 200, font = 30, textvariable = joyText, bg = "white")
sorrowDisplay.grid(row=1, column=0, padx=0, pady=0)
angerDisplay.grid(row=1, column=2, padx=0, pady=0, sticky="W")
surpriseDisplay.grid(row=2, column=0, padx=0, pady=0)
joyDisplay.grid(row=2, column=2, padx=0, pady=0.1, sticky="W")

'''
liveEmotionText = tk.StringVar()
liveEmotionText.set("emotion text")
#emotion text window
emotionText = tk.Message(window, width = 500, font = 30, textvariable = liveEmotionText)
emotionText.grid(row=1, column=25, padx=10, pady=2)
'''

liveEmotionText = tk.Text(window, width = 70, height = 15, font = 10)
#Origonal row=1, column=70
liveEmotionText.grid(row = 3, column = 0, padx = 0, pady = 0)

#liveEmotionText.insert("1.0", "Live Emotion goes here")



#text (Original width=69, height=65)
transcriptText = tk.Text(window, width = 69, height = 65, font = 20)
transcriptText.grid(row = 3, column = 2, padx = 0, pady = 0)

transcriptText.insert("1.0", "")




window.geometry("+-10+0")
window.geometry("2500x1000")


#Capture video frames
lmain = tk.Label(imageFrame, height = 600, width = 700)
lmain.grid(row=1, column=1)
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
        global sorrowDisplay
        global angerDisplay
        global joyDisplay
        global surpriseDisplay

        if(likelihood_name[face.sorrow_likelihood]!= "VERY_UNLIKELY"):
            sorrowDisplay.configure(background = "blue")
        else:
            sorrowDisplay.configure(background="white")
        if(likelihood_name[face.anger_likelihood]!= "VERY_UNLIKELY"):
            angerDisplay.configure(background = "red")
        else:
            angerDisplay.configure(background="white")
        if(likelihood_name[face.surprise_likelihood]!= "VERY_UNLIKELY"):
            surpriseDisplay.configure(background = "purple")
        else:
            surpriseDisplay.configure(background="white")
        if(likelihood_name[face.joy_likelihood]!= "VERY_UNLIKELY"):
            joyDisplay.configure(background = "yellow")
        else:
            joyDisplay.configure(background="white")

            
        
        
        newStr= 'anger: {}'.format(likelihood_name[face.anger_likelihood])
        angerText.set(newStr)
        newStr= 'joy: {}'.format(likelihood_name[face.joy_likelihood])
        joyText.set(newStr)
        newStr= 'surprise: {}'.format(likelihood_name[face.surprise_likelihood])
        surpriseText.set(newStr)
        newStr= 'sorrow: {}'.format(likelihood_name[face.sorrow_likelihood])
        sorrowText.set(newStr)

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






show_frame()  #Display 2
window.mainloop()  #Starts GUI