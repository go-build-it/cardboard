FROM python:3 as builder
RUN ["pip", "install", "pipenv"]
COPY Pipfile Pipfile.lock /project/
WORKDIR /project
RUN pipenv lock --requirements > /tmp/requirements.txt


# This is the real container
FROM python:3
# We need git, tar

COPY --from=builder /tmp /tmp
RUN pip install --no-cache-dir --disable-pip-version-check -r /tmp/requirements.txt

COPY . /project
WORKDIR /project
