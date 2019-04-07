FROM circleci/python:3.6-browsers

COPY . /app
RUN pip install --user -r /app/requirements.txt
RUN sudo touch /geckodriver.log && sudo chmod 777 /geckodriver.log
CMD python /app/script.py 