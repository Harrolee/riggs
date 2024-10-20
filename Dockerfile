FROM python:3.12

ADD requirements.txt .
RUN pip install -r requirements.txt

COPY lyrics/ lyrics/
COPY fonts/ fonts/
COPY *.py pyrightconfig.json ./
CMD ["python3", "./main.py"] 