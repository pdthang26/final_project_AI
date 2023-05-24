import cv2
import tkinter as tk
import keras
from keras.models import load_model
from PIL import Image, ImageTk
from keras.utils.image_utils import img_to_array
from tkinter import messagebox as msg
import numpy as np
import os

class FaceDetectionGUI(tk.Tk):
    def __init__(self):
        # Khởi tạo GUI
        super().__init__()
        #variable
        self.gender_pred=None
        self.age_pred=None
        #cấu hình GUI
        self.protocol( 'WM_DELETE_WINDOW', self.btn_thoat_click)
        self.model_gender = load_model("D:\Semester 6\Artificial Intelligence\GUI\gender.h5")
        self.model_age = load_model("D:\Semester 6\Artificial Intelligence\GUI\Age.h5")
        self.geometry('1300x700') 
        self.config(bg='#42f5cb')
        self.title('Ứng dụng lựa chọn quần áo tự động')

        self.lbl_welcome = tk.Label(self, text="Chào mừng bạn đến với cửa hàng hãy đứng trước camera nhấn tiếp tục và tìm ra món đồ ưng ý", 
                                     fg= 'Green',
                                     font = ('Arial',17),bg='#42f5cb', relief =tk.FLAT )
        self.lbl_welcome.pack(side= tk.TOP, pady=10) 

        # Tạo nút "Detection" để lưu ảnh chỉ có khuôn mặt
        self.button = tk.Button(self, width= 20,text='Chọn đồ',font = ('Arial',17), command=self.choose)
        self.button.place(x=200, y=540) 
        
        self.button_next = tk.Button(self, width= 20,text='Lựa chọn khác',font = ('Arial',17), command=self.next)
        self.button_next.place(x=700, y=540) 

        self.button_finish = tk.Button(self, width= 20,text='Hoàn thành ',font = ('Arial',17), command=self.finish)
        self.button_finish.place(x=1000, y=540) 

        self.button_next.config(state="disabled")
        self.button_finish.config(state="disabled")
        # Tạo label để hiển thị hình ảnh từ camera trên GUI
        self.label = tk.Label(self)
        self.label.place(x=10, y=50) # Đặt label ở phía trên cùng của GUI và thêm khoảng cách dọc giữa label và các thành phần dưới

        self.lbl_gender = tk.Label(self, text="Giới tính: ", font = ('Arial',17), bg='#42f5cb',relief =tk.FLAT )
        self.lbl_gender.place(x=100, y= 600)


        self.lbl_age = tk.Label(self, text="Tuổi: ", font = ('Arial',17), bg='#42f5cb', relief =tk.FLAT )
        self.lbl_age.place(x=100, y= 630)

        self.lbl_clothes = tk.Label(self, bg='#42f5cb')
        self.lbl_clothes.place(x=800, y= 50)

        # Khởi tạo đối tượng capture để lấy hình ảnh từ camera
        self.cap = cv2.VideoCapture(0)
        
        self.update()
        

    def update(self):
            image_gender = None
            # Lặp lại việc cập nhật hình ảnh sau 10ms
            ret, frame = self.cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    face_img = frame[y:y+h, x:x+w]
                    face_img1 = frame[y:y+h, x:x+w]
                    # Resize khuôn mặt với độ phân giải 30x30
                    image_gender = cv2.resize(face_img, (30, 30), interpolation = cv2.INTER_AREA)
                    image_age = cv2.resize(face_img1, (100, 100), interpolation = cv2.INTER_AREA)
                # Chuyển đổi hình ảnh từ định dạng OpenCV sang định dạng Pillow
                img1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img1 = Image.fromarray(img1)
                imgtk = ImageTk.PhotoImage(image=img1)
                self.label.image = imgtk
                self.label.config(image=imgtk)
                if image_gender is not None:
                    self.predict(image_gender, image_age)
                    self.predict_run = self.after(10, self.predict)
            self.update_run = self.after(10, self.update)

    def choose(self):
        self.i=1
        self.after_cancel(self.predict_run)
        self.after_cancel(self.update_run)
        if self.gender_pred == 'Nam':
            folder= "D:/Semester 6/Artificial Intelligence/GUI/clothes/man/" 
            self.file = folder  + str(self.age_pred) +" (1).jpg"
        elif self.gender_pred == 'Nữ':
            folder= "D:/Semester 6/Artificial Intelligence/GUI/clothes/women/" 
            self.file = folder + str(self.age_pred) +" (1).jpg"
        img = Image.open(self.file)
        img = img.resize((340, 470), Image.ANTIALIAS)
        imgtk = ImageTk.PhotoImage(image=img)
        self.lbl_clothes.image = imgtk
        self.lbl_clothes.config(image=imgtk)
        self.button_next.config(state="normal")
        self.button_finish.config(state="normal")
        self.button.config(state="disabled")
    
    def next(self):
        if os.path.exists(self.file):
            self.i=self.i+1
        else : self.i=1
        if self.gender_pred == 'Nam':
            folder= "D:/Semester 6/Artificial Intelligence/GUI/clothes/man/" 
            self.file = folder  + str(self.age_pred) +" ("+ str(self.i) + ").jpg"
        elif self.gender_pred == 'Nữ':
            folder= "D:/Semester 6/Artificial Intelligence/GUI/clothes/women/" 
            self.file = folder + str(self.age_pred) +" ("+ str(self.i) + ").jpg"
        img = Image.open(self.file)
        img = img.resize((340, 470), Image.ANTIALIAS)
        imgtk = ImageTk.PhotoImage(image=img)
        self.lbl_clothes.image = imgtk
        self.lbl_clothes.config(image=imgtk)
    def finish (self):
        self.button.config(state="normal")
        self.button_next.config(state="disabled")
        self.button_finish.config(state="disabled")
        self.update_run = self.after(10, self.update)
    def predict(self, image_gender, image_age):
        gender = {0: 'Nam',1:'Nữ'}
        age = {0: '15->17',1:'18->20', 2:"21->23", 3:'24->25'}
        img = image_gender
        img = img_to_array(img)
        img= img.reshape(1,30,30,3)
        img = img.astype('float32')
        img =img/255
        result  = np.argmax(self.model_gender.predict(img),axis=1)
        self.gender_pred = gender[result[0]]
        self.lbl_gender.config(text= "Giới tính: " + gender[result[0]])


        img2 = image_age
        img2 = img_to_array(img2)
        img2= img2.reshape(1,100,100,3)
        img2 = img2.astype('float32')
        img2 =img2/255
        result  = np.argmax(self.model_age.predict(img2),axis=1)
        self.age_pred = result[0]
        self.lbl_age.config(text= "Tuổi: " + age[result[0]])
       

    def btn_thoat_click (self):
        self.after_cancel(self.predict_run)
        self.after_cancel(self.update_run)
        tra_loi = msg.askquestion('Warning','ban co muon thoat khong?') 
        if tra_loi =='yes' :
           
           self.destroy() # hủy lớp self


if __name__ == '__main__':
    # Khởi tạo ứng dụng
    app = FaceDetectionGUI()
    # Chạy ứng dụng
    app.mainloop()