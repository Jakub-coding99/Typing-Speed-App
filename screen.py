
from tkinter import *
from tkinter import messagebox



class Screen:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("900x500+400+200")
        self.window.title("Typing Speed App")
        self.window.config(pady=30,padx=30,background="black")
        self.control_text = []
        self.name_var= StringVar()
        self.type_input = Entry()
        self.index = 0
        self.mistakes = 0
        self.count_press = 0
        self.type_input = Entry(background="white",width=100,font=("Arial",15),textvariable=self.name_var)
        self.type_input.bind ("<KeyRelease>", lambda event: self.write())
        self.type_input.bind("<BackSpace>", self.backspace)
        self.corrected_mistake = 0
        self.seconds = 60 # choose your second timer
        self.intro()
        self.words = self.get_text()
        self.succes_rate()
        for i in range(6):
            self.window.columnconfigure(i, weight=1)
        
        self.window.mainloop()

   
    def write(self):

        if len(self.control_text) == 0:
            self.count_down(self.seconds)
        i = self.type_input.get()
        self.control_text.append(i)
        
        
        for i in range(len(self.control_text)):
            for x in self.control_text:
                self.entry_list =list(x)
        for x in range(len(self.control_text)):
           self.control()  
    
    
            

    def control(self):
        self.update_statistics()
        try:
           
            if self.words_list[self.index] == self.entry_list[self.index]:
                self.mark_correct()
                self.update_statistics()
                

            elif self.words_list[self.index] != self.entry_list[self.index] and len(self.entry_list) > self.index:
                self.mark_wrong()
                self.update_statistics()
            
        
        except IndexError:
            pass
    
        
    def backspace(self, event):
        self.index -=1
        try:
            x = self.entry_list.index(self.entry_list[-1])
            if x >= 0:
                tag_names = self.word_label.tag_names(f"1.{self.index}")
                if "red" in tag_names:
                    self.corrected_mistake +=1
                
                delete = self.entry_list.pop(x)     
                self.word_label.tag_remove("red",f"1.{self.index}", f"1.{self.index + 1}")
                self.word_label.tag_remove("green",f"1.{self.index}", f"1.{self.index + 1}")
                self.control()
        
        except (IndexError, AttributeError):
            pass
    
    

    def count_down(self,count):
        
        if count >= 0:
            minutes, second = divmod(count, 60)
            self.timer.config(text = f"TIME: {minutes:02d}:{second:02d}")
            if count < 5:
                
                self.timer.config(fg="red")
            
            if count >0:
                t = self.window.after(1000,self.count_down, count -1)
            
            else:
                try:
                    
                    self.window.after_cancel(self.end())

                except ValueError:
                    pass
            

    def widgets(self):
        
        stats_frame = Frame(self.window, bg="black")
        stats_frame.grid(row=1,column=1, sticky="e",pady=10)

        #characters per minute
        self.cpm = Label(stats_frame,text=f"CPM: {self.count_press}", fg="WHITE",bg="black", font=("Arial",15))
        self.cpm.pack(side="right",padx=5)
        
        self.wpm_widget = Label(stats_frame,text=f"WPM: {self.wpm()}", fg="WHITE",bg="black", font=("Arial",15))
        self.wpm_widget.pack(side="right",padx=5)

        
        self.accuraccy_percentage = Label(stats_frame,text=f"{self.succes_rate()} %", fg="green",bg="black", font=("Arial",15))
        self.accuraccy_percentage.pack(side="right",padx=5)

        self.accuraccy = Label(stats_frame,text="ACCURACY: ", fg="WHITE",bg="black", font=("Arial",15))
        self.accuraccy.pack(side="right",)



        # mistakes widget
        self.mistake_count = Label(stats_frame,text = self.mistakes, fg="red",bg="black", font=("Arial",15))
        self.mistake_count.pack(side="right",padx=5)

        self.mistake_widget = Label(stats_frame,text = "Mistakes:", fg="WHITE",bg="black", font=("Arial",15))
        self.mistake_widget.pack(side="right")

        
        minutes,second = divmod(self.seconds, 60)
        self.timer = Label(stats_frame, text=f"TIME: {minutes:02d}:{second:02d}", fg="WHITE",bg="black", font=("Arial",15))
        self.timer.pack(side="right", padx=5)
    
    def intro(self):
        self.window.rowconfigure(2,weight=1)
        title_label = Label(text="Typing speed test",fg="white", width=20,background="black",font=("Arial",25),)
        title_label.grid(row=0,column=0,columnspan=5,sticky="n")
        
        
        self.start_btn = Button(text="Start", fg="black", background="white",font=("Arial",20),command=self.start)
        self.start_btn.grid(row=3,column=2)

        self.instruction_btn = Button(text="Instructions", fg="black", background="white",font=("Arial",20),command= self.instructions)
        self.instruction_btn.grid(row=2,column=2)
        

    def instructions(self):
        instruction_window = Toplevel(self.window)
        instruction_window.title("Instructions")
        instruction_window.geometry("700x350+1100+250")
        instruction_window.config(bg="black", padx=20, pady=20)

        
        
        self.instructions_label = Label(instruction_window,text="Welcome to Typing Test App!\n"
                                            "Start by clicking on Start.\n"
                                            "Click to entry point, once you start typing the countdown is on! \n"
                                            "If you type incorrect characters you can delete and type it correctly,\n" \
                                            "however it will count as mistake"
                                            
                                            "\n"
                                            "Explanation: \n"
                                            "  - CPM - characters per minute \n"
                                            "  - WPM - words per minute (5 correct characters) \n"
                                            "  - MISTAKES - number of wrong characters \n"
                                            "  - ACCURACY - percentage of correct characters"
                                            ,
                                   
                                   background="black",font=("Arial",15, "bold"),fg="red",justify=LEFT,
        )
        self.instructions_label.grid(row=2, column=1,columnspan=3, sticky="ew", ipady=18)
        
        def check_mapped():
            if self.instructions_label.winfo_ismapped():
                self.instruction_btn.config(state="disabled")
        
        self.window.after(100,check_mapped)
        instruction_window.protocol("WM_DELETE_WINDOW",lambda:self.close_window(instruction_window))
        
    def close_window(self,window):
        window.destroy()
        self.instruction_btn.config(state="normal")
    
    
    def get_text(self):
        import random
        import os
        path = os.path.join(os.path.dirname(__file__), "words.txt")
        with open(path,"r") as self.words:
            print(self.words)
            x = self.words.read().splitlines()
            database = random.choices(x, k=500)
            return database
            
            
        
    def start(self):
    
        self.instruction_btn.destroy()
        
        self.widgets()
        self.type_input.grid(row = 4,column=0, columnspan=4, sticky="ew", pady=10)
        
        self.restart = Button(text="RESTART", bg="black",fg="white",padx=5,command=self.restart_game )
        self.restart.grid(row= 5,columnspan=4)
        
        
        self.write_below = Label(text="WRITE BELOW:",fg="white",bg="black")
        self.write_below.grid(row=3,column =0,sticky="w")
        
        
        #adding space after each word
        text = " ".join(self.words)
        list_with_spaces = list(text)
        
        #giving every letter an element
        self.words_list = []
        for i in list_with_spaces: 
            
            for y in i:
                self.words_list.append(y)
        
        self.start_btn.destroy()
        
        #creating text widget with words
        self.word_label = Text(self.window,width=100, font=("Arial",15),height=2,fg="white",bg="black")
        text_1 = self.words
        self.word_label.tag_configure("green",foreground="green")
        self.word_label.tag_configure("red",foreground="red")
        self.word_label.tag_configure("white",foreground="white")
        self.word_label.insert(END,text_1)
        
        self.word_label.grid(row=2,column=0, columnspan=4,ipady = 30)

    
  
    def update_statistics(self):
        self.accuraccy_percentage.config(text =f"{self.succes_rate()} %")
        self.cpm.config(text=f"CPM: {self.count_press}")
        self.wpm_widget.config(text=f"WPM: {self.wpm()}")
        self.mistake_count.config(text = self.mistakes )
        
    

    def mark_correct(self):
        
        self.word_label.tag_add("green", f"1.{self.index}", f"1.{self.index + 1}")
        self.index += 1
        self.count_press += 1
        if self.corrected_mistake > 0 and self.mistakes > 0:
            self.corrected_mistake -= 1
    
    def mark_wrong(self):
    
        self.word_label.tag_add("red", f"1.{self.index}", f"1.{self.index + 1}")
        self.index += 1
        self.mistakes += 1
        


    def succes_rate(self):
       try:
        mist_count = len(self.entry_list) - self.mistakes
        perc = mist_count / len(self.entry_list)  * 100
        rounded_perc = round(perc,1)
        
        if rounded_perc < 0:
            return 0.0
        
        else:
            return rounded_perc
       except (ZeroDivisionError,AttributeError, TypeError):
           return 0.0
       


    def wpm(self):
        try:
            correct_chars = len(self.entry_list) - self.mistakes
            words = correct_chars // 5
            if words < 0:
                return 0
            else:
                return words
        except AttributeError:
            return 0


        
    def end(self):
        with open("result.txt", "a") as data:
            data.write(f"WPM: {self.wpm()}, CPM: {self.count_press}, Accuracy: {self.succes_rate()}%, Time: {self.seconds} seconds\n")
        messagebox.showinfo("Type Speed Test", f"Your WPM: {self.wpm()}, CPM:{self.count_press}, Accuracy: {self.succes_rate()}%")
        self.type_input.config(state="disabled")
        
    
    def restart_game(self):
        self.window.destroy()
        screen = Screen()
        
        







