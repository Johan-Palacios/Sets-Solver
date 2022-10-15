FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /home/app
COPY ./ /home/app/
RUN python3 -m pip install -r requirements.txt
RUN cd /home/app && python3 make.py
RUN python3 /home/app/manage.py migrate
EXPOSE 8000/tcp
CMD ["python3", "/home/app/manage.py", "runserver", "0.0.0.0:8000"]
