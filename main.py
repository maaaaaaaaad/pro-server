import json
import os
import time
import tkinter as tk
from tkinter import messagebox
import re
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def save_data_to_file(data):
  with open('user_data.json', 'w') as f:
    json.dump(data, f)


def load_data_from_file():
  try:
    with open('user_data.json', 'r') as f:
      data = json.load(f)
  except FileNotFoundError:
    data = []
  return data


class App:

  def __init__(self, master):
    self.master = master
    self.entry_sets = []
    self.button_frame = tk.Frame(self.master)
    self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)
    self.select_all_frame = tk.Frame(self.master)
    self.select_all_frame.pack(side=tk.BOTTOM, fill=tk.X)
    self.add_button = tk.Button(self.master,
                                text="추가",
                                command=self.add_entry_set)
    self.add_button.pack()
    self.remove_button = tk.Button(self.button_frame,
                                   text="삭제",
                                   command=self.remove_entry_set)
    self.remove_button.pack(side=tk.LEFT)
    self.remove_button.pack_forget()
    self.all_var = tk.IntVar()
    self.all_checkbox = tk.Checkbutton(self.select_all_frame,
                                       text="전체 선택",
                                       variable=self.all_var,
                                       command=self.select_all)
    self.all_checkbox.pack(side=tk.BOTTOM, anchor=tk.CENTER)
    self.all_checkbox.pack_forget()
    self.execute_button = tk.Button(self.button_frame,
                                    text="실행",
                                    command=self.execute_entries)
    self.canvas = tk.Canvas(self.master)
    self.frame = tk.Frame(self.canvas)
    entries_data = load_data_from_file()
    for domain, login_id, password, board, title, content in entries_data:
      self.add_entry_set(domain, login_id, password, board, title, content)
    self.scrollbar = tk.Scrollbar(self.master,
                                  orient="vertical",
                                  command=self.canvas.yview)
    self.canvas.configure(yscrollcommand=self.scrollbar.set)
    self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    self.canvas.create_window((0, 0),
                              window=self.frame,
                              anchor=tk.NW,
                              tags="self.frame")
    self.frame.bind("<Configure>", self.on_frame_configure)

  def execute_entries(self):
    entries_data = []
    domain_pattern = re.compile(
      r"(?:http|ftp|https)://(?:[\w_-]+(?:(?:\.[\w_-]+)+))(?:[\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"
    )
    for entry_set, check_var in self.entry_sets:
      if not check_var.get():
        continue
      domain_entry = entry_set.grid_slaves(row=0, column=1)[0]
      id_entry = entry_set.grid_slaves(row=1, column=1)[0]
      password_entry = entry_set.grid_slaves(row=2, column=1)[0]
      board_domain_entry = entry_set.grid_slaves(row=3, column=1)[0]
      title_entry = entry_set.grid_slaves(row=4, column=1)[0]
      content_text = entry_set.grid_slaves(row=5, column=1)[0]
      domain = domain_entry.get()
      login_id = id_entry.get()
      password = password_entry.get()
      board = board_domain_entry.get()
      title = title_entry.get()
      content = content_text.get("1.0", tk.END).strip()
      if not domain or not login_id or not password or not board or not title or not content:
        messagebox.showerror("오류", "모든 필드를 입력해주세요.")
        return
      if not domain_pattern.match(domain):
        messagebox.showerror("오류", "로그인 도메인 주소가 올바르지 않습니다.")
        return
      if not domain_pattern.match(board):
        messagebox.showerror("오류", "게시판 도메인 주소가 올바르지 않습니다.")
        return
      entries_data.append((domain, login_id, password, board, title, content))
    driver_path = os.path.join(os.getcwd(), "chromedriver")
    service = Service(executable_path=driver_path)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-infobars')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    for domain, login_id, password, board, title, content in entries_data:
      escaped_domain = json.dumps(domain)
      driver.execute_script(f"window.open({escaped_domain})")
      driver.switch_to.window(driver.window_handles[-1])
      wait = WebDriverWait(driver, 10)
      wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
      id_field = driver.find_element(By.CSS_SELECTOR, "input[name*='id']")
      password_field = driver.find_element(By.CSS_SELECTOR,
                                           "input[name*='password']")
      try:
        wait.until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name*='id']")))
        id_field.send_keys(login_id)
        wait.until(
          EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[name*='password']")))
        password_field.send_keys(password)
        wait.until(
          EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[type*='submit']")))
        buttons = driver.find_elements(By.CSS_SELECTOR,
                                       "button[type*='submit']")
        login_button = None
        for button in buttons:
          wait.until(
            EC.element_to_be_clickable(
              (By.CSS_SELECTOR, "button[type*='submit']")))
          pattern = re.compile(r"(?i)(로그인|login)")
          if pattern.match(button.text.strip()):
            login_button = button
            break
        if login_button:
          login_button.click()
          time.sleep(3)
          driver.get(board)
          wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
          save_data_to_file(entries_data)
        else:
          messagebox.showerror("오류",
                               "로그인 버튼을 찾을 수 없습니다. 로그인 도메인 주소를 정확히 입력해주세요.")
          return
      except TimeoutException:
        print('Wait for timeout!')
    input("Press Enter to close the browser and exit the program...")
    print(entries_data)

  def select_all(self):
    for entry_set, check_var in self.entry_sets:
      check_var.set(self.all_var.get())

  def add_entry_set(self,
                    domain='',
                    login_id='',
                    password='',
                    board='',
                    title='',
                    content=''):
    entry_set = tk.Frame(self.frame)
    entry_set.pack(pady=10)
    check_var = tk.IntVar()
    check_button = tk.Checkbutton(entry_set, variable=check_var)
    check_button.grid(row=1, rowspan=1, column=3, padx=5, sticky=tk.W)
    domain_label = tk.Label(entry_set, text="도메인 로그인 주소:")
    domain_label.grid(row=0, column=0, padx=5, sticky=tk.E)
    domain_entry = tk.Entry(entry_set)
    domain_entry.grid(row=0, column=1)
    id_label = tk.Label(entry_set, text="로그인 아이디:")
    id_label.grid(row=1, column=0, padx=5, sticky=tk.E)
    id_entry = tk.Entry(entry_set)
    id_entry.grid(row=1, column=1)
    password_label = tk.Label(entry_set, text="로그인 패스워드:")
    password_label.grid(row=2, column=0, padx=5, sticky=tk.E)
    password_entry = tk.Entry(entry_set, show="*")
    password_entry.grid(row=2, column=1)
    board_domain_label = tk.Label(entry_set, text="게시판 주소(url):")
    board_domain_label.grid(row=3, column=0, padx=5, sticky=tk.E)
    board_domain_entry = tk.Entry(entry_set)
    board_domain_entry.grid(row=3, column=1)
    title_label = tk.Label(entry_set, text="글 제목:")
    title_label.grid(row=4, column=0, padx=5, sticky=tk.E)
    title_entry = tk.Entry(entry_set)
    title_entry.grid(row=4, column=1)
    content_label = tk.Label(entry_set, text="글 내용:")
    content_label.grid(row=5, column=0, padx=5, sticky=tk.E)
    content_text = tk.Text(entry_set, height=5, width=26)
    content_text.grid(row=5, column=1)
    domain_entry.insert(0, domain)
    id_entry.insert(0, login_id)
    password_entry.insert(0, password)
    board_domain_entry.insert(0, board)
    title_entry.insert(0, title)
    content_text.insert('1.0', content)
    self.entry_sets.append((entry_set, check_var))
    self.update_remove_button_state()

  def update_all_checkbox_state(self):
    self.all_var.set(0)

  def remove_entry_set(self):
    for entry_set, check_var in self.entry_sets[:]:
      if check_var.get():
        entry_set.destroy()
        self.entry_sets.remove((entry_set, check_var))
    self.update_remove_button_state()
    self.update_all_checkbox_state()

  def update_remove_button_state(self):
    if self.entry_sets:
      self.remove_button.pack()
      self.all_checkbox.pack(side=tk.BOTTOM, anchor=tk.CENTER)
      self.execute_button.pack(side=tk.BOTTOM)
    else:
      self.remove_button.pack_forget()
      self.all_checkbox.pack_forget()
      self.execute_button.pack_forget()

  def on_frame_configure(self, _event):
    self.canvas.configure(scrollregion=self.canvas.bbox("all"))


if __name__ == "__main__":
  root = tk.Tk()
  screen_width = root.winfo_screenwidth()
  screen_height = root.winfo_screenheight()
  x_coordinate = int((screen_width / 2) - (600 / 2))
  y_coordinate = int((screen_height / 2) - (800 / 2))
  root.geometry(f"600x800+{x_coordinate}+{y_coordinate}")
  root.resizable(False, False)
  app = App(root)
  root.mainloop()
