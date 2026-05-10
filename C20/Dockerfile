FROM ubuntu:22.04
RUN apt-get update && apt-get install -y gcc gcc-multilib socat --no-install-recommends && rm -rf /var/lib/apt/lists/*
WORKDIR /challenge
COPY vuln.c .
RUN gcc -m32 -fno-stack-protector -no-pie -w -o mission_terminal vuln.c
RUN echo "cyn0x{buff3r_0v3rfl0w_w1nt3r_s0ld13r}" > /flag.txt && chmod 444 /flag.txt
EXPOSE 1337
CMD ["socat","TCP-LISTEN:1337,reuseaddr,fork","EXEC:./mission_terminal"]