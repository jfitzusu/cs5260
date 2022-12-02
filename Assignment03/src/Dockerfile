FROM python:3.9
COPY requirments.txt requirments.txt
RUN pip3 install -r requirments.txt
COPY *.py /src/
CMD ["python", "/src/consumer.py", "--rq", "cs5260-requests", "--wb", "usu-cs5260-snarl-dist", "-v"]