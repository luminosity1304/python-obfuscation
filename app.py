import base64
import zlib
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText


def _xor_bytes(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def obfuscate_source(source: str, key: str = "secret") -> str:
    if not isinstance(source, str):
        raise TypeError("source must be a str")
    key_bytes = key.encode("utf-8")
    if not key_bytes:
        key_bytes = b"\x00"
    compressed = zlib.compress(source.encode("utf-8"))
    xored = _xor_bytes(compressed, key_bytes)
    return base64.b64encode(xored).decode("ascii")


def deobfuscate_source(blob: str, key: str = "secret") -> str:
    if not isinstance(blob, str):
        raise TypeError("blob must be a str")
    key_bytes = key.encode("utf-8")
    if not key_bytes:
        key_bytes = b"\x00"
    raw = base64.b64decode(blob)
    xored = _xor_bytes(raw, key_bytes)
    return zlib.decompress(xored).decode("utf-8")


def obfuscate_python(source: str, key: str = "secret") -> str:
    return obfuscate_source(source, key)


def deobfuscate_python(blob: str, key: str = "secret") -> str:
    return deobfuscate_source(blob, key)


def obfuscate_lua(source: str, key: str = "secret") -> str:
    return obfuscate_source(source, key)


def deobfuscate_lua(blob: str, key: str = "secret") -> str:
    return deobfuscate_source(blob, key)


class ObfApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("python obfuscation")
        self.geometry("900x600")
        self._build()

    def _build(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True)

        self.frame_obf = ttk.Frame(notebook)
        self.frame_deobf = ttk.Frame(notebook)

        notebook.add(self.frame_obf, text="obfuscate")
        notebook.add(self.frame_deobf, text="deobfuscate")

        # common controls
        for frame in (self.frame_obf, self.frame_deobf):
            top = ttk.Frame(frame)
            top.pack(fill=tk.X, padx=6, pady=6)

            ttk.Label(top, text="language").pack(side=tk.LEFT)
            lang = ttk.Combobox(top, values=["python", "lua"], width=10)
            lang.current(0)
            lang.pack(side=tk.LEFT, padx=4)

            ttk.Label(top, text="key").pack(side=tk.LEFT, padx=(10, 0))
            key_entry = ttk.Entry(top, width=25)
            key_entry.insert(0, "secret")
            key_entry.pack(side=tk.LEFT, padx=4)

            setattr(frame, "lang_widget", lang)
            setattr(frame, "key_widget", key_entry)

        # Obfuscate tab
        ttk.Label(self.frame_obf, text="source").pack(anchor=tk.W, padx=6)
        self.src_text = ScrolledText(self.frame_obf, height=18)
        self.src_text.pack(fill=tk.BOTH, expand=True, padx=6)

        btn_frame = ttk.Frame(self.frame_obf)
        btn_frame.pack(fill=tk.X, pady=6, padx=6)

        ttk.Button(btn_frame, text="open", command=self.open_source).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="save obfuscated", command=self.save_obfuscated).pack(
            side=tk.LEFT, padx=6
        )
        ttk.Button(btn_frame, text="obfuscate", command=self.do_obfuscate).pack(side=tk.RIGHT)

        ttk.Label(self.frame_obf, text="obfuscated output").pack(anchor=tk.W, padx=6)
        self.obf_text = ScrolledText(self.frame_obf, height=8)
        self.obf_text.pack(fill=tk.BOTH, expand=False, padx=6)

        # deobfuscate tab
        ttk.Label(self.frame_deobf, text="obfuscated input").pack(anchor=tk.W, padx=6)
        self.inp_text = ScrolledText(self.frame_deobf, height=12)
        self.inp_text.pack(fill=tk.BOTH, expand=True, padx=6)

        btn_frame2 = ttk.Frame(self.frame_deobf)
        btn_frame2.pack(fill=tk.X, pady=6, padx=6)

        ttk.Button(btn_frame2, text="open", command=self.open_obf).pack(side=tk.LEFT)
        ttk.Button(btn_frame2, text="deobfuscate", command=self.do_deobfuscate).pack(side=tk.RIGHT)

        ttk.Label(self.frame_deobf, text="deobfuscated output").pack(anchor=tk.W, padx=6)
        self.deobf_text = ScrolledText(self.frame_deobf, height=10)
        self.deobf_text.pack(fill=tk.BOTH, expand=False, padx=6)

    def open_source(self):
        path = filedialog.askopenfilename(
            filetypes=[("python lua files", "*.py *.lua"), ("all files", "*")]
        )
        if not path:
            return
        with open(path, "r", encoding="utf-8") as f:
            self.src_text.delete("1.0", tk.END)
            self.src_text.insert(tk.END, f.read())

    def save_obfuscated(self):
        txt = self.obf_text.get("1.0", tk.END).strip()
        if not txt:
            messagebox.showinfo("save", "no obfuscated data to save")
            return
        path = filedialog.asksaveasfilename(defaultextension=".obf", filetypes=[("obf files", "*.obf")])
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(txt)
        messagebox.showinfo("saved", f"saved to {path}")

    def do_obfuscate(self):
        src = self.src_text.get("1.0", tk.END)
        lang = self.frame_obf.lang_widget.get().lower()
        key = self.frame_obf.key_widget.get()
        try:
            if lang == "python":
                out = obfuscate_python(src, key)
            else:
                out = obfuscate_lua(src, key)
            self.obf_text.delete("1.0", tk.END)
            self.obf_text.insert(tk.END, out)
            messagebox.showinfo("done", "obfuscation complete")
        except Exception as e:
            messagebox.showerror("error", str(e))

    def open_obf(self):
        path = filedialog.askopenfilename(filetypes=[("obf files", "*.obf"), ("all files", "*")])
        if not path:
            return
        with open(path, "r", encoding="utf-8") as f:
            self.inp_text.delete("1.0", tk.END)
            self.inp_text.insert(tk.END, f.read())

    def do_deobfuscate(self):
        blob = self.inp_text.get("1.0", tk.END).strip()
        lang = self.frame_deobf.lang_widget.get().lower()
        key = self.frame_deobf.key_widget.get()
        try:
            if lang == "python":
                out = deobfuscate_python(blob, key)
            else:
                out = deobfuscate_lua(blob, key)
            self.deobf_text.delete("1.0", tk.END)
            self.deobf_text.insert(tk.END, out)
            messagebox.showinfo("done", "deobfuscation complete")
        except Exception as e:
            messagebox.showerror("error", str(e))


def main():
    app = ObfApp()
    app.mainloop()


if __name__ == "__main__":
    main()
