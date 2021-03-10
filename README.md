# Face-Recognition-Based-Attendance-System
### A web app to recognize faces of all students in photo and mark their attendance in Database using Deep Learning.  

## Project Flow
![Test Image 4](https://github.com/sakshamj74/Face-Recognition-Based-Attendance-System/blob/main/diagrams/block_diagram.png)

## MTCNN Architecture
![Test Image 5](https://github.com/sakshamj74/Face-Recognition-Based-Attendance-System/blob/main/diagrams/mtcnn_1.png)

## Facenet Architecture Intuition
![Test Image 6](https://github.com/sakshamj74/Face-Recognition-Based-Attendance-System/blob/main/diagrams/google-facenet-algorithm.png)


## Other files:
<b>app.py</b> : Backend code using Flask.   
<b>Face_recog_facenet</b> : Model Building Code.   
<b>face_net.h5 </b>: Saved wights of Facenet model.  
<b>pred_3_svm_face_model.pkl</b> : Saved Svm Model.  
<b>requirements.txs </b>: File with all required libraries.  
<b>template </b>: HTML/CSS codes.  
<b>Test</b> : This will store images to test our app.  

## How to run
### Step 1:
#### open Terminal and Install the required libraries by pip install -r requirements.txt 
### Step 2:
#### Use "export FLASK_APP=app.py"
### Step 3:
#### Use this "flask run" to run server.
 
## Future Work
#### Reducing response time, At present it is around 40-50 secs per image on CPU.  
#### Making Backend better with personalised logins for every student and faculty.  
#### Improving model accuracy by using better image processing techniques.
#### Testing model with more number of students in one frame.
