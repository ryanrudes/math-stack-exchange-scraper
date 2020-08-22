import threading
import sys
import queue
import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

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

    questions.append({
        'url': question_url,
        'title': title,
        'question': question
    })

    return r.status_code
  else:
    return "Nonexistent question ID"

def do_work():
  while True:
    question_id = q.get()
    status, question_url = get_status(question_id)
    q.task_done()

def get_status(question_id):
  try:
    question_url = "https://math.stackexchange.com/questions/{}/".format(question_id)
    status_code = extract_questions(question_url)
    return status_code, question_url
  except:
    return "Error", question_url

save_file_path, concurrent, num_questions = sys.argv[1:3]
concurrent = int(concurrent)
num_questions = int(num_questions)

questions = []
q = queue.Queue(concurrent * 2)

for i in range(concurrent):
  thread = threading.Thread(target = do_work)
  thread.daemon = True
  thread.start()

try:
  for question_id in tqdm(range(1, num_questions + 1)):
    q.put(question_id)

  q.join()
except KeyboardInterrupt:
  sys.exit(1)

with open(save_file_path, "w") as f:
  json.dump(questions, f)

f.close()
