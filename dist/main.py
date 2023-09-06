import pickle
import tkinter as tk
import pyttsx3
import datetime
from tkinter import Text, Scrollbar


class Dictionary:
    def __init__(self):
        self.dictionary = self.loadDict()
        self.menu_window = None
        self.function_frame = None
        self.log_file = 'LOG.txt'

    def write_log(self, content):
        with open(self.log_file, mode='a', encoding='utf-8') as file:
            file.write(f'{content}\n')

    def loadDict(self):
        try:
            with open('dictionary.pkl', 'rb') as file:
                content = pickle.load(file)
        except FileNotFoundError:
            content = []

        contents = [content[i].replace('+', ':').replace('* ', '* Loại từ:').replace('=', '\t>> Example: ').replace('!', '\t>> Example: ').replace('- ', '> Nghĩa: ') for i in range(len(content))]
        dictionary = {}
        for line in contents:
            if line.startswith('@'):
                values = ''
                try:
                    idx = line.find(' /')
                    key = line[1: idx]
                    values += f'Phiên âm:{line[idx:]}'
                except:
                    key = line[1:]
            else:
                values += line

            dictionary[key] = values

        return dictionary

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")        

    def create_menu(self):
        self.menu_window = tk.Tk()
        self.menu_window.title("Dictionary Menu")
        self.menu_window.iconbitmap('icon.ico')

        # Gọi hàm để đặt kích thước cửa sổ và vị trí ở trung tâm
        self.center_window(self.menu_window, 1280, 720)

        # Tạo một khung chứa menu bên trái
        menu_frame = tk.Frame(self.menu_window, width=200, bg="lightgray")
        menu_frame.pack(side='left', fill='y')
        menu_label = tk.Label(menu_frame, text="Select an option:", font=('Helvetica', 14))
        menu_label.pack(pady=5)

        # Tạo một khung chứa các chức năng bên phải
        self.function_frame = tk.Frame(self.menu_window)
        self.function_frame.pack(side='right', fill='both', expand=True)

        # Load the background image
        background_image = tk.PhotoImage(file='background_galaxy.png')
        background_label = tk.Label(self.function_frame, image=background_image)
        background_label.place(relwidth=1, relheight=1)

        button_width = 20  # Set a fixed width for buttons

        search_button = tk.Button(menu_frame, text="Search a word", command=self.open_search, width=button_width)
        search_button.pack(pady=5)

        add_button = tk.Button(menu_frame, text="Insert a new word", command=self.open_add, width=button_width)
        add_button.pack(pady=5)

        delete_button = tk.Button(menu_frame, text="Delete a word", command=self.open_delete, width=button_width)
        delete_button.pack(pady=5)

        exit_button = tk.Button(menu_frame, text="Exit", command=self.menu_window.destroy, width=button_width)
        exit_button.pack(pady=5)

        group_label = tk.Label(menu_frame, text="Members:\n13. Hay Tran\n14. Duong Hiep\n15. Hong Hung\n16. Quang Huy\n17. Gia Linh\n18. Anh Minh", font=('Times', 15), bg='lightgray', justify='left')
        group_label.pack(side='bottom', pady=10)
        
        self.menu_window.mainloop()

    def open_search(self):
        self.clear_function_frame()
        search_frame = tk.Frame(self.function_frame)
        search_frame.pack(padx=20, pady=20)

        search_label = tk.Label(search_frame, text="Search a word:")
        search_label.pack(anchor='w', pady=5)
        self.search_entry = tk.Entry(search_frame, font=('Times', 20))
        self.search_entry.pack(fill='x', padx=5, pady=5)
        search_button = tk.Button(search_frame, text="Search", command=self.searchWord, width=20)
        search_button.pack()

        # Thêm nút phát âm
        pronounce_button = tk.Button(search_frame, text="Pronounce", command=self.pronounce, width=20)
        pronounce_button.pack(anchor='center', pady=5)


        back_button = tk.Button(search_frame, text="Back to Home", command=self.back_to_home, width=20)
        back_button.pack(anchor='center')

        # Tạo thanh cuộn
        scrollbar = Scrollbar(search_frame)
        scrollbar.pack(side='right', fill='y')

        # Tạo một widget văn bản để hiển thị kết quả và liên kết với thanh cuộn
        self.result_text = Text(search_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, font=('Times', 13))
        self.result_text.pack(fill='both', expand=True, padx=5, pady=5)
        scrollbar.config(command=self.result_text.yview)

        #self.result_label = tk.Label(self.function_frame, text="", justify='left', font=('Times', 13))
        #self.result_label.pack()

    def open_add(self):
        self.clear_function_frame()
        add_frame = tk.Frame(self.function_frame)
        add_frame.pack(padx=20, pady=20)
        add_label = tk.Label(add_frame, text="Insert a new word:")
        add_label.pack(anchor='w', pady=5)
        self.new_word_entry = tk.Entry(add_frame, font=('Times', 18))
        self.new_word_entry.pack(fill='x', padx=5, pady=5)
        meaning_label = tk.Label(add_frame, text="Translate to Vietnamese:")
        meaning_label.pack(anchor='w', pady=5)
        self.meaning_entry = tk.Entry(add_frame, font=('Times', 18))
        self.meaning_entry.pack(fill='x', padx=5, pady=5)
        add_button = tk.Button(add_frame, text="Insert", command=self.addNewWords, width=20)
        add_button.pack()

        back_button = tk.Button(add_frame, text="Back to Home", command=self.back_to_home, width=20)
        back_button.pack(anchor='center', pady=5)

        self.result_label = tk.Label(self.function_frame, text="", justify='left')
        self.result_label.pack()

    def open_delete(self):
        self.clear_function_frame()
        delete_frame = tk.Frame(self.function_frame)
        delete_frame.pack(padx=20, pady=20)
        delete_label = tk.Label(delete_frame, text="Delete a word:")
        delete_label.pack(anchor='w', pady=5)
        self.delete_entry = tk.Entry(delete_frame, font=('Times', 18))
        self.delete_entry.pack(fill='x', padx=5, pady=5)
        delete_button = tk.Button(delete_frame, text="Delete", command=self.deleteWord, width=20)
        delete_button.pack()

        back_button = tk.Button(delete_frame, text="Back to Home", command=self.back_to_home, width=20)
        back_button.pack(anchor='center', pady=5)

        self.result_label = tk.Label(self.function_frame, text="", justify='left')
        self.result_label.pack()
        
    def clear_function_frame(self):
        for widget in self.function_frame.winfo_children():
            widget.destroy()

    def back_to_home(self):
        # Đóng cửa sổ hiện tại (sub-frame)
        self.menu_window.destroy()
        
        # Hiển thị lại trang chính (menu)
        self.create_menu()

    #def pronounce(self):
    #    word = self.search_entry.get().lower()
    #    if word:
    #        try:
    #            # Sử dụng pyttsx3 để phát âm
    #            self.engine.say(word)
    #            self.engine.runAndWait()

    #        except Exception as e:
    #            self.result_label.config(text="Error while pronouncing.")

    def pronounce(self):
        word = self.search_entry.get().lower()
        if word:
            try:
                # Tạo một đối tượng `SpeechSynthesis` để tùy chỉnh tốc độ đọc
                speech = pyttsx3.init()

                # Lấy thông số hiện tại của giọng nói
                voice_properties = speech.getProperty('voices')[0]

                # Thiết lập tốc độ đọc (rate) thành một giá trị tùy chỉnh (vd: 100, bạn có thể thay đổi giá trị này)
                speech.setProperty('rate', 130)  # Thay đổi giá trị 150 thành tốc độ đọc mong muốn

                # Sử dụng pyttsx3 để phát âm
                speech.say(word)
                speech.runAndWait()

            except Exception as e:
                self.result_label.config(text="Error while pronouncing.")

    def searchWord(self):
        word = self.search_entry.get().lower()
        if word not in self.dictionary:
            self.result_text.config(state='normal')  # Cho phép chỉnh sửa nội dung trong Text widget
            self.result_text.delete('1.0', tk.END)  # Xóa toàn bộ nội dung trong Text widget
            self.result_text.insert(tk.END, f'{word} not found!')
            self.result_text.config(state='disabled')  # Vô hiệu hóa chỉnh sửa nội dung trong Text widget
        else:
            self.result_text.config(state='normal')  # Cho phép chỉnh sửa nội dung trong Text widget
            self.result_text.delete('1.0', tk.END)  # Xóa toàn bộ nội dung trong Text widget
            self.result_text.insert(tk.END, self.dictionary[word])
            self.result_text.config(state='disabled')  # Vô hiệu hóa chỉnh sửa nội dung trong Text widget

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.write_log(f'{timestamp}---Search: {word}')
            

    def addNewWords(self):
        new_word = self.new_word_entry.get().lower()
        keys = self.dictionary.keys()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if new_word in keys:
            self.result_label.config(text='This word already exists, please choose another word!')
            self.write_log(f"{timestamp}---(Add) '{new_word}' already exists")
        else:
            meaning = self.meaning_entry.get()
            self.dictionary[new_word] = meaning
            with open('dictionary.pkl', 'rb') as file:
                content = pickle.load(file)
            content.append(f'@{new_word}\n')
            content.append(f'- {meaning.strip()}\n')
            with open('dictionary.pkl', 'wb') as file:
                pickle.dump(content, file)
            self.result_label.config(text=f'New word: {new_word}\nMeaning: {meaning}\n')
            self.write_log(f'{timestamp}---Add: {new_word}')
            

    def deleteWord(self):
        word = self.delete_entry.get().lower().strip()
        keys = self.dictionary.keys()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if word not in keys:
            self.result_label.config(text='Not found, please choose another word!', font=(24))
            self.write_log(f"{timestamp}---(Delete) '{word}' Not found!")
        else:
            with open('dictionary.pkl', 'rb') as file:
                content = pickle.load(file)

            idx1 = None
            idx2 = None

            for index, value in enumerate(content):
                if value.startswith(f'@{word}'):
                    idx1 = index
                    break
            
            for index, value in enumerate(content[idx1+1:]):
                if value.startswith('@'):
                    idx2 = index + idx1
                    break

            del content[idx1:idx2]
            with open('dictionary.pkl', 'wb') as file:
                pickle.dump(content, file)
            self.result_label.config(text=f'Deleted {word} successfully!')
            self.write_log(f'{timestamp}---Delete: {word}')


    def menu(self):
        self.create_menu()

if __name__ == "__main__":
    Dictionary().menu()
