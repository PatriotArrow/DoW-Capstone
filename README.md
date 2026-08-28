## Setup

### 1. Serverless platform (OpenFaaS on k3s)

# Install k3s
curl -sfL https://get.k3s.io | sh -

# Configure kubeconfig
mkdir -p ~/.kube
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $USER:$USER ~/.kube/config

# Install OpenFaaS
arkade install openfaas


Note: Traefik (bundled with k3s) was disabled to free port 80 for Apache.

### 2. Deploy the function

faas-cli template store pull python3-http
# Add pillow to requirements.txt, edit handler.py
faas-cli build -f stack.yml
faas-cli deploy -f stack.yml
faas-cli list


### 3. Apache front end


sudo apt install apache2 -y
sudo a2enmod proxy proxy_http
# Configure reverse proxy in /etc/apache2/sites-enabled/000-default.conf
sudo systemctl restart apache2


### 4. Monitoring


# Prometheus ships with OpenFaaS
kubectl port-forward -n openfaas svc/prometheus 9090:9090 &

# Install Grafana (optional, for dashboards)
sudo apt install grafana -y
sudo systemctl start grafana-server

### 5. Cloudflare

# Install cloudflared
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared
chmod +x cloudflared
sudo mv cloudflared /usr/local/bin/

# Run the tunnel (requires a domain added to Cloudflare)
cloudflared tunnel run waf-research

## Running the experiment

Keep the gateway forwarded while running:

kubectl port-forward -n openfaas svc/gateway 8080:8080 &


### Generate traffic

# Normal traffic
locust -f locustfile.py NormalUser --host https://<your-domain>

# Attack traffic
locust -f locustfile.py LeechAttacker --host https://<your-domain>

### Measure cost

kubectl port-forward -n openfaas svc/prometheus 9090:9090 &
python3 openfaas-commercial-platform-emulator/priceCalc.py
