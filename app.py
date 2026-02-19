import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter.font import Font
import os

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("记事本 - 未命名")
        self.root.geometry("800x600")
        
        # 核心变量
        self.file_path = None  # 当前文件路径
        self.current_language = "en"  # 默认语言
        
        # 菜单文本映射（统一管理多语言文本）
        self.lang_texts = {
            "en": {
                "menu_file": "File",
                "menu_edit": "Edit",
                "menu_language": "Language",
                "menu_help": "Help",
                "file_new": "New",
                "file_open": "Open",
                "file_save": "Save",
                "file_save_as": "Save As",
                "file_exit": "Exit",
                "edit_cut": "Cut",
                "edit_copy": "Copy",
                "edit_paste": "Paste",
                "edit_undo": "Undo",
                "edit_redo": "Redo",
                "edit_select_all": "Select All",
                "lang_zh_CN": "Simplified Chinese",
                "lang_zh_TW": "Traditional Chinese",
                "lang_en": "English",
                "help_about": "About",
                "title_untitled": "Notepad - Untitled",
                "prompt_save": "Save changes to untitled file?",
                "prompt_title": "Prompt",
                "about_title": "About Notepad",
                "about_content": "Notepad\nAuthor: system_mini\nVersion: V 1.35\nA simple and lightweight notepad replacement."
            },
            "zh_CN": {
                "menu_file": "文件",
                "menu_edit": "编辑",
                "menu_language": "语言",
                "menu_help": "帮助",
                "file_new": "新建",
                "file_open": "打开",
                "file_save": "保存",
                "file_save_as": "另存为",
                "file_exit": "退出",
                "edit_cut": "剪切",
                "edit_copy": "复制",
                "edit_paste": "粘贴",
                "edit_undo": "撤销",
                "edit_redo": "重做",
                "edit_select_all": "全选",
                "lang_zh_CN": "简体中文",
                "lang_zh_TW": "繁体中文",
                "lang_en": "English",
                "help_about": "关于",
                "title_untitled": "记事本 - 未命名",
                "prompt_save": "是否保存未命名文件的更改？",
                "prompt_title": "提示",
                "about_title": "关于记事本",
                "about_content": "记事本\n作者: system_mini\n版本: V 1.35\n一个简单轻量的记事本替代工具。"
            },
            "zh_TW": {
                "menu_file": "檔案",
                "menu_edit": "編輯",
                "menu_language": "語言",
                "menu_help": "說明",
                "file_new": "新建",
                "file_open": "開啟",
                "file_save": "儲存",
                "file_save_as": "另存為",
                "file_exit": "退出",
                "edit_cut": "剪下",
                "edit_copy": "複製",
                "edit_paste": "貼上",
                "edit_undo": "撤銷",
                "edit_redo": "重做",
                "edit_select_all": "全選",
                "lang_zh_CN": "簡體中文",
                "lang_zh_TW": "繁體中文",
                "lang_en": "English",
                "help_about": "關於",
                "title_untitled": "記事本 - 未命名",
                "prompt_save": "是否儲存未命名檔案的變更？",
                "prompt_title": "提示",
                "about_title": "關於記事本",
                "about_content": "記事本\n作者: system_mini\n版本: V 1.35\n一個簡單輕量的記事本替代工具。"
            }
        }
        
        # 设置字体
        self.font = Font(family="Consolas", size=14)
        
        # 文本编辑区域
        self.text_area = scrolledtext.ScrolledText(root, font=self.font, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill=tk.BOTH)
        self.text_area.bind("<KeyRelease>", self.apply_syntax_highlighting)  # 实时高亮
        
        # 初始化菜单栏（核心修复：重新创建菜单的方式修改顶级菜单文本）
        self.create_menubar()
        
        # 初始语法高亮
        self.apply_syntax_highlighting()

    # 核心修复：重新创建菜单栏（解决顶级菜单无法修改label的问题）
    def create_menubar(self):
        # 先销毁旧菜单（如果存在）
        try:
            self.root.config(menu="")
        except:
            pass
        
        # 创建新菜单栏
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # 获取当前语言的文本
        texts = self.lang_texts[self.current_language]
        
        # ===== 文件菜单 =====
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=texts["menu_file"], menu=self.file_menu)
        self.file_menu.add_command(label=texts["file_new"], command=self.new_file)
        self.file_menu.add_command(label=texts["file_open"], command=self.open_file)
        self.file_menu.add_command(label=texts["file_save"], command=self.save_file)
        self.file_menu.add_command(label=texts["file_save_as"], command=self.save_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label=texts["file_exit"], command=self.confirm_exit)
        
        # ===== 编辑菜单 =====
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=texts["menu_edit"], menu=self.edit_menu)
        self.edit_menu.add_command(label=texts["edit_cut"], command=lambda: self.text_area.event_generate("<<Cut>>"))
        self.edit_menu.add_command(label=texts["edit_copy"], command=lambda: self.text_area.event_generate("<<Copy>>"))
        self.edit_menu.add_command(label=texts["edit_paste"], command=lambda: self.text_area.event_generate("<<Paste>>"))
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label=texts["edit_undo"], command=self.undo)
        self.edit_menu.add_command(label=texts["edit_redo"], command=self.redo)
        self.edit_menu.add_command(label=texts["edit_select_all"], command=self.select_all)
        
        # ===== 语言菜单 =====
        self.language_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=texts["menu_language"], menu=self.language_menu)
        self.language_menu.add_command(label=self.lang_texts["zh_CN"]["lang_zh_CN"], command=lambda: self.change_language("zh_CN"))
        self.language_menu.add_command(label=self.lang_texts["zh_TW"]["lang_zh_TW"], command=lambda: self.change_language("zh_TW"))
        self.language_menu.add_command(label=self.lang_texts["en"]["lang_en"], command=lambda: self.change_language("en"))
        
        # ===== 帮助菜单 =====
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=texts["menu_help"], menu=self.help_menu)
        self.help_menu.add_command(label=texts["help_about"], command=self.about)

    # 切换语言（核心修复：重新创建菜单）
    def change_language(self, language):
        self.current_language = language
        self.create_menubar()  # 重新创建菜单，自动应用新语言
        self.update_title()    # 更新窗口标题

    # 语法高亮（修复后）
    def apply_syntax_highlighting(self, event=None):
        # 清空旧标签
        for tag in ["english", "number", "punctuation", "space"]:
            self.text_area.tag_remove(tag, 1.0, tk.END)
        
        # 配置标签样式
        self.text_area.tag_configure("english", foreground="#008000")  # 深绿
        self.text_area.tag_configure("number", foreground="#FF4500")   # 橙红
        self.text_area.tag_configure("punctuation", foreground="#DC143C") # 深红
        self.text_area.tag_configure("space", background="#F5F5F5")   # 浅灰
        
        # 逐字符遍历
        content = self.text_area.get(1.0, tk.END)
        current_pos = 1.0
        for char in content:
            next_pos = self.text_area.index(f"{current_pos} + 1 char")
            if char.isalpha():
                self.text_area.tag_add("english", current_pos, next_pos)
            elif char.isdigit():
                self.text_area.tag_add("number", current_pos, next_pos)
            elif char in ",.!?;:'\"-()[]{}<>":
                self.text_area.tag_add("punctuation", current_pos, next_pos)
            elif char == ' ':
                self.text_area.tag_add("space", current_pos, next_pos)
            current_pos = next_pos

    # 文件操作
    def new_file(self):
        if self.check_unsaved_changes():
            self.text_area.delete(1.0, tk.END)
            self.file_path = None
            self.update_title()

    def open_file(self):
        if self.check_unsaved_changes():
            file_path = filedialog.askopenfilename(
                filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
            )
            if file_path:
                self.file_path = file_path
                with open(file_path, "r", encoding='utf-8') as f:
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, f.read())
                self.update_title()

    def save_file(self):
        if self.file_path:
            with open(self.file_path, "w", encoding='utf-8') as f:
                f.write(self.text_area.get(1.0, tk.END))
        else:
            self.save_as()

    def save_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if file_path:
            self.file_path = file_path
            self.save_file()
            self.update_title()

    # 辅助功能
    def update_title(self):
        texts = self.lang_texts[self.current_language]
        if self.file_path:
            self.root.title(f"{texts['menu_file'].replace('檔案', '記事本').replace('文件', '记事本')} - {os.path.basename(self.file_path)}")
        else:
            self.root.title(texts["title_untitled"])

    def check_unsaved_changes(self):
        content = self.text_area.get(1.0, tk.END).strip()
        if content and not self.file_path:
            texts = self.lang_texts[self.current_language]
            result = messagebox.askyesnocancel(texts["prompt_title"], texts["prompt_save"])
            if result:
                self.save_as()
                return True
            elif result is None:
                return False
        return True

    def confirm_exit(self):
        if self.check_unsaved_changes():
            self.root.quit()

    def undo(self):
        try:
            self.text_area.edit_undo()
        except:
            pass

    def redo(self):
        try:
            self.text_area.edit_redo()
        except:
            pass

    def select_all(self):
        self.text_area.tag_add(tk.SEL, 1.0, tk.END)
        self.text_area.mark_set(tk.INSERT, 1.0)

    def about(self):
        texts = self.lang_texts[self.current_language]
        messagebox.showinfo(texts["about_title"], texts["about_content"])

if __name__ == "__main__":
    root = tk.Tk()
    app = Notepad(root)
    root.mainloop()