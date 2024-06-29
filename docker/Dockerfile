# builder container
FROM golang:1.21.1-alpine AS builder
# set go env vars
ENV GO111MODULE=on
ENV CGO_ENABLED=0
ENV GOOS=linux
ENV GOARCH=amd64
# install necessary toolset for build musl-dev
RUN apk add --no-cache git make bash gcc
# set work dir
WORKDIR /go/src/github.com/cosmos/gaia
# clone gaia
RUN git clone --branch v17.2.0 https://github.com/cosmos/gaia.git .
# build binary
RUN make build

# ------------------------

# use alpine image for main container (lean image, perfect for node setup)
FROM alpine:3.20.1

# package to allow https
RUN apk add --no-cache ca-certificates

# copy binary from builder container to main container
COPY --from=builder /go/src/github.com/cosmos/gaia/build/gaiad /usr/bin/gaiad
# create gaia user for better security, do not use root user
RUN addgroup -S gaia && adduser -S gaia -G gaia
USER gaia

# chain envs - ideally this should be in an env file
ENV CHAIN_NAME="newchain"
ENV INITIAL_VALIDATOR="newval"
ENV KEYRING_BACKEND="test"
ENV MINIMUM_GAS_PRICE="0.025uatom"
ENV INITIAL_VALIDATOR_BALANCE="1000000000stake"
ENV INITIAL_VALIDATOR_STAKE="100000000stake"

# Initialize chain and genesis
RUN gaiad init $INITIAL_VALIDATOR --chain-id=$CHAIN_NAME
RUN gaiad keys add $INITIAL_VALIDATOR --keyring-backend $KEYRING_BACKEND
RUN gaiad genesis add-genesis-account $INITIAL_VALIDATOR $INITIAL_VALIDATOR_BALANCE --keyring-backend $KEYRING_BACKEND
RUN gaiad genesis gentx $INITIAL_VALIDATOR $INITIAL_VALIDATOR_STAKE --chain-id $CHAIN_NAME --keyring-backend $KEYRING_BACKEND
RUN gaiad genesis collect-gentxs

# Enable telemetry with prometheus retention
RUN sed -i 's/enabled = false/enabled = true/' /home/gaia/.gaia/config/app.toml
RUN sed -i 's/prometheus-retention-time = 0/prometheus-retention-time = 60/' /home/gaia/.gaia/config/app.toml

# start gaiad
CMD ["sh", "-c", "gaiad start --minimum-gas-prices ${MINIMUM_GAS_PRICE}"]

# expose 26656 for peer to peer connection and 26657 for rpc
EXPOSE 26656 26657
