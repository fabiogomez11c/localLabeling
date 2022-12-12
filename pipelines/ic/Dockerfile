FROM us-docker.pkg.dev/vertex-ai/training/tf-cpu.2-8:m92

WORKDIR /

COPY . .

# RUN pip install -r requirements.txt

ENTRYPOINT ["python", "-m", "trainer.task"]
