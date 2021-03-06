FROM public.ecr.aws/lambda/python:3.8

ENV DEBIAN_FRONTEND=noninteractive

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}

# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"


ENV PORT 8080

# ENTRYPOINT ["tini", "--"]
CMD [ "app.handler" ] 