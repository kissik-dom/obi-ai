# Kingdom AI OS Vault server configuration.
# Proper (non-dev) server mode backed by file storage on a persistent volume.
storage "file" {
  path = "/vault/file"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = "true"
}

api_addr = "http://127.0.0.1:8200"
disable_mlock = true