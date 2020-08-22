import threading
import sys
import queue
import requests
from bs4 import BeautifulSoup
import json

def strip_whitespace(text):
  while "  " in text:
    text = text.replace("  ", " ")

  return text.strip()

def extract_questions(question_url):
  global questions

  r = requests.get(question_url)
  
  if r.url.split("/")[4] == question_url.split("/")[4]:
    content = r.content.decode()

    idx = content.index("<title>") + 7
    sub_content = content[idx:]
    idx = sub_content.index(" - Mathematics Stack Exchange")
    title = sub_content[:idx]

    if title != "Page not found":
      idx = content.index('<div class="post-text"')
      sub_content = content[idx:]
      idx = sub_content.index("\n")
      sub_content = sub_content[idx + 1:]
      idx = sub_content.index("</div>")
      question = strip_whitespace(sub_content[:idx].replace("\n", "").replace("\t", "").replace("\r", ""))
      
      with open(save_filepath, "a") as f:
        data = json.load(f)
        data.update({'url': r.url, 'title': title, 'question': question})
        f.seek(0)
        json.dump(data, f)
      
      f.close()

    return r.status_code
  else:
    return "Nonexistent question ID"

def do_work():
  while True:
    question_id = q.get()
    status, question_url = get_status(question_id)
    do_something_with_result(status, question_url)
    q.task_done()

def get_status(question_id):
  try:
    question_url = "https://math.stackexchange.com/questions/{}/".format(question_id)
    status_code = extract_questions(question_url)
    return status_code, question_url
  except:
    return "Error", question_url

def do_something_with_result(status, url):
  print (url, status)

save_filepath = sys.argv[1]
  
concurrent = 200
questions = []
q = queue.Queue(concurrent * 2)

for i in range(concurrent):
  thread = threading.Thread(target = do_work)
  thread.daemon = True
  thread.start()

try:
  for question_id in range(1, 1000):
    q.put(question_id)

  q.join()
except KeyboardInterrupt:
  sys.exit(1)
