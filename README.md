# API Client GUIs

mã python đơn giản để gửi yêu cầu đến các API URL thông qua giao diện đồ họa GUI từ các thư viện `tkinter` , `wxPython`, `toga` .


## các phụ thuộc

```bash
pip install requests
pip install toga
pip install wxPython
```


## GUI tkinter
thư viện mặc định của python nên khỏi cài 


```python
import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json

class APIClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("API Client")

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # URL Entry
        ttk.Label(self.root, text="API URL:").grid(column=0, row=0, padx=10, pady=10, sticky="E")
        self.url_entry = ttk.Entry(self.root, width=50)
        self.url_entry.grid(column=1, row=0, padx=10, pady=10)

        # Method Selection
        self.method_var = tk.StringVar(value="GET")
        ttk.Label(self.root, text="Method:").grid(column=0, row=1, padx=10, pady=10, sticky="E")
        method_options = ["GET", "POST", "PUT", "DELETE"]
        self.method_menu = ttk.OptionMenu(self.root, self.method_var, *method_options)
        self.method_menu.grid(column=1, row=1, padx=10, pady=10)

        # Data Entry (for POST, PUT requests)
        ttk.Label(self.root, text="Data (JSON):").grid(column=0, row=2, padx=10, pady=10, sticky="E")
        self.data_entry = tk.Text(self.root, height=10, width=50)
        self.data_entry.grid(column=1, row=2, padx=10, pady=10)

        # Send Button
        self.send_button = ttk.Button(self.root, text="Send Request", command=self.send_request)
        self.send_button.grid(column=0, row=3, columnspan=2, pady=10)

        # Response Text
        ttk.Label(self.root, text="Response:").grid(column=0, row=4, padx=10, pady=10, sticky="E")
        self.response_text = tk.Text(self.root, height=10, width=50)
        self.response_text.grid(column=1, row=4, padx=10, pady=10)

    def send_request(self):
        url = self.url_entry.get()
        method = self.method_var.get()
        data = self.data_entry.get("1.0", tk.END).strip()

        try:
            if method == "GET":
                response = requests.get(url)
            elif method == "POST":
                json_data = self.parse_json(data)
                if not json_data:
                    return
                response = requests.post(url, json=json_data)
            elif method == "PUT":
                json_data = self.parse_json(data)
                if not json_data:
                    return
                response = requests.put(url, json=json_data)
            elif method == "DELETE":
                response = requests.delete(url)

            self.response_text.delete("1.0", tk.END)
            self.response_text.insert(tk.END, f"Status Code: {response.status_code}\n")
            try:
                json_response = response.json()
                formatted_response = json.dumps(json_response, indent=4)
                self.response_text.insert(tk.END, f"Response:\n{formatted_response}")
            except json.JSONDecodeError:
                self.response_text.insert(tk.END, f"Response:\n{response.text}")
        except requests.RequestException as e:
            messagebox.showerror("Request Error", str(e))

    def parse_json(self, data):
        import json
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            messagebox.showerror("JSON Error", "Invalid JSON format")
            return {}


if __name__ == "__main__":
    root = tk.Tk()
    app = APIClientApp(root)
    root.mainloop()
```


## GUI wxPython

```python
import wx
import requests
import json

class APIClientFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(APIClientFrame, self).__init__(*args, **kw)

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.url_input = wx.TextCtrl(panel, size=(400, -1))
        sizer.Add(wx.StaticText(panel, label="API URL:"), 0, wx.ALL, 5)
        sizer.Add(self.url_input, 0, wx.ALL, 5)

        self.method_choice = wx.Choice(panel, choices=["GET", "POST", "PUT", "DELETE"])
        sizer.Add(wx.StaticText(panel, label="Method:"), 0, wx.ALL, 5)
        sizer.Add(self.method_choice, 0, wx.ALL, 5)

        self.data_input = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size=(400, 100))
        sizer.Add(wx.StaticText(panel, label="Data (JSON):"), 0, wx.ALL, 5)
        sizer.Add(self.data_input, 0, wx.ALL, 5)

        send_button = wx.Button(panel, label="Send Request")
        send_button.Bind(wx.EVT_BUTTON, self.send_request)
        sizer.Add(send_button, 0, wx.ALL, 5)

        self.response_output = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(400, 200))
        sizer.Add(wx.StaticText(panel, label="Response:"), 0, wx.ALL, 5)
        sizer.Add(self.response_output, 0, wx.ALL, 5)

        panel.SetSizer(sizer)
        self.SetSize((500, 500))
        self.SetTitle("API Client")

    def send_request(self, event):
        url = self.url_input.GetValue()
        method = self.method_choice.GetStringSelection()
        data = self.data_input.GetValue()

        try:
            if method == "GET":
                response = requests.get(url)
            elif method == "POST":
                response = requests.post(url, json=self.parse_json(data))
            elif method == "PUT":
                response = requests.put(url, json=self.parse_json(data))
            elif method == "DELETE":
                response = requests.delete(url)

            self.response_output.SetValue(f"Status Code: {response.status_code}\n")
            try:
                json_response = response.json()
                formatted_response = json.dumps(json_response, indent=4)
                self.response_output.AppendText(f"Response:\n{formatted_response}")
            except json.JSONDecodeError:
                self.response_output.AppendText(f"Response:\n{response.text}")
        except requests.RequestException as e:
            self.response_output.SetValue(f"Request Error: {e}")

    def parse_json(self, data):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return {}

class APIClientApp(wx.App):
    def OnInit(self):
        frame = APIClientFrame(None)
        frame.Show()
        return True

if __name__ == "__main__":
    app = APIClientApp()
    app.MainLoop()
```

## GUI toga

```python
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import requests
import json

class APIClientApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.name)
        self.main_box = toga.Box(style=Pack(direction=COLUMN))

        self.url_input = toga.TextInput(placeholder='API URL')
        self.method_choice = toga.Selection(items=["GET", "POST", "PUT", "DELETE"])
        self.data_input = toga.TextInput(placeholder='Data (JSON)', style=Pack(height=100))
        self.send_button = toga.Button('Send Request', on_press=self.send_request)
        self.response_output = toga.MultilineTextInput(style=Pack(height=200))

        self.main_box.add(self.url_input)
        self.main_box.add(self.method_choice)
        self.main_box.add(self.data_input)
        self.main_box.add(self.send_button)
        self.main_box.add(self.response_output)

        self.main_window.content = self.main_box
        self.main_window.show()

    def send_request(self, widget):
        url = self.url_input.value
        method = self.method_choice.value
        data = self.data_input.value

        try:
            if method == "GET":
                response = requests.get(url)
            elif method == "POST":
                response = requests.post(url, json=self.parse_json(data))
            elif method == "PUT":
                response = requests.put(url, json=self.parse_json(data))
            elif method == "DELETE":
                response = requests.delete(url)

            response_text = f"Status Code: {response.status_code}\n"
            try:
                json_response = response.json()
                formatted_response = json.dumps(json_response, indent=4)
                response_text += f"Response:\n{formatted_response}"
            except json.JSONDecodeError:
                response_text += f"Response:\n{response.text}"
            self.response_output.value = response_text
        except requests.RequestException as e:
            self.response_output.value = f"Request Error: {e}"

    def parse_json(self, data):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return {}

if __name__ == "__main__":
    app = APIClientApp('API Client', 'org.example.apiclient')
    app.main_loop()
```



## Tài liệu tham khảo
[tkinter](https://docs.python.org/3/library/tkinter.html)
[wxPython](https://github.com/wxWidgets/Phoenix)
[toga](https://toga.readthedocs.io/en/latest/)



