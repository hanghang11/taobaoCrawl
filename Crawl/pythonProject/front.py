import pathlib
import pyperclip as pc
from queue import Queue
from tkinter.filedialog import askdirectory
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import utility
from tkinter import *
import Crawl
class FileSearchEngine(ttk.Frame):

    queue = Queue()
    searching = False

    def __init__(self, master):
        super().__init__(master, padding=15)
        self.pack(fill=BOTH, expand=YES)

        # application variables
        _path = str(3)
        self.path_var = ttk.StringVar(value=_path)
        self.term_var = ttk.StringVar(value='input keywords')
        self.type_var = ttk.StringVar(value='endswidth')

        # header and labelframe option container
        option_text = "Complete the form to begin your search"
        self.option_lf = ttk.Labelframe(self, text=option_text, padding=15)
        self.option_lf.pack(fill=X, expand=YES, anchor=N)

        self.create_path_row()
        self.create_term_row()
        self.create_type_row()
        self.create_results_view()

        self.progressbar = ttk.Label(
            master=self,
            bootstyle=INFO,
            text='debug info'
        )
        self.progressbar.pack(fill=X, expand=YES)

    def create_path_row(self):
        """Add path row to labelframe"""
        path_row = ttk.Frame(self.option_lf)
        path_row.pack(fill=X, expand=YES)
        path_lbl = ttk.Label(path_row, text="Pagenum", width=8)
        path_lbl.pack(side=LEFT, padx=(15, 0))
        path_ent = ttk.Entry(path_row, textvariable=self.path_var)
        path_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)
        browse_btn = ttk.Button(
            master=path_row,
            text="Confirm",
            # command=self.on_browse,
            width=8
        )
        browse_btn.pack(side=LEFT, padx=5)

    def clearTable(self,tree):
        x = tree.get_children()
        for item in x:
            tree.delete(item)

    def showPopoutMenu(self,w, menu):
        def popout(event):
            menu.post(event.x + w.winfo_rootx(), event.y + w.winfo_rooty())
            w.update()
        w.bind('<Button-3>', popout)

    # 复制选中值(选中的行，list形式复制)
    def copy_from_treeview(self, tree, event):
        selection = tree.selection()
        # column = tree.identify_column(event.x)
        # column_no = int(column.replace("#", "")) - 1
        copy_values = []

        try:
            value = tree.item(selection)["values"][0]
            copy_values.append(str(value))
        except:
            pass
        copy_string = "\n".join(copy_values)
        pc.copy(copy_string)

    def BeginCrawl(self):
        print("事件")
        # 复制选中行到剪切板
        self.resultview.bind("<Control-Key-c>", lambda x: self.copy_from_treeview(self.resultview, x))

        menu = Menu()
        menu.add_cascade(label='copy')
        # menu.add_cascade(label='功能二')
        self.showPopoutMenu(self.resultview, menu)
        self.clearTable(self.resultview)
        lists = [{"name": "yang", "gender": "男", "age": "18"}, {"name": "郑", "gender": "女", "age": "25"}]

        # keyword = self.term_var
        pagenum = int(self.path_var.get())
        lists = Crawl.crawl(1,pagenum)
        # print(list)
        i = 0
        for v in lists:
            # print(v)
            self.resultview.insert('', i, values = (v[3],v[1],v[4]))
        # for v in lists:
        #     print(v)
        #     self.resultview.insert('', i, values = (v.get('name'),v.get('gender'),v.get('age')))
        self.progressbar.config(text=str(len(lists))+' found')


    #搜索按钮
    def create_term_row(self):
        """Add term row to labelframe"""
        term_row = ttk.Frame(self.option_lf)
        term_row.pack(fill=X, expand=YES, pady=15)
        term_lbl = ttk.Label(term_row, text="Keywords", width=8)
        term_lbl.pack(side=LEFT, padx=(15, 0))
        term_ent = ttk.Entry(term_row, textvariable=self.term_var)
        term_ent.pack(side=LEFT, fill=X, expand=YES, padx=5)
        search_btn = ttk.Button(
            master=term_row,
            text="Search",
            # command=self.on_search,
            bootstyle=OUTLINE,
            width=8,
            command=self.BeginCrawl
        )
        search_btn.pack(side=LEFT, padx=5)

    def create_type_row(self):
        """Add type row to labelframe"""
        type_row = ttk.Frame(self.option_lf)
        type_row.pack(fill=X, expand=YES)
        type_lbl = ttk.Label(type_row, text="Type", width=8)
        type_lbl.pack(side=LEFT, padx=(15, 0))

        contains_opt = ttk.Radiobutton(
            master=type_row,
            text="Chrome",
            variable=self.type_var,
            value="contains"
        )
        contains_opt.pack(side=LEFT)

        startswith_opt = ttk.Radiobutton(
            master=type_row,
            text="Firefox",
            variable=self.type_var,
            value="startswith"
        )
        startswith_opt.pack(side=LEFT, padx=15)

        endswith_opt = ttk.Radiobutton(
            master=type_row,
            text="Edge",
            variable=self.type_var,
            value="endswith"
        )
        endswith_opt.pack(side=LEFT)
        endswith_opt.invoke()

    def create_results_view(self):
        """Add result treeview to labelframe"""
        self.resultview = ttk.Treeview(
            master=self,
            bootstyle=INFO,
            columns=[0, 1, 2, 3, 4],
            show=HEADINGS
        )
        self.resultview.pack(fill=BOTH, expand=YES, pady=10)

        # setup columns and use `scale_size` to adjust for resolution
        self.resultview.heading(0, text='Name', anchor=W)
        self.resultview.heading(1, text='Price', anchor=W)
        self.resultview.heading(2, text='Location', anchor=E)
        self.resultview.heading(3, text='URL', anchor=E)
        # self.resultview.heading(4, text='Path', anchor=W)
        self.resultview.column(
            column=0,
            anchor=W,
            width=utility.scale_size(self, 125),
            stretch=False
        )
        self.resultview.column(
            column=1,
            anchor=W,
            width=utility.scale_size(self, 80),
            stretch=False
        )
        self.resultview.column(
            column=2,
            anchor=E,
            width=utility.scale_size(self, 150),
            stretch=False
        )
        self.resultview.column(
            column=3,
            anchor=E,
            width=utility.scale_size(self, 100),
            stretch=False
        )
        self.resultview.column(
            column=4,
            anchor=W,
            width=utility.scale_size(self, 300)
        )

    # def on_browse(self):
    #     """Callback for directory browse"""
    #     path = askdirectory(title="Browse directory")
    #     if path:
    #         self.path_var.set(path)


if __name__ == '__main__':

    app = ttk.Window("Crawl Search Engine\t\t\t\t\t\t\tMade By CHAOS", "journal")
    FileSearchEngine(app)
    app.mainloop()
