FROM python:3.11-slim

# Prevents Python from buffering stdout/stderr, so 'docker compose logs'
# shows print() output immediately instead of holding it in a buffer --
# useful for the print('everything is working!') sanity checks the course
# README recommends.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy and install dependencies first, separately from the rest of the app
# code. Docker caches each instruction as a layer; as long as
# requirements.txt hasn't changed, this layer is reused on rebuilds instead
# of re-downloading every package, which matters a lot given how often
# you'll be rebuilding while iterating.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the project.
COPY . .

RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
