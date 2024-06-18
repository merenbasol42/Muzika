from tkinter import Misc, simpledialog, messagebox
import customtkinter as ctk

def ask_int_input(
    parent:Misc = None,
    inp_title:str = "Girdi",
    inp_text:str = "Lütfen bir sayı giriniz",
    err_title:str = "Girdi Hatası",
    err_text:str = "Hatalı girdi lütfen bir sayı giriniz"
    ) -> int | None:
    '''
        Sayısal bir değer alana kadar sormaya devam eder.\n
        Girdi strip() metoduyla ayıklanır\n
        Boşluk karekteri girmesi veya hiçbir şey girmemesi durumunda "None" değeri döndürür\n
        Düzgün veri girdisine karşılık girilen değeri "int" türüne dönüştürüp döndürür\n
    '''

    while True:
        inp = simpledialog.askstring(
            title=inp_title,
            prompt=inp_text,
            parent=parent
        )
        if inp == None:
            return None
        inp = inp.strip()
        if inp == "": # Belki de adam sadece boşluk karakteri girdi
            return None
        try:
            _id = int(inp)
        except:
            messagebox.showerror(err_title, err_text)
            continue
        return _id

def ask_str_input(
    parent:Misc = None,
    inp_title:str = "Girdi!",
    inp_text:str = "Lütfen bir string değer giriniz"   
) -> str | None:
    '''
        Girdi strip() metoduyla ayıklanır\n
        Boşluk karekteri girmesi veya hiçbir şey girmemesi durumunda "None" değeri döndürür\n
    '''

    inp = simpledialog.askstring(
        title=inp_title,
        prompt=inp_text,
        parent=parent
    )
    
    if inp == None: return inp
    inp = inp.strip()
    if inp == "": return None
    return inp

def ask_str_input_plus(
    parent:Misc = None,
    control_list:list = [], 
    should_i_do_lowercase:bool = False,
    inp_title:str = "Girdi!",
    inp_text:str = "Lütfen bir string değer giriniz"   
) -> str | None:
    '''
        Girdi strip() metoduyla ayıklanır\n
        Boşluk karekteri girmesi veya hiçbir şey girmemesi durumunda "None" değeri döndürür\n
        Eğer kontrol listesi verilmişse kontrol listesinde yoksa tekrar sorar
    '''

    while True:
        inp = ask_str_input(
            parent=parent,
            inp_title=inp_title,
            inp_text=inp_text
        )
        if inp is None:
            return
        if should_i_do_lowercase:
            inp = inp.lower()
        if inp in control_list or len(control_list) == 0:
            return inp
        else:
            # Dönmeye dewam
            messagebox.showwarning("Hatalı girdi", "Tekrar deneyiniz yada iptal ediniz")

def ask_two_strings(
        parent:Misc,
        toplevel_title:str = "String Input Penceresi",
        first_inp_text:str = "İlk string:",
        second_inp_text:str = "İkinci String:",
        button_name:str = "Girişleri Al"
        
    ) -> list[str] | None:

    def on_button_click():
        string1 = entry1.get().strip()
        string2 = entry2.get().strip()
        top.destroy()  # Topleveli kapat
        result.append(string1)
        result.append(string2)

    top = ctk.CTkToplevel(parent)
    top.geometry("300x250")
    top.title(toplevel_title)

    label1 = ctk.CTkLabel(top, text=first_inp_text)
    label1.pack(pady=10)

    entry1 = ctk.CTkEntry(top)
    entry1.pack(pady=5)

    label2 = ctk.CTkLabel(top, text=second_inp_text)
    label2.pack(pady=10)

    entry2 = ctk.CTkEntry(top)
    entry2.pack(pady=5)

    button = ctk.CTkButton(top, text=button_name, command=on_button_click)
    button.pack(pady=20)

    result = []
    top.wait_window()  # Toplevel kapanana kadar bekle

    # Boş mu kontorl
    try: result.index("")
    except Exception: return result if len(result) != 0 else None
    return None

def ask_str_by_combox(
        result_cb,
        parent: Misc = None,
        combox_list: list = [], 
        inp_title: str = "Girdi!",
        inp_text: str = "Lütfen bir string değer giriniz"
    ) -> str | None:

    wn = ctk.CTkToplevel(master=parent)

    def ok_cb():
        result_cb(combox.get())
        wn.destroy()

    def exit_cb():
        result_cb(None)
        wn.destroy()

    # Ana pencerenin boyutlarını al
    if parent is not None:
        parent.update_idletasks()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()

        # Toplevel pencerenin boyutlarını hesapla
        width = 250
        height = 320
        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)
        wn.geometry(f"{width}x{height}+{x}+{y}")
    else:
        wn.geometry("250x320")

    wn.title(inp_title)
    wn.protocol("WM_DELETE_WINDOW", exit_cb)

    label = ctk.CTkLabel(master=wn, text=inp_text, wraplength=200)
    combox = ctk.CTkComboBox(master=wn, values=combox_list)
    okbutton = ctk.CTkButton(master=wn, text="OK", command=ok_cb)

    label.pack(pady=(50, 20))
    combox.pack(pady=20)
    okbutton.pack(pady=20)

