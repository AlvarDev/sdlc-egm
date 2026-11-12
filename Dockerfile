# Stage 1: Build static Go binary
FROM golang:1.23-alpine AS builder

WORKDIR /src
COPY go.mod server.go ./
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -o /out/codelab-server server.go

# Stage 2: Minimal Google Distroless static runtime (nonroot)
FROM gcr.io/distroless/static-debian12:nonroot

WORKDIR /app
COPY --from=builder /out/codelab-server /app/codelab-server
COPY docs /app/docs

ENV PORT=8080
EXPOSE 8080
USER nonroot:nonroot

ENTRYPOINT ["/app/codelab-server"]
